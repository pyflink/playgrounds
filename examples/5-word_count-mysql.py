from pyflink.dataset import ExecutionEnvironment
from pyflink.table import TableConfig, DataTypes, BatchTableEnvironment
from pyflink.table.descriptors import Schema, OldCsv, FileSystem

exec_env = ExecutionEnvironment.get_execution_environment()
exec_env.set_parallelism(1)
t_config = TableConfig()
t_env = BatchTableEnvironment.create(exec_env, t_config)

t_env.connect(FileSystem().path('/opt/examples/data/word_count_input')) \
    .with_format(OldCsv()
                 .field('word', DataTypes.STRING())) \
    .with_schema(Schema()
                 .field('word', DataTypes.STRING())) \
    .create_temporary_table('mySource')


sink_ddl = """CREATE TABLE MySinkTable (
    word varchar,
    count bigint) WITH (
        'connector.type' = 'jdbc',
        'connector.url' = 'jdbc:mysql://localhost:3306/flink-test',
        'connector.table' = 'jdbc_table_name',
        'connector.driver' = 'com.mysql.jdbc.Driver',
    )
"""
t_env.sql_update(sink_ddl)

t_env.from_path('mySource') \
    .group_by('word') \
    .select('word, count(1)') \
    .insert_into('mySink')

t_env.execute("tutorial_job")