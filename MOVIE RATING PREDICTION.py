# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1h3Fg5uIpr6bq9x7abtr26P3_OThWp3ew
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load the dataset, specifying the encoding
data = pd.read_csv('/content/IMDb Movies India.csv', encoding='latin-1') # or 'ISO-8859-1'

# Display the first few rows of the dataset
print(data.head())

# Data Preprocessing
# Drop rows with missing ratings
data = data.dropna(subset=['Rating'])

# Convert 'Rating' to numeric
data['Rating'] = pd.to_numeric(data['Rating'], errors='coerce')

# Handle missing values in other columns if necessary
data.fillna('', inplace=True)

# Feature Engineering
# Create a new feature for the number of actors
data['Num_Actors'] = data[['Actor 1', 'Actor 2', 'Actor 3']].apply(lambda x: x.count(), axis=1)

# Define features and target variable
features = ['Genre', 'Director', 'Actor 1', 'Actor 2', 'Actor 3', 'Num_Actors']
target = 'Rating'

# Split the dataset into training and testing sets
X = data[features]
y = data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocessing and Model Pipeline
# Define the column transformer for preprocessing
# Handle unknown categories using handle_unknown='ignore' in OneHotEncoder
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['Genre', 'Director', 'Actor 1', 'Actor 2', 'Actor 3']),
        ('num', StandardScaler(), ['Num_Actors'])
    ])

# Create a pipeline that first transforms the data and then fits the model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(random_state=42))
])

# Train the model
pipeline.fit(X_train, y_train)

# Make predictions
y_pred = pipeline.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Absolute Error: {mae}')
print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# Feature Importance (for Random Forest)
# Get feature names after one-hot encoding
feature_names = pipeline.named_steps['preprocessor'].get_feature_names_out()
importances = pipeline.named_steps['regressor'].feature_importances_

# Create a DataFrame for feature importances
feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

# Plot feature importances
plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importance_df.head(20))
plt.title('Top 20 Important Features for Movie Rating Prediction')
plt.show()