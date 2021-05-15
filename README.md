# Playgrounds
Playgrounds aims to provide a quick-start environment and examples for users to quickly understand the features of PyFlink. Playgrounds setup environment with docker-compose and integrates PyFlink, Kafka, Python to make it easy for experience. The current Playgrounds examples are based on the latest PyFlink (1.13.0).

# Usage

Please checkout specific branches on how to use PyFlink in a specific Flink version as PyFlink is still in active development and more and more functionalities are added in each version.

# Create Docker Image

```bash
cd image
 
# create docker image
docker build --tag pyflink/playgrounds:1.13.0-rc2 .

# publish docker image
docker push pyflink/playgrounds:1.13.0-rc2
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

4. Check the logs of TM and JM

Check the logs of JM:
```bash
docker-compose logs jobmanager
```

Check the logs of TM:
```bash
docker-compose logs taskmanager
```

You can check whether the environment is running correctly by visiting Flink Web UI [http://localhost:8081](http://localhost:8081).

# Examples
1. PyFlink Table API WordCount
2. Read and write with Kafka using PyFlink Table API
3. Python UDF
4. Python UDF with dependencies
5. Python Pandas UDF
6. Python UDF with metrics
7. Python UDF used in Java Table API jobs
8. Python UDF used in pure-SQL jobs
9. PyFlink DataStream API WordCount
10. Keyed Stream of PyFlink DataStream API
11. State Access in PyFlink DataStream API

## 1-PyFlink Table API WordCount

Code：[1-word_count.py](https://github.com/pyflink/playgrounds/blob/master/examples/table/1-word_count.py)

Run:
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/table/1-word_count.py
```
Check Results:

A result file will be added in the path `/opt/examples/table/output/word_count_output/`, 

Check Results:
```
docker-compose exec taskmanager cat /opt/examples/table/output/word_count_output/part-aec367b4-5e68-4958-bbb9-98b264e0d314-cp-0-task-0-file-0
```

The results look like：
```
flink	2
pyflink	1
```

## 2-Read and write with Kafka using PyFlink Table API

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

A result file will be added in the path `/opt/examples/table/output/udf_add_output`

Check Results:
```
docker-compose exec taskmanager cat /opt/examples/table/output/udf_add_output/part-933b41cd-9388-4ba8-9437-cbf5f87c2469-cp-0-task-0-file-0
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

A result file will be added in the path `/opt/examples/table/output/udf_add_with_dependency_output`

Check Results:
```
docker-compose exec taskmanager cat /opt/examples/table/output/udf_add_with_dependency_output/part-589bdd40-8cfe-4f50-9484-ae46629e0a90-0-0
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

A result file will be added in the path `/opt/examples/table/output/pandas_udf_add_output/`

Check Results:
```
docker-compose exec taskmanager cat /opt/examples/table/output/pandas_udf_add_output/part-1e9a35a7-28c3-4a46-bb84-a2fb1d62e0ed-cp-0-task-0-file-0
```

The results look like：

```
3
```

## 6-Python UDF with metrics

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
A result file will be added in the path `/opt/examples/table/output/sql-test-out/`, with the following content：
```
2
3
4
```

## 9-PyFlink DataStream API WordCount

Code：[9-data_stream_word_count.py](https://github.com/pyflink/playgrounds/blob/master/examples/datastream/batch/9-data_stream_word_count.py)

Run:
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/datastream/batch/9-data_stream_word_count.py
```
Check Results:

A result file will be added in the path `/opt/examples/datastream/output/data_stream_word_count`, 

Check Results:
```
docker-compose exec taskmanager cat /opt/examples/datastream/output/data_stream_word_count/2021-04-14--03/pre-fa447e19-a6ad-42ca-966e-3a564c7fffde-0suf
```

The results look like：
```
+I[flink, 2]
+I[pyflink, 1]
```

## 10-PyFlink DataStream API ProcessFunction

Code：[10-data_stream_process_function.py](https://github.com/pyflink/playgrounds/blob/master/examples/datastream/batch/10-data_stream_process_function.py)

Run:
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/datastream/batch/10-data_stream_process_function.py
```
Check Results:

A result file will be added in the path `/opt/examples/datastream/output/data_stream_process_function_demo`,

## 11-State Access in PyFlink DataStream API

Code：[11-data_stream_state_access.py](https://github.com/pyflink/playgrounds/blob/master/examples/datastream/batch/11-data_stream_state_access.py)

Run:
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/datastream/batch/11-data_stream_state_access.py
```
Check Results:

A result file will be added in the path `/opt/examples/datastream/output/state_access`, 

Check Results:
```
docker-compose exec taskmanager cat /opt/examples/datastream/output/state_access/2021-04-14--09/pre-7b83235f-4737-4b2f-9af7-9de0e7d4a890-0suf
```

The results look like：
```
2
4
2
4
5
2
4
5
2
4
```
