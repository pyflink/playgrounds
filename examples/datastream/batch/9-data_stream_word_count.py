from pyflink.common import WatermarkStrategy, Row
from pyflink.common.serialization import Encoder
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FileSource, StreamFormat, FileSink, OutputFileConfig
from pyflink.datastream.execution_mode import RuntimeExecutionMode


def data_stream_word_count_demo():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    env.set_runtime_mode(RuntimeExecutionMode.BATCH)

    input_path = '/opt/examples/datastream/input/word_count_input'
    output_path = '/opt/examples/datastream/output/data_stream_word_count'

    file_source = FileSource\
        .for_record_stream_format(
            StreamFormat.text_line_format(),
            input_path) \
        .process_static_file_set() \
        .build()

    file_sink = FileSink \
        .for_row_format(output_path, Encoder.simple_string_encoder()) \
        .with_output_file_config(OutputFileConfig.builder().with_part_prefix('pre').with_part_suffix('suf').build()) \
        .build()

    ds = env.from_source(
        source=file_source,
        watermark_strategy=WatermarkStrategy.for_monotonous_timestamps(),
        source_name='file_source',
        type_info=Types.STRING())

    ds.map(lambda a: Row(a, 1), output_type=Types.ROW([Types.STRING(), Types.INT()])) \
        .key_by(lambda a: a[0]) \
        .reduce(lambda a, b: Row(a[0], a[1] + b[1])) \
        .sink_to(file_sink)

    env.execute('9-data_stream_word_count')


if __name__ == '__main__':
    data_stream_word_count_demo()
