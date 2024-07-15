from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("ReadFromMinio")
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

spark.read.json("s3a://commerce/cdc-.sales.orders/**/**/*.json").show()

spark.stop()
