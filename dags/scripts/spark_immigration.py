import os
from datetime import datetime
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
        .config("spark.jars.packages","saurfang:spark-sas7bdat:3.0.0-s_2.12")\
        .getOrCreate()
    return spark

def process_immigration_data(spark, input_data, output_data):

    # filepath to song data file
    immigration_data = os.path.join(input_data, "immigration/*/*/*.sas7bdat")

    songDataSchema =  R([
        Fld("i94yr",Short()),
        Fld("i94mon",Short()),
        Fld("arrdate",Short()),
        Fld("i94mode",Short()),
        Fld("airline",Str()),
        Fld("biryear",Short()),
        Fld("gender",Str()),
        Fld("i94Addr",Str()),
        Fld("i94visa",Short()),
        Fld("occup",Str()),
    ])
    
    df = spark.read\
        .format('com.github.saurfang.sas.spark')\
            .load(
                immigration_data,
                # schema=songDataSchema,
                forceLowercaseNames=True,
                inferLong=True
                )

def main():
    spark = create_spark_session()
    input_data = 'dag/data/'
    output_data = ''
    
    process_immigration_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
