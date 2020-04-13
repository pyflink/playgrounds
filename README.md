# Playgrounds
Playgrounds 旨在提供快速上手的环境及例子，方便用户快速了解PyFlink的功能。Playgrounds采用docker-compose环境，集成了PyFlink、Kafka、Python。目前Playgrounds的例子基于最新的PyFlink 1.10.0。

# 环境配置

## 环境依赖
* **你只需要在你的电脑上安装[Docker](https://www.docker.com)。**

Docker 适用于 Linux, MacOS, 和 Windows。

**注意**：你需要为配置 Docker 配置足够的资源，以避免培训环境卡死无响应。
我们在以 3-4 GB 内存和 3-4 CPU 核运行的 Docker 上拥有良好的体验。

## 获取 Docker Compose 配置

Docker Compose 环境通过一个 YAML 文件来配置。默认的文件路径是 `docker-compose.yml`。

通过 clone 我们的 Git 仓库可以获取该环境的配置文件。

```
git clone https://github.com/pyflink/playgrounds.git
```
## 启动培训环境

为了运行培训环境，Docker 引擎需要先运行在你的电脑上。

另外，所有必需的 Docker 镜像都必须存在于本地映像存储中。Docker 会自动检查缺少的镜像并从 [Docker Hub](http://hub.docker.com) 下载。当第一次运行这个命令的时候，大概会花费几分钟去下载所有依赖的镜像（大约 2.3GB）。一旦镜像可用了，培训环境一般能在几秒钟内启动。

为了启动培训环境，需要打开命令行（Windows 用户可以使用 `cmd`），进入包含`docker-compose.yml`文件的目录，然后运行如下命令。 

* **Linux & MacOS**

```bash
docker-compose up -d
```

* **Windows**

```
set COMPOSE_CONVERT_WINDOWS_PATHS=1
docker-compose up -d
```

----

这个 `docker-compose` 会以 detached 模式启动所有 Docker Compose 配置中定义的容器。你可以通过访问 Flink Web UI [http://localhost:8081](http://localhost:8081) 来检查环境是否正确运行了。

# 例子
1. wordcount
2. read and write with kafka
3. python udf
4. python pandas udf
5. udf with metric

## 1-WordCount

启动程序
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/wordcount.py
```
查看结果

playgrounds/examples/data目录下会生成一个word_count_output结果文件，内容如下：
```
flink	2
pyflink	1
```

## 2-Read and write with Kafka

Kafka是一个常用的connector，本例子展示了如何读写Kafka。

启动命令
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/2-from_kafka_to_kafka.py
```
查看输出
```
docker-compose exec kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic TempResults
```
输出的内容大致如下：

```
{"rideId":3321,"taxiId":2013003189,"isStart":true,"lon":-73.99606,"lat":40.725132,"psgCnt":2,"rideTime":"2013-01-01T00:11:47Z"}
{"rideId":744,"taxiId":2013000742,"isStart":false,"lon":-73.97362,"lat":40.791283,"psgCnt":1,"rideTime":"2013-01-01T00:11:48Z"}
{"rideId":3322,"taxiId":2013003190,"isStart":true,"lon":-73.98382,"lat":40.74381,"psgCnt":1,"rideTime":"2013-01-01T00:11:48Z"}
{"rideId":3323,"taxiId":2013003191,"isStart":true,"lon":-74.00485,"lat":40.72102,"psgCnt":4,"rideTime":"2013-01-01T00:11:48Z"}
```
停止job

请访问http://localhost:8081/#/overview ，并选择运行的job，然后点Cancle.

## 3-Python UDF

启动命令
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/3-udf_add.py
```
查看输出

playgrounds/examples/data目录下会生成一个udf_add_output结果文件，内容如下：
```
3
```

## 4-Python UDF with dependenciy

假设我们对上面的例子进行修改，引入了外部依赖`mpmath`，此时，需要使用`set_python_requirements`来指定需要的依赖。Python UDF的依赖管理详见 [Python 依赖管理文档](https://ci.apache.org/projects/flink/flink-docs-master/dev/table/python/dependency_management.html)。

启动命令
```
cd playgrounds
docker-compose exec jobmanager ./bin/flink run -py /opt/examples/4-udf_add_with_dependency.py
```
查看输出

playgrounds/examples/data目录下会生成一个udf_add_output结果文件，内容如下：
```
3
```

