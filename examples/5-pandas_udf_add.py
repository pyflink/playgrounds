from pyflink.table import DataTypes, EnvironmentSettings, BatchTableEnvironment
from pyflink.table.udf import udf

# Init environment
environment_settings = EnvironmentSettings.new_instance().use_blink_planner().in_batch_mode().build()
t_env = BatchTableEnvironment.create(environment_settings=environment_settings)
t_env._j_tenv.getPlanner().getExecEnv().setParallelism(1)

t_env.get_config().get_configuration().set_boolean('python.fn-execution.memory.managed', True)

# Define and register UDF
add = udf(lambda i, j: i + j, [DataTypes.BIGINT(), DataTypes.BIGINT()], DataTypes.BIGINT(), udf_type="pandas")
t_env.register_function("add", add)

# Register Source
t_env.execute_sql("""
        CREATE TABLE mySource (
          a BIGINT,
          b BIGINT
        ) WITH (
          'connector' = 'filesystem',
          'format' = 'csv',
          'path' = '/opt/examples/data/udf_add_input'
        )
    """)

# Register Sink
t_env.execute_sql("""
        CREATE TABLE mySink (
          `sum` BIGINT
        ) WITH (
          'connector' = 'filesystem',
          'format' = 'csv',
          'path' = '/opt/examples/data/pandas_udf_add_output'
        )
    """)

# Query
t_env.from_path('mySource')\
    .select("add(a, b)") \
    .insert_into('mySink')

t_env.execute("5-pandas_udf_add")
