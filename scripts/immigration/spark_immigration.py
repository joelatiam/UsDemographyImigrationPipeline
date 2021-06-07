import os
from datetime import datetime, timedelta

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear,\
    date_format, monotonically_increasing_id
from pyspark.sql.types import StructType as R, StructField as Fld, DoubleType as Dbl,\
    StringType as Str, IntegerType as Int, LongType as Long, ShortType as Short,\
    DateType as Date


def create_spark_session():
    spark = SparkSession \
        .builder \
        .getOrCreate()

    return spark


def get_arrival_mode(x):
    try:

        arrival_mode = int(x)
        if arrival_mode == 1:
            return 'Air'
        elif arrival_mode == 2:
            return 'Sea'
        elif arrival_mode == 3:
            return 'Land'
        else:
            return 'Not reported'

    except:
        return None


def convert_datetime(x):
    try:
        start = datetime(1960, 1, 1)
        return start + timedelta(days=int(x))
    except:
        return None


def process_immigration_data(spark, input_data, output_data):

    # filepath to song data file
    immigration_data = os.path.join(
        input_data, "immigration/parquet/*.parquet")

    destination_directory_path = os.path.join(
        output_data, "immigration")

    df = spark.read.parquet(immigration_data)

    udf_datetime_from_sas = udf(lambda x: convert_datetime(x), Date())

    udf_arrival_mode = udf(lambda x: get_arrival_mode(x), Str())

    df = df.select(
        udf_datetime_from_sas("arrdate").alias("arrival_date"),
        udf_arrival_mode("i94mode").alias("arrival_mode"),
        col("i94visa").alias("visa_type").cast(Short()),
        col("biryear").alias("birth_year").cast(Short()),
        col("gender").cast(Str()),
        col("i94Addr").alias("residential_state").cast(Str())
    )

    df.write.mode("overwrite")\
        .parquet(destination_directory_path)


def main():
    spark = create_spark_session()
    input_data = 'data/raw'
    output_data = 'data/cleaned'

    process_immigration_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
