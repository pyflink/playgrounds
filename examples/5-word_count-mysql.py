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


source_ddl = """CREATE TABLE MySourceTable (word varchar) WITH (
        'connector.type' = 'jdbc',
        'connector.url' = 'jdbc:mysql://db:3306/flink-test',
        'connector.table' = 'word',
        'connector.driver' = 'com.mysql.jdbc.Driver',
        'connector.username' = 'root',
        'connector.password' = 'example')
"""

sink_ddl = """CREATE TABLE MySinkTable (
    word varchar,
    cnt bigint) WITH (
        'connector.type' = 'jdbc',
        'connector.url' = 'jdbc:mysql://db:3306/flink-test',
        'connector.table' = 'result',
        'connector.driver' = 'com.mysql.jdbc.Driver',
        'connector.username' = 'root',
        'connector.password' = 'example')
"""

st_env.sql_update(source_ddl)
st_env.sql_update(sink_ddl)

st_env.from_path('MySourceTable') \
    .group_by('word') \
    .select('word, count(1)') \
    .insert_into('MySinkTable')

st_env.execute("5-word_count-mysql")