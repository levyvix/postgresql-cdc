# Apache Spark & Trip Record Data Analysis [Spark Measure]
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

![Roadmap](./docs/perf-spark.png)

### verify local spark installation
```shell
pip install -r requirements.txt
pyspark --version

spark-submit --help
http://localhost:4040/jobs/
```

### install required packages
```shell
pip install -r requirements.txt
```


### build spark docker images [spark & history server]
```shell
docker build -t owshq-spark:3.5 -f Dockerfile.spark . 
docker build -t owshq-spark-history-server:3.5 -f Dockerfile.history .
```

### run spark cluster & history server on docker
```shell
docker-compose up -d
docker ps
```

### download files & save on [storage] folder
```shell
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
```

### execute spark application
```shell
docker exec -it spark-master /opt/bitnami/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  /opt/bitnami/spark/jobs/my_spark_docker.py
```

### access spark history server
```shell
http://localhost:8080/
http://localhost:18080/
```

### tier down resources
```shell
docker-compose down
```
