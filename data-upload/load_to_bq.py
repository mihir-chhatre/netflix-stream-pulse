# import json
# from kafka import KafkaConsumer
# import pandas as pd
# import psycopg2
# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, to_date, hour, minute, second
# from google.cloud import bigquery

# # Kafka configuration
# kafka_nodes = "kafka:9092"
# completionTopic = "completion-event"

# # PostgreSQL configuration
# postgres_host = "postgres"
# postgres_port = "5432"
# postgres_db = "postgres"
# postgres_user = "postgres"
# postgres_password = "postgres"

# # BigQuery configuration
# bigquery_project = "netflix-stream-pulse"
# bigquery_dataset = "real_time_analytics"
# bigquery_table_1 = "viewsByGenderAgeGroup"
# bigquery_table_2 = "viewsByDeviceGenre"
# bigquery_table_3 = "viewsByLocationMR"

# # Initialize Spark session
# spark = SparkSession.builder \
#     .appName("TransformedDataToBQ") \
#     .getOrCreate()

# # Initialize BigQuery client
# client = bigquery.Client()

# def pandas_to_spark(pandas_df):
#     return spark.createDataFrame(pandas_df)

# def transform_dataframe(df):
#     return df.withColumn("date", to_date(col("window_end_utctime"))) \
#              .withColumn("hour", hour(col("window_end_utctime"))) \
#              .withColumn("min", minute(col("window_end_utctime"))) \
#              .drop("window_end_utctime")  # Drop the column

# def load_data_to_bigquery():
#     # Connect to PostgreSQL
#     conn = psycopg2.connect(
#         host=postgres_host,
#         port=postgres_port,
#         dbname=postgres_db,
#         user=postgres_user,
#         password=postgres_password
#     )

#     # Read data using Pandas
#     pandas_df1 = pd.read_sql("SELECT * FROM viewsByGenderAgeGroupAggregation", conn)
#     pandas_df2 = pd.read_sql("SELECT * FROM viewsByDeviceGenreAggregation", conn)
#     pandas_df3 = pd.read_sql("SELECT * FROM viewsByLocationMRAggregation", conn)

#     # Close the PostgreSQL connection
#     conn.close()

#     # Convert Pandas DataFrames to Spark DataFrames
#     df1 = pandas_to_spark(pandas_df1)
#     df2 = pandas_to_spark(pandas_df2)
#     df3 = pandas_to_spark(pandas_df3)

#     # Transform DataFrames
#     df1_transformed = transform_dataframe(df1)
#     df2_transformed = transform_dataframe(df2)
#     df3_transformed = transform_dataframe(df3)

#     # Convert back to Pandas DataFrames for BigQuery upload
#     df1_pandas = df1_transformed.toPandas()
#     df2_pandas = df2_transformed.toPandas()
#     df3_pandas = df3_transformed.toPandas()

#     # Load DataFrame1 to BigQuery
#     table_id1 = f"{bigquery_project}.{bigquery_dataset}.{bigquery_table_1}"
#     job1 = client.load_table_from_dataframe(df1_pandas, table_id1)
#     job1.result()  # Wait for the job to complete

#     # Load DataFrame2 to BigQuery
#     table_id2 = f"{bigquery_project}.{bigquery_dataset}.{bigquery_table_2}"
#     job2 = client.load_table_from_dataframe(df2_pandas, table_id2)
#     job2.result()  # Wait for the job to complete

#     # Load DataFrame3 to BigQuery
#     table_id3 = f"{bigquery_project}.{bigquery_dataset}.{bigquery_table_3}"
#     job3 = client.load_table_from_dataframe(df3_pandas, table_id3)
#     job3.result()  # Wait for the job to complete

#     print("\n*** Data loaded to BigQuery ***")

# def listen_for_completion_message():
#     consumer = KafkaConsumer(
#         completionTopic,
#         bootstrap_servers=kafka_nodes,
#         auto_offset_reset='earliest',
#         group_id='my-group',
#         value_deserializer=lambda x: json.loads(x.decode('utf-8'))
#     )

#     for message in consumer:
#         if message.value.get('status') == 'complete':
#             print("Completion message received, loading data to BigQuery...")
#             load_data_to_bigquery()
#             break

# if __name__ == "__main__":
#     listen_for_completion_message()









import json
from kafka import KafkaConsumer
import pandas as pd
import psycopg2
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, hour, minute, cast, StringType
from google.cloud import bigquery

# Kafka configuration
kafka_nodes = "kafka:9092"
completionTopic = "completion-event"

# PostgreSQL configuration
postgres_host = "postgres"
postgres_port = "5432"
postgres_db = "postgres"
postgres_user = "postgres"
postgres_password = "postgres"

# BigQuery configuration
bigquery_project = "netflix-stream-pulse"
bigquery_dataset = "real_time_analytics"
bigquery_table_1 = "viewsByDeviceGenre"
bigquery_table_2 = "viewsByGenderAgeGroup"
bigquery_table_3 = "viewsByLocationMR"

# Initialize Spark session
spark = SparkSession.builder \
    .appName("TransformedDataToBQ") \
    .getOrCreate()

# Initialize BigQuery client
client = bigquery.Client()

def pandas_to_spark(pandas_df):
    return spark.createDataFrame(pandas_df)

def transform_dataframe(df, table_name):
    df_transformed = df.withColumn("date", to_date(col("window_end_utctime"))) \
                       .withColumn("hour", hour(col("window_end_utctime")).cast(StringType())) \
                       .withColumn("min", minute(col("window_end_utctime")).cast(StringType())) \
                       .drop("window_end_utctime")  # Drop the column

    if table_name == "viewsByDeviceGenre":
        return df_transformed.select("device_type", "genre", "view_count", "date", "hour", "min")
    elif table_name == "viewsByGenderAgeGroup":
        return df_transformed.select("gender", "age_group", "view_count", "date", "hour", "min")
    elif table_name == "viewsByLocationMR":
        return df_transformed.select("country", "maturity_rating", "view_count", "date", "hour", "min")

def create_bq_table_with_sql(table_id, schema_query):
    query = f"CREATE TABLE IF NOT EXISTS {table_id} {schema_query}"
    query_job = client.query(query)  # Starts the query
    query_job.result()  # Waits for the query to finish

def load_data_to_bigquery():
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=postgres_host,
        port=postgres_port,
        dbname=postgres_db,
        user=postgres_user,
        password=postgres_password
    )

    # Read data using Pandas
    pandas_df1 = pd.read_sql("SELECT * FROM viewsByDeviceGenreAggregation", conn)
    pandas_df2 = pd.read_sql("SELECT * FROM viewsByGenderAgeGroupAggregation", conn)
    pandas_df3 = pd.read_sql("SELECT * FROM viewsByLocationMRAggregation", conn)

    # Close the PostgreSQL connection
    conn.close()

    # Convert Pandas DataFrames to Spark DataFrames
    df1 = pandas_to_spark(pandas_df1)
    df2 = pandas_to_spark(pandas_df2)
    df3 = pandas_to_spark(pandas_df3)

    # Transform DataFrames
    df1_transformed = transform_dataframe(df1, "viewsByDeviceGenre")
    df2_transformed = transform_dataframe(df2, "viewsByGenderAgeGroup")
    df3_transformed = transform_dataframe(df3, "viewsByLocationMR")

    # Define the schema for each BigQuery table
    # Define the SQL schema and table creation queries for each BigQuery table
    schema_query1 = """
    (device_type STRING, genre STRING, view_count INTEGER, date DATE, hour STRING, min STRING)
    PARTITION BY date
    CLUSTER BY hour, min
    """
    schema_query2 = """
    (gender STRING, age_group STRING, view_count INTEGER, date DATE, hour STRING, min STRING)
    PARTITION BY date
    CLUSTER BY hour, min
    """
    schema_query3 = """
    (country STRING, maturity_rating STRING, view_count INTEGER, date DATE, hour STRING, min STRING)
    PARTITION BY date
    CLUSTER BY hour, min
    """

    # Create BigQuery tables using the SQL queries
    create_bq_table_with_sql(f"{bigquery_project}.{bigquery_dataset}.{bigquery_table_1}", schema_query1)
    create_bq_table_with_sql(f"{bigquery_project}.{bigquery_dataset}.{bigquery_table_2}", schema_query2)
    create_bq_table_with_sql(f"{bigquery_project}.{bigquery_dataset}.{bigquery_table_3}", schema_query3)


    # Convert back to Pandas DataFrames for BigQuery upload
    df1_pandas = df1_transformed.toPandas()
    df2_pandas = df2_transformed.toPandas()
    df3_pandas = df3_transformed.toPandas()

    # Load DataFrame1 to BigQuery
    table_id1 = f"{bigquery_project}.{bigquery_dataset}.{bigquery_table_1}"
    job1 = client.load_table_from_dataframe(df1_pandas, table_id1)
    job1.result()  # Wait for the job to complete

    # Load DataFrame2 to BigQuery
    table_id2 = f"{bigquery_project}.{bigquery_dataset}.{bigquery_table_2}"
    job2 = client.load_table_from_dataframe(df2_pandas, table_id2)
    job2.result()  # Wait for the job to complete

    # Load DataFrame3 to BigQuery
    table_id3 = f"{bigquery_project}.{bigquery_dataset}.{bigquery_table_3}"
    job3 = client.load_table_from_dataframe(df3_pandas, table_id3)
    job3.result()  # Wait for the job to complete

    print("\n*** Data loaded to BigQuery ***")

def listen_for_completion_message():
    consumer = KafkaConsumer(
        completionTopic,
        bootstrap_servers=kafka_nodes,
        auto_offset_reset='earliest',
        group_id='my-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        if message.value.get('status') == 'complete':
            print("Completion message received, loading data to BigQuery...")
            load_data_to_bigquery()
            break

if __name__ == "__main__":
    listen_for_completion_message()
