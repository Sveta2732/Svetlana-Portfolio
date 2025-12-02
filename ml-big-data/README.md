# eCommerce Fraud Detection with Big Data (PySpark MLlib) 💳⚡

## TL;DR
PySpark-based project for detecting Card-Not-Present (CNP) fraud using large-scale eCommerce data. Covers the full big data workflow including feature engineering, Spark ML pipelines, model training and evaluation, and clustering—showcasing practical experience with Spark and applied machine learning at scale.

---

## Project Overview
Fraudulent transactions threaten revenue and customer trust in online retail. This project uses historical transactions and browsing data to build predictive models and explore customer behavior via unsupervised learning.

**Objectives:**
- **Feature Engineering & Big Data Handling:** Process millions of records efficiently using PySpark DataFrames.
- **Fraud Prediction:** Classify transactions as fraudulent or genuine.
- **Behavioral Clustering:** Identify patterns of fraudulent users with K-Means.
---

## Technical Stack
- **Big Data:** PySpark 3.5, Spark MLlib  
- **ML Models:** Random Forest, Gradient Boosted Tree, K-Means  
- **Visualization:** matplotlib
- **Environment:** Python 3+, Jupyter Notebook, Docker  

---

## Data Overview
Datasets (CSV, millions of rows):
- `category.csv` – Product categories  
- `customer.csv` – Customer demographics  
- `product.csv` – Product details  
- `transaction.csv` – Sales transactions  
- `browsing_behaviour.csv` – Browsing events  
- `customer_session.csv` – Session-to-customer mapping  
- `fraud_transaction.csv` – Known fraudulent transactions  



---

## Methods & Actions
1. **Data Loading & Transformation**
   - Created a SparkSession with optimized configuration for big data processing.  
   - Defined schemas for all datasets to enforce correct data types and enable efficient loading.  
   - Aggregated browsing events into three levels (L1, L2, L3) and derived ratios to capture user intent.  
   - Extracted session-level features such as time-of-day, customer demographics, purchase counts, and fraud labels. 

2. **Exploratory Data Analysis**
      - Generated statistics for numeric, categorical, and boolean columns.  
   - Created visualisations to understand feature relationships with fraud labels.  
   - Identified features with high predictive power (e.g., L1/L2 ratios, number of failed payments). 

3. **Feature Engineering & ML Pipeline**
   - Spark ML Pipelines with transformers and estimators.
   - Models trained: **Random Forest (RF)** & **Gradient Boosted Tree (GBT)**.
   - Metrics:
     - RF: Accuracy 0.998, Precision 1.0, Recall 0.859  
     - GBT: Accuracy 0.9996, Precision 0.978, Recall 1.0 (selected final model)

4. **Customer Clustering (K-Means)**
   - Unsupervised analysis of user behavior.
   - Identified common fraud patterns.


---

## Project Structure
```text
fraud_detection_project/
│
├── src/                     # Main project code
│   ├── __init__.py          # Marks the folder as a Python package
│   ├── data_loading.py      # Load and preprocess CSV data using PySpark
│   ├── feature_engineering.py # Create and transform features for ML models
│   ├── model_training.py    # Build, train, and evaluate ML models (Random Forest, GBT)
│   └── kmeans_module.py     # Perform user clustering using K-Means
│
├── notebooks/               # Jupyter notebooks for analysis and experimentation
│   └── ml_bigdata.ipynb     # Main notebook: EDA, feature engineering, model training, visualizations
│
├── data/                    # Raw CSV datasets
│
├── requirements.txt         
└── README.md                

```

## How to Run
1. **Clone the repository**  
```bash
git clone https://github.com/Sveta2732/Svetlana-Portfolio.git
cd Svetlana-Portfolio/ml-big-data
```
2. **Install dependencies**

It is recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```
3. **Open the Jupyter Notebook**
```bash
jupyter notebook notebooks/ml_bigdata.ipynb
```
> **Note:** The notebook is configured for PySpark. Model training may take several minutes depending on dataset size and system resources.  
> For GitHub, only sample datasets  with 10,000 rows are included for demonstration.



---

## Key Learnings

* Practical experience with big data pipelines in PySpark for real-world ML applications.
* Built highly accurate ML models for fraud detection at scale (GBT: AUC 1.0). 

* Reinforced best practices in ML pipeline creation, model evaluation, and reproducibility in a big data context. 

* Explored unsupervised learning at scale, using clustering to uncover behavioral patterns that inform fraud detection strategies

---
This project was originally submitted as Assignment 2A for FIT5202 (Monash University, 2024), focused on building ML models for eCommerce fraud detection using big data techniques. It demonstrates practical expertise in ML pipelines, PySpark, and real-world fraud analytics