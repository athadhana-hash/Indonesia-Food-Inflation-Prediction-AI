📊 Indonesia Food Inflation Prediction

This project aims to build a machine learning-based system to predict food inflation in Indonesia using commodity price data, inflation indicators, and environmental factors.

Beyond prediction, this project also provides insights into the key drivers of inflation and includes an interactive simulation to support data-driven decision making.

⚠️ Problem Statement

There is no single, ready-to-use dataset available for modeling food inflation in Indonesia.

Relevant data is scattered across multiple official sources:

Statistics Indonesia (BPS)
Bank Indonesia (BI)
BMKG (weather data)

Additionally:

Data comes in different formats
Not integrated across sources
Consists of 27 raw datasets
Covers the period 2020–2025

As a result, the data cannot be directly used for machine learning.

💡 Solution

An ETL (Extract, Transform, Load) pipeline was developed to integrate all datasets into a single master dataset.

🔄 ETL Process

1. Extract

Collect data from multiple sources (inflation, commodity prices, rainfall)

2. Transform

Merge multi-year datasets
Standardize date formats
Handle missing values
Align data by time period
Feature engineering:
Inflation lag features
Rolling averages
Commodity price changes (%)
Rainfall anomaly

3. Load

Produce a final dataset ready for model training
🤖 Machine Learning Models

The following models were implemented:

Ridge Regression
XGBoost Regressor
📈 Model Performance

Ridge Regression

Test MAE: 0.0430
Test R²: 0.9979

XGBoost

Test MAE: 0.2729
Test RMSE: 0.3968
Test R²: 0.8294

🔍 Key Insights
Commodity price changes (rather than absolute prices) have the strongest impact on inflation
Chili price volatility is the most dominant factor influencing food inflation
Inflation shows strong temporal dependency (historical trends matter)
Environmental factors like rainfall have indirect influence
📊 Interactive Dashboard (Streamlit)

This project includes an interactive dashboard featuring:

Inflation trend visualization
Relationship between inflation and commodity prices
Model-based feature importance
Inflation condition alerts
Simulation of chili price changes and their impact on inflation

👉 The dashboard acts as a decision support system, not just a visualization tool.

⚙️ Project Structure
data_preprocessing/
EDA/
model/
train_model/
dataset/
dashboard/

▶️ How to Run
1. Build Dataset
python data_preprocessing/build_main_dataset.py
2. Data Preprocessing
jupyter notebook data_preprocessing/process.ipynb
3. Train Model
jupyter notebook train_model/model.ipynb
4. Run Dashboard
streamlit run dashboard/dashboard.py

🧠 Tech Stack
Python
Pandas & NumPy
Scikit-learn
XGBoost
Streamlit

🎯 Conclusion

This project demonstrates that:

Disconnected economic datasets can be integrated through an ETL pipeline
Machine learning can effectively capture food inflation patterns
Data-driven systems can support better understanding and decision making

👉 This approach transforms raw data into actionable insights for monitoring and managing food inflation.
