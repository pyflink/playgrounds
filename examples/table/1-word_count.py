from pyflink.table import EnvironmentSettings, TableEnvironment

environment_settings = EnvironmentSettings.new_instance().use_blink_planner().in_batch_mode().build()
t_env = TableEnvironment.create(environment_settings=environment_settings)
t_env.get_config().get_configuration().set_string('parallelism.default', '1')

t_env.execute_sql("""
         CREATE TABLE mySource (
           word STRING
         ) WITH (
           'connector' = 'filesystem',
           'format' = 'csv',
           'path' = '/opt/examples/table/input/word_count_input'
         )
     """)

t_env.execute_sql("""
         CREATE TABLE mySink (
           word STRING,
           `count` BIGINT
         ) WITH (
           'connector' = 'filesystem',
           'format' = 'csv',
           'path' = '/opt/examples/table/output/word_count_output'
         )
     """)

t_env.from_path('mySource') \
    .group_by('word') \
    .select('word, count(1)') \
    .insert_into('mySink')

# Execute
t_env.execute("1-word_count")
