from pyflink.common import WatermarkStrategy, Row
from pyflink.common.serialization import Encoder
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FileSink, OutputFileConfig, NumberSequenceSource
from pyflink.datastream.execution_mode import RuntimeExecutionMode


def batch_seq_num_test():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(2)
    env.set_runtime_mode(RuntimeExecutionMode.BATCH)

    seq_num_source = NumberSequenceSource(1, 1000)

    output_path = '/opt/examples/output/batch_seq_num'
    file_sink = FileSink \
        .for_row_format(output_path, Encoder.simple_string_encoder()) \
        .with_output_file_config(OutputFileConfig.builder().with_part_prefix('pre').with_part_suffix('suf').build()) \
        .build()

    ds = env.from_source(
        source=seq_num_source,
        watermark_strategy=WatermarkStrategy.for_monotonous_timestamps(),
        source_name='file_source',
        type_info=Types.LONG())

    ds.map(lambda a: Row(a % 4, 1), output_type=Types.ROW([Types.LONG(), Types.LONG()])) \
        .key_by(lambda a: a[0]) \
        .reduce(lambda a, b: Row(a[0], a[1] + b[1])) \
        .sink_to(file_sink)

    env.execute('9-data_stream_batch_seq_num')


if __name__ == '__main__':
    batch_seq_num_test()
