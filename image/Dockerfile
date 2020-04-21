###############################################################################
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

###############################################################################
# Build PyFlink Playground Image
###############################################################################

FROM flink:1.10.0-scala_2.11

# Install python
RUN set -ex; \
  apt-get update; \
  apt-get -y install python3; \
  apt-get -y install python3-pip; \
  apt-get -y install python3-dev; \
  ln -s /usr/bin/python3 /usr/bin/python; \
  ln -s /usr/bin/pip3 /usr/bin/pip

# Install pyflink
RUN set -ex; \
  apt-get update; \
  python -m pip install --upgrade pip; \
  pip install apache-flink

ARG FLINK_VERSION=1.10.0

# Download connector libraries
RUN wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-json/${FLINK_VERSION}/flink-json-${FLINK_VERSION}.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-csv/${FLINK_VERSION}/flink-csv-${FLINK_VERSION}.jar; \
#    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-avro/${FLINK_VERSION}/flink-avro-${FLINK_VERSION}.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-jdbc_2.11/${FLINK_VERSION}/flink-jdbc_2.11-${FLINK_VERSION}.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/mysql/mysql-connector-java/8.0.19/mysql-connector-java-8.0.19.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-hive_2.11/${FLINK_VERSION}/flink-connector-hive_2.11-${FLINK_VERSION}.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-hbase_2.11/${FLINK_VERSION}/flink-hbase_2.11-${FLINK_VERSION}.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-hive_2.11/${FLINK_VERSION}/flink-connector-hive_2.11-${FLINK_VERSION}.jar; \
    wget -P /opt/flink/lib/ https://repo1.maven.org/maven2/org/apache/hive/hive-exec/2.3.4/hive-exec-2.3.4.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka_2.11/${FLINK_VERSION}/flink-sql-connector-kafka_2.11-${FLINK_VERSION}.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-elasticsearch6_2.11/${FLINK_VERSION}/flink-sql-connector-elasticsearch6_2.11-${FLINK_VERSION}.jar; \
# Create data folders
    mkdir -p /opt/data; \
    mkdir -p /opt/data/stream; \
    echo "taskmanager.memory.jvm-metaspace.size: 512m" >> /opt/flink/conf/flink-conf.yaml; \
    echo "rest.port: 8088" >> /opt/flink/conf/flink-conf.yaml;

# Install hbase and run
COPY ./hbase-fat.jar /opt/flink/lib
COPY ./hbase-1.4.13-bin.tar.gz /opt
#RUN wget -P /opt/ http://apache.spinellicreations.com/hbase/1.4.13/hbase-1.4.13-bin.tar.gz;
RUN tar zxvf /opt/hbase-1.4.13-bin.tar.gz -C /opt
RUN echo "export JAVA_HOME=/usr/local/openjdk-8" >> /opt/hbase-1.4.13/conf/hbase-env.sh
RUN echo "\n<configuration>\n  <property>\n    <name>hbase.tmp.dir</name>\n    <value>tmp</value>  </property>\n</configuration>" > /opt/hbase-1.4.13/conf/hbase-site.xml

WORKDIR /opt/flink