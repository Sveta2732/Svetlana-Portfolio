from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier, GBTClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
import pyspark.sql.functions as F
import numpy as np
import matplotlib.pyplot as plt

def prepare_features_for_ml(features_df):
    """
    Prepare numeric and categorical columns for ML pipelines.
    Returns: numeric columns, categorical columns
    """
    numeric_cols = features_df.drop('gender','time_of_day','is_fraud','lat','long','first_join_year','age','long_grid').columns
    categorical_cols = ['time_of_day']
    return numeric_cols, categorical_cols

def create_pipelines(numeric_cols, categorical_cols):
    """
    Create Spark ML pipelines for RandomForest and GBT models.
    Returns: pipeline_rf, pipeline_gbt
    """
    numeric_cols = [x for x in numeric_cols if x!='labels']
    # Indexing categorical columns
    indexer = StringIndexer(inputCols=categorical_cols, outputCols=[f'{x}_index' for x in categorical_cols])
    
    # One-hot encoding
    encoder = OneHotEncoder(inputCols=[f'{x}_index' for x in categorical_cols],
                            outputCols=[f'{x}_vec' for x in categorical_cols])
    
    # Vector assembler
    assembler_inputs = [f'{x}_vec' for x in categorical_cols] + numeric_cols
    assembler = VectorAssembler(inputCols=assembler_inputs, outputCol='features')
    
    # Classifiers
    rf = RandomForestClassifier(labelCol='labels', featuresCol='features', numTrees=10)
    gbt = GBTClassifier(labelCol='labels', featuresCol='features')
    
    # Pipelines
    pipeline_rf = Pipeline(stages=[indexer, encoder, assembler, rf])
    pipeline_gbt = Pipeline(stages=[indexer, encoder, assembler, gbt])
    
    return pipeline_rf, pipeline_gbt

def train_and_evaluate(train_df, test_df, pipeline_rf, pipeline_gbt):
    """
    Train models and evaluate using Spark ML metrics and ROC curve.
    Saves best model to filesystem.
    """
    # Train
    model_rf = pipeline_rf.fit(train_df)
    model_gbt = pipeline_gbt.fit(train_df)
    
    # Predict
    predictions_rf = model_rf.transform(test_df)
    predictions_gbt = model_gbt.transform(test_df)
    
    # Evaluate AUC (optional quick check)
    evaluator = BinaryClassificationEvaluator(labelCol='labels', rawPredictionCol='rawPrediction')
    auc_rf = evaluator.evaluate(predictions_rf)
    auc_gbt = evaluator.evaluate(predictions_gbt)
    print(f"Quick AUC check - RF: {auc_rf:.4f}, GBT: {auc_gbt:.4f}")

    # Save the best model (GBT assumed best)
    model_gbt.write().overwrite().save('fraud_prediction_model')

    return predictions_rf, predictions_gbt

def compute_metrics(predictions, prediction_name):
    """
    Compute TP, TN, FP, FN, accuracy, precision, recall, F1 for predictions.
    """
    TN = predictions.filter('prediction = 0 AND labels = prediction').count()
    TP = predictions.filter('prediction = 1 AND labels = prediction').count()
    FN = predictions.filter('prediction = 0 AND labels <> prediction').count()
    FP = predictions.filter('prediction = 1 AND labels <> prediction').count()

    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP) if TP + FP > 0 else 0
    recall = TP / (TP + FN) if TP + FN > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

    print(f'\nFor {prediction_name}:')
    predictions.groupBy('labels', 'prediction').count().show()
    print(f"TN: {TN}, TP: {TP}, FN: {FN}, FP: {FP}")
    print(f"Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1: {f1}")
    
    return accuracy, precision, recall, f1

def plot_roc_curve(predictions, model_name="Model"):
    """
    Plot ROC curve for a given predictions DataFrame with 'labels' and probability column.
    Assumes 'probability' column exists with [negative_prob, positive_prob].
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import pyspark.sql.functions as F
    import pyspark.sql.types as T

    # Convert probability vector to two separate columns
    to_array = F.udf(lambda v: v.toArray().tolist(), T.ArrayType(T.FloatType()))
    prob_df = predictions.withColumn('probability', to_array('probability'))
    prob_df = prob_df.select(prob_df.probability[0].alias('negative_prob'),
                             prob_df.probability[1].alias('positive_prob'),
                             'labels')

    # Function to compute confusion matrix
    def confusion_matrix(pred_df):
        TN = pred_df.filter('prediction = 0 AND labels = 0').count()
        TP = pred_df.filter('prediction = 1 AND labels = 1').count()
        FN = pred_df.filter('prediction = 0 AND labels = 1').count()
        FP = pred_df.filter('prediction = 1 AND labels = 0').count()
        return TP, TN, FP, FN

    # Compute TPR and FPR for multiple thresholds
    roc_values = []
    for threshold in np.linspace(0, 1, 100):
        prob_df = prob_df.withColumn('prediction', F.when(prob_df.positive_prob > threshold, 1).otherwise(0))
        tp, tn, fp, fn = confusion_matrix(prob_df)
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        roc_values.append([tpr, fpr])

    tpr_values, fpr_values = zip(*roc_values)

    # Plot
    plt.figure(figsize=(10, 7))
    plt.plot(fpr_values, tpr_values, label=f'ROC Curve ({model_name})', color='coral')
    plt.plot(np.linspace(0,1,100), np.linspace(0,1,100), linestyle='--', label='Baseline', color='lightblue')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve for {model_name}')
    plt.legend()
    plt.show()
