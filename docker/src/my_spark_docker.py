"""
docker exec -it spark-master1 /opt/bitnami/spark/bin/spark-submit  \
    --master spark://spark-master:7077   --deploy-mode client   \
        /opt/bitnami/spark/jobs/my_spark_docker.py
"""

from delta import DeltaTable, configure_spark_with_delta_pip
from pyspark.sql import SparkSession
from utils import schemas


def create_spark_session():
    builder = (
        SparkSession.builder.appName("ReadFromMinio")
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .config("spark.hadoop.fs.s3a.access.key", "minio")
        .config("spark.hadoop.fs.s3a.secret.key", "minio123")
        .config("spark.hadoop.fs.s3a.path.style.access", True)
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config(
            "spark.jars.packages",
            "org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk-bundle:1.11.901",
        )
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
    )

    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    return spark


class Ingestor:
    def __init__(self, spark, catalog, schemaname, tablename, data_format):
        self.spark = spark
        self.catalog = catalog
        self.schemaname = schemaname
        self.tablename = tablename
        self.format = data_format
        self.set_schema()

    def set_schema(self):
        self.data_schema = schemas.get(self.tablename.split("_")[-1].upper())

    def load(self, path):
        df = self.spark.read.format(self.format).schema(self.data_schema).load(path)
        return df

    def save(self, df):
        (
            df.write.format("delta")
            .mode("overwrite")
            .save(f"s3a://commerce/{self.schemaname}/{self.catalog}/{self.tablename}")
        )
        return True

    def execute(self, path):
        df = self.load(path)
        return self.save(df)


# TODO: Make it work
class IngestorCDC(Ingestor):
    def __init__(
        self,
        spark,
        catalog,
        schemaname,
        tablename,
        data_format,
        id_field,
        timestamp_field,
    ):
        super().__init__(spark, catalog, schemaname, tablename, data_format)
        self.id_field = id_field
        self.timestamp_field = timestamp_field
        self.set_deltatable()

    def set_deltatable(self):
        tablename = f"{self.catalog}.{self.schemaname}.{self.tablename}"
        self.deltatable = DeltaTable.forName(self.spark, tablename)

    def upsert(self, df):
        df.createOrReplaceGlobalTempView(f"view_{self.tablename}")
        query = f"""
            SELECT *
            FROM global_temp.view_{self.tablename}
            QUALIFY ROW_NUMBER() OVER (PARTITION BY {self.id_field} ORDER BY {self.timestamp_field} DESC) = 1
        """

        df_cdc = self.spark.sql(query)

        (
            self.deltatable.alias("b")
            .merge(df_cdc.alias("d"), f"b.{self.id_field} = d.{self.id_field}")
            .whenMatchedDelete(condition="d.OP = 'D'")
            .whenMatchedUpdateAll(condition="d.OP = 'U'")
            .whenNotMatchedInsertAll(condition="d.OP = 'I' OR d.OP = 'U'")
            .execute()
        )

    def load(self, path):
        df = (
            self.spark.readStream.format("cloudFiles")
            .option("cloudFiles.format", self.format)
            .schema(self.data_schema)
            .load(path)
        )
        return df

    def save(self, df):
        stream = (
            df.writeStream.option(
                "checkpointLocation",
                f"/Volumes/raw/{self.schemaname}/cdc/{self.tablename}_checkpoint/",
            )
            .foreachBatch(lambda df, batchID: self.upsert(df))
            .trigger(availableNow=True)
        )
        return stream.start()


if __name__ == "__main__":
    spark = create_spark_session()
    catalog = "sales"
    schemaname = "bronze"
    tablename = ["orders", "users", "products"]
    data_format = "json"
    for table in tablename:
        ingestor = Ingestor(
            spark,
            catalog,
            schemaname,
            table,
            data_format,
        )
        ingestor.execute(f"s3a://commerce/cdc.sales.{table}/**/**/*.json")


# df = spark.read.json("s3a://commerce/cdc.sales.orders/**/**/*.json")

# df.write.format("delta").mode("overwrite").save("s3a://commerce/sales_orders_delta")
