#
# from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
# from pyflink.table import StreamTableEnvironment, EnvironmentSettings
# from pyflink.table.catalog import HiveCatalog
# from py4j.java_gateway import java_import
# from pyflink.java_gateway import get_gateway
#
#
#
# def from_kafka_to_kafka_demo():
#     s_env = StreamExecutionEnvironment.get_execution_environment()
#     s_env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
#     s_env.set_parallelism(1)
#
#     # use blink table planner
#     st_env = StreamTableEnvironment \
#         .create(s_env, environment_settings=EnvironmentSettings
#                 .new_instance()
#                 .in_streaming_mode()
#                 .use_blink_planner().build())
#
#     name = 'myhive'
#     default_database = 'default'
#     hive_conf_dir = '/usr/local/hive/conf'
#     hive_version = '2.3.4'
#     j_hive_catalog = get_gateway().jvm.org.apache.flink.table.catalog.hive.HiveCatalog(
#         name, default_database, hive_conf_dir, hive_version)
#     hive_catalog = HiveCatalog(j_hive_catalog=j_hive_catalog)
#     st_env.register_catalog("myhive", hive_catalog)
#     st_env.use_catalog("myhive")
#
#     # query
#     st_env.from_path("src").group_by("key").select("key, count(1) as cnt").insert_into("dest")
#
#     # execute
#     st_env.execute("8-hive_catalog")
#
#
# if __name__ == '__main__':
#     from_kafka_to_kafka_demo()