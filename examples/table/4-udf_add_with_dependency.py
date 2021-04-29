from pyflink.table import DataTypes, EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import col
from pyflink.table.udf import udf

env_settings = EnvironmentSettings.new_instance().in_streaming_mode().use_blink_planner().build()
t_env = TableEnvironment.create(environment_settings=env_settings)
t_env.get_config().get_configuration().set_string('parallelism.default', '1')


@udf(input_types=[DataTypes.BIGINT(), DataTypes.BIGINT()], result_type=DataTypes.BIGINT())
def add(i, j):
    from mpmath import fadd # add third-party dependency
    return int(fadd(1, 2))


t_env.set_python_requirements("/opt/examples/table/input/requirements.txt")

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
          'path' = '/opt/examples/table/output/udf_add_with_dependency_output'
        )
    """)

t_env.from_path('mySource')\
    .select(add(col('a'), col('b'))) \
    .insert_into('mySink')

t_env.execute("4-udf_add_with_dependency")
