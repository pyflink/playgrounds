from pyflink.common import WatermarkStrategy, Row
from pyflink.common.serialization import Encoder
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FileSink, OutputFileConfig, NumberSequenceSource
from pyflink.datastream.execution_mode import RuntimeExecutionMode
from pyflink.datastream.functions import KeyedProcessFunction, RuntimeContext
from pyflink.datastream.state import MapStateDescriptor


class MyKeyedProcessFunction(KeyedProcessFunction):

    def open(self, runtime_context: RuntimeContext):
        state_desc = MapStateDescriptor('map', Types.LONG(), Types.LONG())
        self.state = runtime_context.get_map_state(state_desc)

    def process_element(self, value, ctx: 'KeyedProcessFunction.Context'):
        if not self.state.contains(value[0]):
            result = value[1]
            self.state.put(value[0], result)
        else:
            existing = self.state.get(value[0])
            if existing <= 10:
                result = value[1] + existing
                self.state.put(value[0], result)
            else:
                result = existing
        yield result


def data_stream_process_function_demo():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(2)
    env.set_runtime_mode(RuntimeExecutionMode.BATCH)

    seq_num_source = NumberSequenceSource(1, 1000)

    output_path = '/opt/examples/datastream/output/data_stream_process_function_demo'
    file_sink = FileSink \
        .for_row_format(output_path, Encoder.simple_string_encoder()) \
        .with_output_file_config(OutputFileConfig.builder().with_part_prefix('pre').with_part_suffix('suf').build()) \
        .build()

    ds = env.from_source(
        source=seq_num_source,
        watermark_strategy=WatermarkStrategy.for_monotonous_timestamps(),
        source_name='seq_num_source',
        type_info=Types.LONG())

    ds.map(lambda a: Row(a % 4, 1), output_type=Types.ROW([Types.LONG(), Types.LONG()])) \
        .key_by(lambda a: a[0]) \
        .map(lambda a: (a[0], a[1] + 1)) \
        .key_by(lambda a: a[0]) \
        .reduce(lambda a, b: (a[0], a[1] + b[1])) \
        .key_by(lambda a: a[0]) \
        .process(MyKeyedProcessFunction(), Types.LONG()) \
        .filter(lambda i: i <= 10) \
        .sink_to(file_sink)

    env.execute('10-data_stream_process_function')


if __name__ == '__main__':
    data_stream_process_function_demo()
