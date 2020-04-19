#!/usr/bin/env bash
/opt/hbase-1.4.13/bin/start-hbase.sh
echo "create 'flink-test', 'cf1'" | /opt/hbase-1.4.13/bin/hbase shell
echo "put 'flink-test', 'row1', 'cf1:word', 'flink'" | /opt/hbase-1.4.13/bin/hbase shell
echo "put 'flink-test', 'row2', 'cf1:word', 'flink'" | /opt/hbase-1.4.13/bin/hbase shell
echo "put 'flink-test', 'row3', 'cf1:word', 'pyflink'" | /opt/hbase-1.4.13/bin/hbase shell
echo "create 'result', 'cf1'" | /opt/hbase-1.4.13/bin/hbase shell


