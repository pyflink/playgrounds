from pyflink.table import EnvironmentSettings, BatchTableEnvironment

# Init environment
environment_settings = EnvironmentSettings.new_instance().use_blink_planner().in_batch_mode().build()
t_env = BatchTableEnvironment.create(environment_settings=environment_settings)
t_env._j_tenv.getPlanner().getExecEnv().setParallelism(1)

# Register Source
t_env.execute_sql("""
        CREATE TABLE mySource (
          word STRING
        ) WITH (
          'connector' = 'filesystem',
          'format' = 'csv',
          'path' = '/opt/examples/data/word_count_input'
        )
    """)

# Register Sink
t_env.execute_sql("""
        CREATE TABLE mySink (
          word STRING,
          `count` BIGINT
        ) WITH (
          'connector' = 'filesystem',
          'format' = 'csv',
          'path' = '/opt/examples/data/word_count_output'
        )
    """)

# Query
t_env.from_path('mySource') \
    .group_by('word') \
    .select('word, count(1)') \
    .insert_into('mySink')

# Execute
t_env.execute("1-word_count")
