from pyspark.sql import SparkSession
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
)

spark = (
    SparkSession.builder.appName("ReadFromMinio")
    # .master("spark://localhost:7077")
    .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000")
    .config("spark.hadoop.fs.s3a.access.key", "minio")
    .config("spark.hadoop.fs.s3a.secret.key", "minio123")
    .config("spark.hadoop.fs.s3a.path.style.access", True)
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config(
        "spark.jars.packages",
        "org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk-bundle:1.11.901",
    )
    .getOrCreate()
)

orders_schema = StructType(
    [
        StructField(
            "value",
            StructType(
                [
                    StructField("before", StringType(), True),
                    StructField(
                        "after",
                        StructType(
                            [
                                StructField("id", IntegerType(), True),
                                StructField("user_id", IntegerType(), True),
                                StructField("product_id", IntegerType(), True),
                                StructField("quantity", IntegerType(), True),
                                StructField("created_at", LongType(), True),
                                StructField("updated_at", LongType(), True),
                                StructField("deleted_at", StringType(), True),
                            ]
                        ),
                        True,
                    ),
                    StructField(
                        "source",
                        StructType(
                            [
                                StructField("version", StringType(), True),
                                StructField("connector", StringType(), True),
                                StructField("name", StringType(), True),
                                StructField("ts_ms", LongType(), True),
                                StructField("snapshot", StringType(), True),
                                StructField("db", StringType(), True),
                                StructField("sequence", StringType(), True),
                                StructField("schema", StringType(), True),
                                StructField("table", StringType(), True),
                                StructField("txId", IntegerType(), True),
                                StructField("lsn", LongType(), True),
                                StructField("xmin", StringType(), True),
                            ]
                        ),
                        True,
                    ),
                    StructField("op", StringType(), True),
                    StructField("ts_ms", LongType(), True),
                    StructField("transaction", StringType(), True),
                ]
            ),
            True,
        ),
    ]
)

# df = (
#     spark.readStream.format("json")
#     .schema(spark.read.json("s3a://commerce/cdc.sales.orders/**/**/*.json").schema)
#     .load("s3a://commerce/cdc.sales.orders/**/**/*.json")
# )

# query = df.writeStream.format("console").start()
# query.awaitTermination()


df = (
    spark.read.format("json")
    .schema(orders_schema)
    .load("s3a://commerce/cdc.sales.orders/**/**/*.json")
)
df.printSchema()
df.show()
