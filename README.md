# Playgrounds
Playgrounds aims to provide a quick-start environment and examples for users to quickly understand the features of PyFlink. Playgrounds setup environment with docker-compose and integrates PyFlink, Kafka, Python to make it easy for experience. The current Playgrounds examples are based on the latest PyFlink (1.11).

# Create Docker Image

```bash
cd image

# create docker image
docker build --tag pyflink/playgrounds:1.11.0 .

# publish docker image
docker push pyflink/playgrounds:1.11.0
```

# Environment Setup

1. Install [Docker](https://www.docker.com). 
2. Get Docker Compose configuration
```
git clone -b 1.11 https://github.com/pyflink/playgrounds.git
```
3. Setup environment
* **Linux & MacOS**

```bash
cd playgrounds
docker-compose up -d
```

* **Windows**

```
cd playgrounds
set COMPOSE_CONVERT_WINDOWS_PATHS=1
docker-compose up -d
```

You can check whether the environment is running correctly by visiting Flink Web UI [http://localhost:8081](http://localhost:8081).

# Examples
1. WordCount
2. Read and write with Kafka
3. Python UDF
4. Python UDF with dependencies
5. 向量化Python UDF
6. Python UDF with User-defined metrics
7. Python UDF used in Java Table API jobs
8. Python UDF used in pure-SQL jobs


## 1-WordCount

Code：[1-word_count.py](https://github.com/pyflink/playgrounds/blob/1.11/examples/1-word_count.py)

Run:
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/1-word_count.py
```
Check Results:

A result file will be added in the path `examples/data/word_count_output/`, with the following content：
```
flink	2
pyflink	1
```

## 2-Read and write with Kafka

Code：[2-from_kafka_to_kafka.py](https://github.com/pyflink/playgrounds/blob/1.11/examples/2-from_kafka_to_kafka.py)

Run:
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/2-from_kafka_to_kafka.py
```

Check Results:
```
docker-compose exec kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic TempResults
```
The results look like：

```
{"rideId":3321,"taxiId":2013003189,"isStart":true,"lon":-73.99606,"lat":40.725132,"psgCnt":2,"rideTime":"2013-01-01T00:11:47Z"}
{"rideId":744,"taxiId":2013000742,"isStart":false,"lon":-73.97362,"lat":40.791283,"psgCnt":1,"rideTime":"2013-01-01T00:11:48Z"}
{"rideId":3322,"taxiId":2013003190,"isStart":true,"lon":-73.98382,"lat":40.74381,"psgCnt":1,"rideTime":"2013-01-01T00:11:48Z"}
{"rideId":3323,"taxiId":2013003191,"isStart":true,"lon":-74.00485,"lat":40.72102,"psgCnt":4,"rideTime":"2013-01-01T00:11:48Z"}
```
Stop job:

Visit http://localhost:8081/#/overview , select the running job and click the `Cancle` button.

## 3-Python UDF

Code：[3-udf_add.py](https://github.com/pyflink/playgrounds/blob/1.11/examples/3-udf_add.py)

Run:
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/3-udf_add.py
```
Check Results:

A result file will be added in the path `examples/data/udf_add_output/`, with the following content：
```
3
```

## 4-Python UDF with dependenciy

Code：[4-udf_add_with_dependency.py](https://github.com/pyflink/playgrounds/blob/1.11/examples/4-udf_add_with_dependency.py)

Check the [Python Dependency management](https://ci.apache.org/projects/flink/flink-docs-master/dev/table/python/dependency_management.html) for more details about how to handle Python UDF dependencies。

Run:
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/4-udf_add_with_dependency.py
```
Check Results:

A result file will be added in the path `examples/data/udf_add_with_dependency_output/`, with the following content：
```
3
```


## 5-向量化Python UDF

Code：[5-pandas_udf_add.py](https://github.com/pyflink/playgrounds/blob/1.11/examples/5-pandas_udf_add.py)

Run:
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/5-pandas_udf_add.py
```
Check Results:

A result file will be added in the path `examples/data/pandas_udf_add_output/`, with the following content：
```
3
```

## 6-Python UDF with Metrics

Code：[6-udf_metrics.py](https://github.com/pyflink/playgrounds/blob/1.11/examples/6-udf_metrics.py)

Run:
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/6-udf_metrics.py
```

Visit http://localhost:8081/#/overview , select the running job and check the metrics.

## 7-Python UDF used in Java Table API jobs

Code: [BlinkBatchPythonUdfSqlJob.java](https://github.com/pyflink/playgrounds/blob/1.11/examples/java/src/main/java/BlinkBatchPythonUdfSqlJob.java)

Compile:
```
cd examples/java
mvn clean package
cd -
```

Run:
```
docker-compose exec jobmanager ./bin/flink run -j /opt/examples/java/target/pyflink-playgrounds.jar -c BlinkBatchPythonUdfSqlJob -pyfs /opt/examples/utils/udfs.py
```

## 8-Python UDF used in pure-SQL jobs

SQL Statement
```
insert into sink select add_one(a) from (VALUES (1), (2), (3)) as source (a)
```

Run:
```
docker-compose exec jobmanager ./bin/sql-client.sh embedded --environment /opt/examples/sql/sql-client.yaml -pyfs /opt/examples/utils/udfs.py --update "insert into sink select add_one(a) from (VALUES (1), (2), (3)) as source (a)"
```
Check Results:

A result file will be added in the path `examples/data/sql-test-out/`, with the following content：
```
2
3
4
```