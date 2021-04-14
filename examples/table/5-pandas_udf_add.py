from pyflink.table import DataTypes, EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import col
from pyflink.table.udf import udf


def pandas_udf_demo():
    # Init environment
    environment_settings = EnvironmentSettings.new_instance().use_blink_planner().in_batch_mode().build()
    t_env = TableEnvironment.create(environment_settings=environment_settings)
    t_env.get_config().get_configuration().set_string('parallelism.default', '1')

    # Define and register UDF
    add = udf(lambda i, j: i + j, [DataTypes.BIGINT(), DataTypes.BIGINT()], DataTypes.BIGINT(), udf_type="pandas")

    # Register Source
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

    # Register Sink
    t_env.execute_sql("""
            CREATE TABLE mySink (
              `sum` BIGINT
            ) WITH (
              'connector' = 'filesystem',
              'format' = 'csv',
              'path' = '/opt/examples/table/output/pandas_udf_add_output'
            )
        """)

    # Query
    t_env.from_path('mySource')\
        .select(add(col('a'), col('b'))) \
        .insert_into('mySink')

    t_env.execute("5-pandas_udf_add")


if __name__ == '__main__':
    pandas_udf_demo()
