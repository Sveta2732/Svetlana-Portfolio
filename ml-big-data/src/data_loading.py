from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType, DateType, TimestampType, BooleanType
from pyspark.sql import functions as F

def create_spark_session(app_name="FraudDetection", master="local[5]"):
    """
    Create a SparkSession and SparkContext with basic configuration.
    """
    spark_conf = SparkConf() \
        .setMaster(master) \
        .set("spark.sql.files.maxPartitionBytes", "16m") \
        .setAppName(app_name) \
        .set("spark.sql.session.timeZone", "Australia/Melbourne")

    spark = SparkSession.builder.config(conf=spark_conf).getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel('ERROR')
    return spark, sc


def load_dataframes(spark, data_path):
    """
    Load CSV files with predefined schemas into Spark DataFrames.
    Returns a dictionary of DataFrames.
    """

    # Schemas
    category_schema = StructType() \
        .add("category_id", StringType(), True) \
        .add("cat_level1", StringType(), True) \
        .add("cat_level2", StringType(), True) \
        .add("cat_level3", StringType(), True)

    customer_schema = StructType() \
        .add("customer_id", StringType(), True) \
        .add("first_name", StringType(), True) \
        .add("last_name", StringType(), True) \
        .add("username", StringType(), True) \
        .add("email", StringType(), True) \
        .add("gender", StringType(), True) \
        .add("birthdate", DateType(), True) \
        .add("first_join_date", DateType(), True)

    product_schema = StructType() \
        .add("id", StringType(), True) \
        .add("gender", StringType(), True) \
        .add("baseColour", StringType(), True) \
        .add("season", StringType(), True) \
        .add("year", StringType(), True) \
        .add("usage", StringType(), True) \
        .add("productDisplayName", StringType(), True) \
        .add("category_id", StringType(), True)

    browsing_behaviour_schema = StructType() \
        .add("session_id", StringType(), True) \
        .add("event_type", StringType(), True) \
        .add("event_time", TimestampType(), True) \
        .add("traffic_source", StringType(), True) \
        .add("device_type", StringType(), True)

    transaction_schema = StructType() \
        .add("created_at", TimestampType(), True) \
        .add("customer_id", StringType(), True) \
        .add("transaction_id", StringType(), True) \
        .add("session_id", StringType(), True) \
        .add("product_metadata", StringType(), True) \
        .add("payment_method", StringType(), True) \
        .add("payment_status", StringType(), True) \
        .add("promo_amount", DoubleType(), True) \
        .add("promo_code", StringType(), True) \
        .add("shipment_fee", DoubleType(), True) \
        .add("shipment_location_lat", DoubleType(), True) \
        .add("shipment_location_long", DoubleType(), True) \
        .add("total_amount", DoubleType(), True) \
        .add("clear_payment", StringType(), True)

    fraud_transaction_schema = StructType() \
        .add("transaction_id", StringType(), True) \
        .add("is_fraud", BooleanType(), True)

    # Load DataFrames
    category = spark.read.format('csv').option('header', True).schema(category_schema).load(f'{data_path}/category.csv')
    customer = spark.read.format('csv').option('header', True).schema(customer_schema).load(f'{data_path}/customer.csv')
    product = spark.read.format('csv').option('header', True).schema(product_schema).load(f'{data_path}/product.csv')
    transaction = spark.read.format('csv').option('header', True).schema(transaction_schema).load(f'{data_path}/transactions.csv')
    browsing_behaviour = spark.read.format('csv').option('header', True).schema(browsing_behaviour_schema).load(f'{data_path}/browsing_behaviour.csv')
    customer_session = spark.read.format('csv').option('header', True).load(f'{data_path}/customer_session.csv')
    fraud_transaction = spark.read.format('csv').option('header', True).schema(fraud_transaction_schema).load(f'{data_path}/fraud_transaction.csv')

    dfs = {
        "category": category,
        "customer": customer,
        "product": product,
        "transaction": transaction,
        "browsing_behaviour": browsing_behaviour,
        "customer_session": customer_session,
        "fraud_transaction": fraud_transaction
    }

    return dfs