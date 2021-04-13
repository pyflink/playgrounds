from pyflink.table import StreamTableEnvironment, DataTypes, EnvironmentSettings
from pyflink.table.descriptors import Schema, OldCsv, FileSystem
from pyflink.table.udf import udf

env_settings = EnvironmentSettings.new_instance().in_streaming_mode().use_blink_planner().build()
t_env = StreamTableEnvironment.create(environment_settings=env_settings)
t_env.get_config().get_configuration().set_string('parallelism.default', '1')

add = udf(lambda i, j: i + j, [DataTypes.BIGINT(), DataTypes.BIGINT()], DataTypes.BIGINT())
t_env.create_temporary_function("add", add)


t_env.connect(FileSystem().path('/opt/examples/table/data/udf_add_input')) \
    .with_format(OldCsv()
                 .field('a', DataTypes.BIGINT())
                 .field('b', DataTypes.BIGINT())) \
    .with_schema(Schema()
                 .field('a', DataTypes.BIGINT())
                 .field('b', DataTypes.BIGINT())) \
    .create_temporary_table('mySource')

t_env.connect(FileSystem().path('/opt/examples/table/data/udf_add_output')) \
    .with_format(OldCsv()
                 .field('sum', DataTypes.BIGINT())) \
    .with_schema(Schema()
                 .field('sum', DataTypes.BIGINT())) \
    .create_temporary_table('mySink')

t_env.from_path('mySource')\
    .select("add(a, b)") \
    .insert_into('mySink')

t_env.execute("3-udf_add")
