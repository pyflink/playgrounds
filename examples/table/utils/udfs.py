from pyflink.table import DataTypes
from pyflink.table.udf import udf


@udf(result_type=DataTypes.BIGINT())
def add_one(i):
    return i + 1
