from pyflink.table import DataTypes
from pyflink.table.udf import udf


@udf(input_types=[DataTypes.BIGINT()], result_type=DataTypes.BIGINT())
def add_one(i):
    return i + 1

