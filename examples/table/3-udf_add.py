from pyflink.table import DataTypes, EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import col
from pyflink.table.udf import udf

env_settings = EnvironmentSettings.new_instance().in_batch_mode().use_blink_planner().build()
t_env = TableEnvironment.create(environment_settings=env_settings)
t_env.get_config().get_configuration().set_string('parallelism.default', '1')

add = udf(lambda i, j: i + j, [DataTypes.BIGINT(), DataTypes.BIGINT()], DataTypes.BIGINT())


t_env.execute_sql("""
        CREATE TABLE mySource (
          a BIGINT,
          b BIGINT
        ) WITH (
          'connector' = 'filesystem',
          'format' = 'csv',
          'path' = '/opt/examples/table/input/udf_add_input'
        )
    """)

t_env.execute_sql("""
        CREATE TABLE mySink (
          `sum` BIGINT
        ) WITH (
          'connector' = 'filesystem',
          'format' = 'csv',
          'path' = '/opt/examples/table/output/udf_add_output'
        )
    """)

t_env.from_path('mySource')\
    .select(add(col('a'), col('b'))) \
    .insert_into('mySink')

t_env.execute("3-udf_add")
