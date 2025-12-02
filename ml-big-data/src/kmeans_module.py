import pyspark.sql.functions as F
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
import pandas as pd
import matplotlib.pyplot as plt

def prepare_kmeans_features(df, exclude_cols=None, categorical_cols=None):
    """
    Prepare features for K-Means clustering.
    df: Spark DataFrame
    exclude_cols: columns to exclude from features
    categorical_cols: list of categorical columns to index/encode
    Returns: assembler inputs, indexer, encoder, assembler
    """
    if exclude_cols is None:
        exclude_cols = ['labels']
    if categorical_cols is None:
        categorical_cols = []

    # Index categorical columns
    outputCols = [f"{c}_index" for c in categorical_cols]
    indexer = StringIndexer(inputCols=categorical_cols, outputCols=outputCols)

    # One-hot encode
    outputCols_OHE = [f"{c}_vec" for c in categorical_cols]
    encoder = OneHotEncoder(inputCols=outputCols, outputCols=outputCols_OHE)

    # Numeric features
    numeric_cols = [c for c in df.columns if c not in exclude_cols + categorical_cols]
    assembler_inputs = outputCols_OHE + numeric_cols
    assembler = VectorAssembler(inputCols=assembler_inputs, outputCol="features_knn")

    return assembler_inputs, indexer, encoder, assembler

def train_kmeans(df, assembler_inputs, indexer, encoder, assembler, k=2):
    """
    Train K-Means clustering model and return predictions and pipeline.
    """
    scaler = StandardScaler(inputCol='features_knn', outputCol='scaledFeatures')
    kmeans = KMeans(featuresCol='scaledFeatures', k=k)
    pipeline = Pipeline(stages=[indexer, encoder, assembler, scaler, kmeans])
    model = pipeline.fit(df)
    predictions = model.transform(df)
    return predictions, model

def evaluate_kmeans(predictions, assembler_inputs, pipeline_model):
    """
    Evaluate K-Means clustering:
    - Compute silhouette score
    - Display cluster centers with feature names
    """
    # Silhouette score
    evaluator = ClusteringEvaluator(featuresCol='scaledFeatures', predictionCol='prediction')
    silhouette = evaluator.evaluate(predictions)
    print(f"Silhouette with squared euclidean distance = {silhouette:.4f}")

    # Cluster centers from trained K-Means model
    centers = pipeline_model.stages[-1].clusterCenters()
    print("Cluster Centers (raw arrays):")
    for center in centers:
        print(center)

    # Create a DataFrame for easier viewing
    centers_df = pd.DataFrame(centers, columns=assembler_inputs)
    print("\nCluster Centers (with feature names):")
    print(centers_df)

    # Show each cluster center with feature name and value
    for i, center in enumerate(centers):
        print(f"\nCluster {i} Center:")
        for name, value in zip(assembler_inputs, center):
            print(f"{name}: {value}")

    return silhouette, centers_df

def silhouette_vs_k(df, assembler_inputs, indexer, encoder, assembler, max_k=10):
    """
    Compute silhouette score for k=2..max_k and plot.
    """
    scaler = StandardScaler(inputCol='features_knn', outputCol='scaledFeatures')
    pipeline_b = Pipeline(stages=[indexer, encoder, assembler, scaler])
    pipelineModel_b = pipeline_b.fit(df)
    scaled_data = pipelineModel_b.transform(df)

    evaluator = ClusteringEvaluator(featuresCol='scaledFeatures', predictionCol='prediction')
    silhouette_arr = []
    for k in range(2, max_k):
        kmeans = KMeans(featuresCol='scaledFeatures', k=k)
        model = kmeans.fit(scaled_data)
        predictions = model.transform(scaled_data)
        silhouette = evaluator.evaluate(predictions)
        silhouette_arr.append(silhouette)
        print(f'k={k}, Silhouette Score={silhouette}')

    # Plot
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(range(2, max_k), silhouette_arr)
    ax.set_xlabel('Number of clusters (k)')
    ax.set_ylabel('Silhouette Score')
    plt.show()
    return silhouette_arr