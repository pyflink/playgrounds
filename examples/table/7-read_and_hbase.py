from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import StreamTableEnvironment, EnvironmentSettings


s_env = StreamExecutionEnvironment.get_execution_environment()
s_env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
s_env.set_parallelism(1)

# use blink table planner
st_env = StreamTableEnvironment \
    .create(s_env, environment_settings=EnvironmentSettings
            .new_instance()
            .in_streaming_mode()
            .use_blink_planner().build())


source_ddl = """CREATE TABLE MySourceTable (
hbase_rowkey_name varchar, cf1 ROW<word varchar>) WITH (
        'connector.type' = 'hbase',
        'connector.version' = '1.4.3',  
        'connector.table-name' = 'flink-test',  
        'connector.zookeeper.quorum' = 'localhost:2181')
"""

sink_ddl = """CREATE TABLE MySinkTable (
hbase_rowkey_name varchar, cf1 ROW<cnt bigint>) WITH (
        'connector.type' = 'hbase',
        'connector.version' = '1.4.3',  
        'connector.table-name' = 'result',  
        'connector.zookeeper.quorum' = 'localhost:2181')
"""

st_env.sql_update(source_ddl)
st_env.sql_update(sink_ddl)

st_env.from_path('MySourceTable') \
    .select('cf1.flatten()') \
    .group_by('cf1$word') \
    .select('cf1$word, ROW(count(1)) as cnt') \
    .insert_into('MySinkTable')

st_env.execute("7-read_and_hbase")