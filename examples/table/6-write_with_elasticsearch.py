
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import StreamTableEnvironment, DataTypes, EnvironmentSettings
from pyflink.table.descriptors import Schema, Kafka, Json, Rowtime, Elasticsearch


def area_cnts():
    s_env = StreamExecutionEnvironment.get_execution_environment()
    s_env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
    s_env.set_parallelism(1)

    # use blink table planner
    st_env = StreamTableEnvironment \
        .create(s_env, environment_settings=EnvironmentSettings
                .new_instance()
                .in_streaming_mode()
                .use_blink_planner().build())

    # register source and sink
    register_rides_source(st_env)
    register_cnt_sink(st_env)

    # query
    st_env.from_path("source")\
        .group_by("taxiId")\
        .select("taxiId, count(1) as cnt")\
        .insert_into("sink")

    # execute
    st_env.execute("6-write_with_elasticsearch")


def register_rides_source(st_env):
    st_env \
        .connect(  # declare the external system to connect to
        Kafka()
            .version("universal")
            .topic("Rides")
            .start_from_earliest()
            .property("zookeeper.connect", "zookeeper:2181")
            .property("bootstrap.servers", "kafka:9092")) \
        .with_format(  # declare a format for this system
        Json()
            .fail_on_missing_field(True)
            .schema(DataTypes.ROW([
            DataTypes.FIELD("rideId", DataTypes.BIGINT()),
            DataTypes.FIELD("isStart", DataTypes.BOOLEAN()),
            DataTypes.FIELD("eventTime", DataTypes.TIMESTAMP()),
            DataTypes.FIELD("lon", DataTypes.FLOAT()),
            DataTypes.FIELD("lat", DataTypes.FLOAT()),
            DataTypes.FIELD("psgCnt", DataTypes.INT()),
            DataTypes.FIELD("taxiId", DataTypes.BIGINT())]))) \
        .with_schema(  # declare the schema of the table
        Schema()
            .field("rideId", DataTypes.BIGINT())
            .field("taxiId", DataTypes.BIGINT())
            .field("isStart", DataTypes.BOOLEAN())
            .field("lon", DataTypes.FLOAT())
            .field("lat", DataTypes.FLOAT())
            .field("psgCnt", DataTypes.INT())
            .field("rideTime", DataTypes.TIMESTAMP())
            .rowtime(
            Rowtime()
                .timestamps_from_field("eventTime")
                .watermarks_periodic_bounded(60000))) \
        .in_append_mode() \
        .register_table_source("source")


def register_cnt_sink(st_env):
    st_env.connect(
        Elasticsearch()
            .version("6")
            .host("elasticsearch", 9200, "http")
            .index("taxiid-cnts")
            .document_type('taxiidcnt')
            .key_delimiter("$")) \
        .with_schema(
            Schema()
                .field("taxiId", DataTypes.BIGINT())
                .field("cnt", DataTypes.BIGINT())) \
        .with_format(
           Json()
               .derive_schema()) \
        .in_upsert_mode() \
        .register_table_sink("sink")


if __name__ == '__main__':
    area_cnts()