"""
docker exec -it spark-master1 /opt/bitnami/spark/bin/spark-submit  \
    --master spark://spark-master:7077   --deploy-mode client   \
        /opt/bitnami/spark/jobs/my_spark_docker.py
"""

from delta import *
from pyspark.sql import SparkSession

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

df = spark.read.json("s3a://commerce/cdc-.sales.orders/**/**/*.json")

df.write.format("delta").mode("overwrite").save("s3a://commerce/sales_orders_delta")
