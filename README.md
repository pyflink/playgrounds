# Playgrounds
Playgrounds aims to provide a quick-start environment and examples for users to quickly understand the features of PyFlink. Playgrounds setup environment with docker-compose and integrates PyFlink, Kafka, Python to make it easy for experience. The current Playgrounds examples are based on the latest PyFlink (1.13.0).

# Create Docker Image

```bash
cd image
 
# create docker image
docker build --tag pyflink/playgrounds:1.13.0-rc0 .

# publish docker image
docker push pyflink/playgrounds:1.13.0-rc0
```

# Environment Setup

1. Install [Docker](https://www.docker.com). 
2. Get Docker Compose configuration
```
git clone https://github.com/pyflink/playgrounds.git
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

You can check whether the environment is running correctly by visiting Flink Web UI [http://localhost:8088](http://localhost:8088).

# Examples
1. WordCount
2. Read and write with Kafka
3. Python UDF
4. Python UDF with dependencies
5. Python Pandas UDF
6. Python UDF with User-defined Metrics
7. Python UDF used in Java Table API jobs
8. Python UDF used in pure-SQL jobs

## 1-WordCount

Code：[1-word_count.py](https://github.com/pyflink/playgrounds/blob/master/examples/table/1-word_count.py)

Run:
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/table/1-word_count.py
```
Check Results:

A result file will be added in the path `/opt/examples/table/data/word_count_output/`, 

Check Results:
```
docker-compose exec taskmanager cat /opt/examples/table/data/word_count_output/part-aec367b4-5e68-4958-bbb9-98b264e0d314-cp-0-task-0-file-0
```

The results look like：
```
flink	2
pyflink	1
```

## 2-Read and write with Kafka

Code：[2-from_kafka_to_kafka.py](https://github.com/pyflink/playgrounds/blob/master/examples/table/2-from_kafka_to_kafka.py)

Run:
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/table/2-from_kafka_to_kafka.py
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

Code：[3-udf_add.py](https://github.com/pyflink/playgrounds/blob/master/examples/table/3-udf_add.py)

Run:
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/table/3-udf_add.py
```

A result file will be added in the path `/opt/examples/table/data/udf_add_output`

Check Results:
```
docker-compose exec taskmanager cat /opt/examples/table/data/udf_add_output/part-933b41cd-9388-4ba8-9437-cbf5f87c2469-cp-0-task-0-file-0
```

The results look like：

```
3
```

## 4-Python UDF with dependency

Code：[4-udf_add_with_dependency.py](https://github.com/pyflink/playgrounds/blob/master/examples/table/4-udf_add_with_dependency.py)

Check the [Python Dependency management](https://ci.apache.org/projects/flink/flink-docs-master/docs/dev/python/table/dependency_management/) for more details about how to handle Python UDF dependencies。

Run:
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/table/4-udf_add_with_dependency.py
```

A result file will be added in the path `/opt/examples/table/data/udf_add_with_dependency_output`

Check Results:
```
docker-compose exec taskmanager cat /opt/examples/table/data/udf_add_with_dependency_output/part-589bdd40-8cfe-4f50-9484-ae46629e0a90-0-0
```

The results look like：

```
3
```

## 5-Pandas UDF

Code：[5-pandas_udf_add.py](https://github.com/pyflink/playgrounds/blob/master/examples/table/5-pandas_udf_add.py)

Run:
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/table/5-pandas_udf_add.py
```

A result file will be added in the path `/opt/examples/table/data/pandas_udf_add_output/`

Check Results:
```
docker-compose exec taskmanager cat /opt/examples/table/data/pandas_udf_add_output/part-1e9a35a7-28c3-4a46-bb84-a2fb1d62e0ed-cp-0-task-0-file-0
```

The results look like：

```
3
```

## 6-Python UDF with Metrics

Code：[6-udf_metrics.py](https://github.com/pyflink/playgrounds/blob/master/examples/table/6-udf_metrics.py)

Run:
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/table/6-udf_metrics.py
```

Visit http://localhost:8081/#/overview , select the running job and check the metrics.

## 7-Python UDF used in Java Table API jobs

Code：[BlinkBatchPythonUdfSqlJob.java](https://github.com/pyflink/playgrounds/blob/master/examples/table/java/src/main/java/BlinkBatchPythonUdfSqlJob.java)

Compile:
```
cd examples/table/java
mvn clean package
cd -
```

Run:
```
docker-compose exec jobmanager ./bin/flink run -d -j /opt/examples/table/java/target/pyflink-playgrounds.jar -c BlinkBatchPythonUdfSqlJob -pyfs /opt/examples/table/utils/udfs.py
```

## 8-Python UDF used in pure-SQL jobs

SQL resource file: [sql-client.yaml](https://github.com/pyflink/playgrounds/blob/master/examples/table/sql/sql-client.yaml)

SQL Statement:
```
insert into sink select add_one(a) from (VALUES (1), (2), (3)) as source (a)
```

Run:
```
docker-compose exec jobmanager ./bin/sql-client.sh embedded --environment /opt/examples/table/sql/sql-client.yaml -pyfs /opt/examples/table/utils/udfs.py --update "insert into sink select add_one(a) from (VALUES (1), (2), (3)) as source (a)"
```

Check Results:
A result file will be added in the path `examples/table/data/sql-test-out/`, with the following content：
```
2
3
4
```
