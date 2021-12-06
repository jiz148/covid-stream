import time

from pyspark.sql import SparkSession

spark = SparkSession.builder.\
    master("local").\
    appName("PySpark_MySQL_test").\
    config("spark.executor.memory", "14G").\
    config("spark.driver.memory", "14G").\
    getOrCreate()

dataframe_mysql = spark.read.format("jdbc").options(
    url="jdbc:mysql://localhost:3306/covid_19",
    driver="com.mysql.cj.jdbc.Driver",
    dbtable="cases",
    user="root",
    password="oookkk").load()

if __name__ == "__main__":

    tic = time.perf_counter()
    dataframe_mysql.registerTempTable('cases')
    spark.sql("""select case_month, count(*) as count from c_19_cases group by case_month""").show()
    toc = time.perf_counter()
    print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")
