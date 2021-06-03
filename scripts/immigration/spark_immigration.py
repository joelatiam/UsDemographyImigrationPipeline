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
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.2.0")\
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
    immigration_data = os.path.join(input_data, "immigration/parquet/*.parquet")  

    df = spark.read.parquet(immigration_data)

    udf_datetime_from_sas = udf(lambda x: convert_datetime(x), Date())

    udf_arrival_mode = udf(lambda x: get_arrival_mode(x), Str())

    df = df.select(
        col("i94yr").alias("year").cast(Short()),
        col("i94mon").alias("month").cast(Short()),
        udf_datetime_from_sas("arrdate").alias("arrival_date"),
        udf_arrival_mode("i94mode").alias("arrival_mode"),
        col("i94visa").alias("visa_type").cast(Short()),
        col("biryear").alias("birth_year").cast(Short()),
        col("gender").cast(Str()),
        col("i94Addr").alias("residential_state").cast(Str())
    )

    df = df.withColumn("year", year("arrival_date"))\
        .withColumn("month", month("arrival_date"))



    print(df.sort(df.month.desc()).show(5))
    print(df.count())

def main():
    spark = create_spark_session()
    input_data = 'dags/data/raw'
    output_data = ''
    print('heeeeeeeeee')
    
    # process_immigration_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
