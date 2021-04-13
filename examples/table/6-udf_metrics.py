from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import StreamTableEnvironment, DataTypes, EnvironmentSettings
from pyflink.table.descriptors import Schema, Kafka, Json
from pyflink.table.udf import ScalarFunction, udf


class MyAdd(ScalarFunction):

    def open(self, function_context):
        mg = function_context.get_metric_group()
        # register metrics
        self.counter = mg.add_group("aaa", "bbb").counter("my_counter")

    def eval(self, a, b):
        # invoke increase() for the counter
        self.counter.inc()
        return a + b


def python_udf_metric_demo():
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
    register_rides_sink(st_env)

    add = udf(MyAdd(), [DataTypes.BIGINT(), DataTypes.BIGINT()], DataTypes.BIGINT())
    st_env.register_function("add", add)

    # query
    st_env.from_path("source").select("add(rideId, taxiId)").insert_into("sink")

    # execute
    st_env.execute("6-udf_metrics")


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
            DataTypes.FIELD("eventTime", DataTypes.STRING()),
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
            .field("eventTime", DataTypes.STRING())) \
        .in_append_mode() \
        .create_temporary_table("source")


def register_rides_sink(st_env):
    st_env \
        .connect(  # declare the external system to connect to
        Kafka()
            .version("universal")
            .topic("TempResults")
            .property("zookeeper.connect", "zookeeper:2181")
            .property("bootstrap.servers", "kafka:9092")) \
        .with_format(  # declare a format for this system
        Json()
            .fail_on_missing_field(True)
            .schema(DataTypes.ROW([DataTypes.FIELD("sum_value", DataTypes.BIGINT())]))) \
        .with_schema(  # declare the schema of the table
        Schema().field("sum_value", DataTypes.BIGINT())) \
        .in_append_mode() \
        .create_temporary_table("sink")


if __name__ == '__main__':
    python_udf_metric_demo()
