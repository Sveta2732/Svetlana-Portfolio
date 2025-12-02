from pyspark.sql import functions as F
from pyspark.sql.types import BooleanType, ArrayType, StructType, StructField, IntegerType

def create_features(transaction, browsing_behaviour, customer, fraud_transaction):
    # Merge transaction with browsing behaviour
    tran_brows_df = transaction.join(
        browsing_behaviour,
        transaction.session_id == browsing_behaviour.session_id,
        how='inner'
    )

    # Define event levels
    l1 = ['AP', 'ATC', 'CO']
    l2 = ['VC', 'VP', 'VI', 'SER']
    l3 = ['SCR', 'HP', 'CL']

    # Count events per level
    levels_df = tran_brows_df.groupBy('transaction_id').agg(
        F.sum(F.when(F.col('event_type').isin(l1), 1).otherwise(0)).alias('l1'),
        F.sum(F.when(F.col('event_type').isin(l2), 1).otherwise(0)).alias('l2'),
        F.sum(F.when(F.col('event_type').isin(l3), 1).otherwise(0)).alias('l3')
    )

    levels = levels_df.withColumn(
        "l1ratio", F.round(F.col('l1') / (F.col('l1') + F.col('l2') + F.col('l3')) * 100, 2)
    ).withColumn(
        "l2ratio", F.round(F.col('l2') / (F.col('l1') + F.col('l2') + F.col('l3')) * 100, 2)
    )

    # Browsing time
    browsing_time = browsing_behaviour.groupBy("session_id").agg(
        F.when(
            F.count("event_time") > 1,
            ((F.max("event_time").cast("long") + F.min("event_time").cast("long")) / 2).cast("timestamp")
        ).otherwise(F.max("event_time")).alias("average_event_time")
    )

    browsing_time = browsing_time.withColumn(
        'time_of_day',
        F.when((F.hour('average_event_time') >= 6) & (F.hour('average_event_time') < 12), 'morning')
         .when((F.hour('average_event_time') >= 12) & (F.hour('average_event_time') < 18), 'afternoon')
         .when((F.hour('average_event_time') >= 18) & (F.hour('average_event_time') < 24), 'evening')
         .otherwise('night')
    )

    # Customer info and age
    cust_trans = transaction.join(customer, 'customer_id', how='inner')\
                            .withColumn('age', F.floor(F.months_between(F.col('created_at'), F.col('birthdate')) / 12))\
                            .withColumn('first_join_year', F.year(F.col('first_join_date')))\
                            .select('customer_id', 'payment_status', 'transaction_id', 'session_id',
                                    'shipment_location_lat', 'shipment_location_long', 'gender', 'age', 'first_join_year')

    # Number of purchases
    cust_tran_pur = cust_trans.join(
        cust_trans.filter(F.col('payment_status') == 'Success')
        .groupBy('customer_id')
        .agg(F.count('*').alias('number_of_purchases')),
        'customer_id', how='left'
    )

    # Merge all features with fraud labels
    features = cust_tran_pur.join(levels, 'transaction_id', how='inner')\
                            .join(browsing_time, 'session_id', how='left')\
                            .join(fraud_transaction, 'transaction_id', how='left')
    
    # Result with original transactions column
    features_tr = features.withColumn('labels', F.when(F.col('is_fraud')== 'true', 1).otherwise(0))\
                          .drop('session_id', 'customer_id' , 'payment_status', 'average_event_time')\
                          .withColumnRenamed('shipment_location_lat', 'lat')\
                          .withColumnRenamed('shipment_location_long', 'long')\
                          .join(transaction, "transaction_id", how='left')\
                          .withColumn('is_fraud', F.when(F.col('is_fraud')== 'true', True).otherwise(False))\
                          .withColumn('created_year', F.year('created_at'))\
                          .drop('shipment_location_lat', 'shipment_location_long')
    features_df = features.withColumn('labels', F.when(F.col('is_fraud')== 'true', 1).otherwise(0))\
                      .drop('transaction_id','session_id', 'customer_id' , 'payment_status', 'average_event_time')\
                      .withColumnRenamed('shipment_location_lat', 'lat')\
                      .withColumn('is_fraud', F.when(F.col('is_fraud')== 'true', True).otherwise(False))\
                      .withColumnRenamed('shipment_location_long', 'long')
    
    

    features_df2 = features_df.withColumn("lat_grid", F.floor(F.col("lat") / 0.5) * 0.5) \
       .withColumn("long_grid", F.floor(F.col("long") / 0.5) * 0.5)    

    return features_df2, features_tr


def prepare_features_for_clustering(features, transaction, browsing_behaviour, customer, customer_session, fraud_transaction):

    # 1. Compute L3 ratio per session/transaction
    # L1/L2/L3 are categories of events in the session (e.g., different product page levels)

    features_tr3 = features.withColumn(
        "l3ratio", 
        F.round(F.col('l3') / (F.col('l1') + F.col('l2') + F.col('l3')) * 100, 2)
    )

    # 2. Compute time difference between L3 events in the session
    # If there are multiple L3 events, calculate difference in minutes; otherwise, set 0

    l1 = ['AP', 'ATC', 'CO']
    l2 = ['VC', 'VP', 'VI', 'SER']
    l3 = ['SCR', 'HP', 'CL']
    beh_time = browsing_behaviour.filter(F.col('event_type').isin(l3)) \
        .groupBy('session_id') \
        .agg(
            F.when(
                F.count("event_time") > 1,
                F.round((F.unix_timestamp(F.max("event_time")) - F.unix_timestamp(F.min("event_time"))) / 60, 2)
            ).otherwise(0).alias('several_l3_time')
        )
    tr_bah3 = features_tr3.join(beh_time, 'session_id', how='inner')

    # 3. Compute total L1/L2/L3 and their ratios per customer
    # Aggregates customer behavior across all sessions
    cust_levels = customer_session.join(browsing_behaviour, 'session_id', how='left') \
        .groupBy('customer_id').agg(
            F.sum(F.when(F.col('event_type').isin(l1), 1).otherwise(0)).alias('l1'),
            F.sum(F.when(F.col('event_type').isin(l2), 1).otherwise(0)).alias('l2'),
            F.sum(F.when(F.col('event_type').isin(l3), 1).otherwise(0)).alias('l3')
        ) \
        .withColumn("l1ratio", F.round(F.col('l1') / (F.col('l1') + F.col('l2') + F.col('l3')) * 100, 2)) \
        .withColumn("l2ratio", F.round(F.col('l2') / (F.col('l1') + F.col('l2') + F.col('l3')) * 100, 2)) \
        .withColumn("l3ratio", F.round(F.col('l3') / (F.col('l1') + F.col('l2') + F.col('l3')) * 100, 2))

    # 4. Compute average L1/L2/L3 per session for each customer

    cust_levels2 = customer_session.join(browsing_behaviour, 'session_id', how='left') \
        .groupBy('customer_id', 'session_id').agg(
            F.sum(F.when(F.col('event_type').isin(l1), 1).otherwise(0)).alias('l1'),
            F.sum(F.when(F.col('event_type').isin(l2), 1).otherwise(0)).alias('l2'),
            F.sum(F.when(F.col('event_type').isin(l3), 1).otherwise(0)).alias('l3')
        ) \
        .groupBy('customer_id').agg(
            F.round(F.sum('l1') / F.count('session_id'), 2).alias('av_l1'),
            F.round(F.sum('l2') / F.count('session_id'), 2).alias('av_l2'),
            F.round(F.sum('l3') / F.count('session_id'), 2).alias('av_l3')
        )

    # Merge total and average L-levels
    cust_levels = cust_levels.join(cust_levels2, 'customer_id', how='left')

    # 5. Average time difference between L3 events per customer
    cust_time = customer_session.join(browsing_behaviour, 'session_id', how='left') \
        .filter(F.col('event_type').isin(l3)) \
        .groupBy('customer_id', 'session_id') \
        .agg(
            F.when(
                F.count("event_time") > 1,
                F.round((F.unix_timestamp(F.max("event_time")) - F.unix_timestamp(F.min("event_time"))) / 60, 2)
            ).otherwise(0).alias('difl3min')
        ) \
        .groupBy('customer_id') \
        .agg(F.round(F.avg('difl3min'), 2).alias('difl3min'))

    cust_levelsn = cust_levels.join(cust_time, 'customer_id', how='left')

      # 6. Failed transactions per customer
    cust_tr = customer.join(transaction, 'customer_id', how='inner')
    cust_tr_status = cust_tr.groupBy('customer_id') \
        .agg(
            F.sum(F.when(F.col('payment_status') == 'Fail', 1).otherwise(0)).alias('fail_number'),
            F.round(
                (F.sum(F.when(F.col('payment_status') == 'Fail', 1).otherwise(0)) / F.count('*')), 2
            ).alias('fail_ratio')
        )
    cust_levelss = cust_levelsn.join(cust_tr_status, 'customer_id', how='inner')

    # 7. Price-based features per customer
    schema = ArrayType(StructType([
        StructField("product_id", IntegerType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("item_price", IntegerType(), True)
    ]))

    cust_tr_item = cust_tr.withColumn("product_metadata_array", F.from_json(F.col("product_metadata"), schema)) \
        .withColumn("product_metadata_exploded", F.explode(F.col("product_metadata_array"))) \
        .withColumn("product_id", F.col("product_metadata_exploded.product_id")) \
        .withColumn("quantity", F.col("product_metadata_exploded.quantity")) \
        .withColumn("item_price", F.col("product_metadata_exploded.item_price")) \
        .drop("product_metadata_array", "product_metadata_exploded")

    # Calculate quantiles for expensive/cheap categorization
    quantiles = cust_tr_item.approxQuantile("item_price", [0.25, 0.75], 0.01)
    q25, q75 = quantiles

    # Categorize items by price and aggregate per customer
    cust_tr_item_price = cust_tr_item.withColumn(
        "price_category",
        F.when(F.col("item_price") > q75, 'expensive')
         .when(F.col("item_price") < q25, 'cheap')
         .otherwise('middle')
    ).groupBy('customer_id').agg(
        F.sum(F.when(F.col('price_category') == 'expensive', 1).otherwise(0)).alias('c_expensive'),
        F.sum(F.when(F.col('price_category') == 'cheap', 1).otherwise(0)).alias('c_cheap'),
        F.sum(F.when(F.col('price_category') == 'middle', 1).otherwise(0)).alias('c_middle')
    ).withColumn(
        "cust_expensive%", F.round(F.col('c_expensive') / (F.col('c_expensive') + F.col('c_cheap') + F.col('c_middle')) * 100, 2)
    ).withColumn(
        "cust_cheap%", F.round(F.col('c_cheap') / (F.col('c_expensive') + F.col('c_cheap') + F.col('c_middle')) * 100, 2)
    )

    # Merge price features with customer-level data
    cast_level_price = cust_levelss.join(cust_tr_item_price, 'customer_id', how='inner')

    # 8. Price-based features per session
    beh_price = cust_tr_item.withColumn(
        "price_category",
        F.when(F.col("item_price") > q75, 'expensive')
         .when(F.col("item_price") < q25, 'cheap')
         .otherwise('middle')
    ).groupBy('session_id').agg(
        F.sum(F.when(F.col('price_category') == 'expensive', 1).otherwise(0)).alias('expensive'),
        F.sum(F.when(F.col('price_category') == 'cheap', 1).otherwise(0)).alias('cheap'),
        F.sum(F.when(F.col('price_category') == 'middle', 1).otherwise(0)).alias('middle')
    ).withColumn(
        "expensive_rat", F.round(F.col('expensive') / (F.col('expensive') + F.col('cheap') + F.col('middle')) * 100, 2)
    ).withColumn(
        "cheap_rat", F.round(F.col('cheap') / (F.col('expensive') + F.col('cheap') + F.col('middle')) * 100, 2)
    )

    beh_gen = tr_bah3.join(beh_price, 'session_id', how='inner')

    # 9. Shopping Cart behavior
    # Detect big ATC activity: added items vs distinct products
    browsing_behaviour_ATC = browsing_behaviour.filter(F.col('event_type') == 'ATC') \
        .groupBy('session_id').agg(F.count('event_type').alias('ATC'))

    beh_item = cust_tr_item.groupBy('session_id') \
        .agg(F.countDistinct('product_id').alias('distinct_product')) \
        .join(browsing_behaviour_ATC, 'session_id', how='inner') \
        .withColumn('bigATC', F.when(F.col('distinct_product') != F.col('ATC'), 'yes').otherwise('no')) \
        .drop('distinct_product', 'ATC')

    behaviour = beh_gen.join(beh_item, 'session_id', how='inner')

    # 10. Repeat purchases per day

    cust_tr_item = cust_tr_item.withColumn('day', F.to_date('created_at'))
    cust_frequ = cust_tr_item.groupBy('customer_id', 'day', 'product_id').count()
    freq_customer = cust_frequ.groupBy('customer_id').agg(F.max("count").alias("max_count")) \
        .withColumn("day_repeat", F.when(F.col("max_count") >= 2, "yes").otherwise("no")) \
        .drop("max_count")

    cust_day = cast_level_price.join(freq_customer, 'customer_id', how='inner')

    # 11. Fraud per customer

    
    cust_fraud = cust_tr.join(fraud_transaction, 'transaction_id', how='left') \
        .withColumn('fraud', F.when(F.col('is_fraud') == 'true', 1).otherwise(0)) \
        .groupBy('customer_id') \
        .agg(F.sum('fraud').alias('was_fraud'))

    # 12. Combine all customer features
    customer_final = cust_fraud.join(cust_day, 'customer_id', how='inner') \
        .drop('l1','l2','l3') \
        .withColumnRenamed('l1ratio', 'cust_l1ratio') \
        .withColumnRenamed('l2ratio', 'cust_l2ratio') \
        .withColumnRenamed('l3ratio', 'cust_l3ratio') \
        .orderBy(F.desc("was_fraud"))


    # 13. Add customer features
    
    behaviour_f = behaviour.join(customer_final, 'customer_id', how='left') \
        .withColumn('was_fraud', F.col('was_fraud') - F.col('labels'))

    
    # 14. Select final features for clustering

    
    features_knn = behaviour_f.select(
        'l3', 'l1ratio', 'l2ratio', 'l3ratio', 'several_l3_time',
        'expensive', 'cheap', 'expensive_rat', 'cheap_rat',
        'fail_number', 'fail_ratio','bigATC', 'was_fraud', 'is_fraud', 'labels'
    )

    return features_knn