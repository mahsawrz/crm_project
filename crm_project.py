# -*- coding: utf-8 -*-
"""CRM-Project-Rezaei.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MV8-oa9pCYcqxRizSMW5KqYxpNgyjgGY
"""

# Calculating the correlation of Support_Request with the rest of the features
# to find out whether its zeros are real or not
import pandas as pd

# Load the dataset
df = pd.read_csv('CRM-Project-Noorbehbahani-Dataset.csv')

# Check the distribution of values in Support_Request
support_request_counts = df['Support_Request'].value_counts()

# Calculate percentage of zeros
zero_count = support_request_counts.get(0, 0)
total_count = len(df)
zero_percentage = (zero_count / total_count) * 100

# Print results
print(f"Number of zeros in Support_Request: {zero_count}")
print(f"Percentage of zeros: {zero_percentage}%")

# checking correlation with other columns:
correlation_matrix = df.corr()
print(correlation_matrix['Support_Request'])

# Interpreting the zeros of the Support_Request column
# by the attributes with which it is most correlated

import pandas as pd

# Load the dataset
df = pd.read_csv('CRM-Project-Noorbehbahani-Dataset.csv')

# Filter rows where Minutes_listened and Completion are both greater than 0
filtered_df = df[(df['Minutes_listened'] > 0) & (df['Completion'] > 0)]

# Calculate statistics of Support_Request where Minutes_listened and Completion are both > 0
non_zero_support_requests = filtered_df['Support_Request']

# Calculate statistics of Support_Request where Minutes_listened or Completion (or both) are 0
zero_minutes_or_completion = df[(df['Minutes_listened'] == 0) | (df['Completion'] == 0)]['Support_Request']

# Print statistics for comparison
print("Statistics for non-zero Minutes_listened and Completion:")
print(non_zero_support_requests.describe())

print("\nStatistics for zero Minutes_listened or Completion:")
print(zero_minutes_or_completion.describe())

# Create an error-free dataset

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'CRM-Project-Noorbehbahani-Dataset.csv'
dataset = pd.read_csv(file_path)

# Impute missing values in Review10/10 with the median
review_median = dataset['Review10/10'].median()
dataset['Review10/10'].fillna(review_median, inplace=True)

# Function to remove outliers using IQR
def remove_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]

# Remove outliers from Book_length(mins)_avg and Price_avg
dataset = remove_outliers_iqr(dataset, 'Book_length(mins)_avg')
dataset = remove_outliers_iqr(dataset, 'Price_avg')

# Ensure Completion rates are within [0, 1]
dataset = dataset[(dataset['Completion'] >= 0) & (dataset['Completion'] <= 1)]

# Ensure Minutes_listened does not exceed Book_length(mins)_overall
dataset = dataset[dataset['Minutes_listened'] <= dataset['Book_length(mins)_overall']]

# Backward fill the Support_Request column
dataset['Support_Request'] = dataset['Support_Request'].replace(0, method='bfill')

# Save the cleaned dataset
cleaned_file_path = 'cleaned_CRM_dataset.csv'
dataset.to_csv(cleaned_file_path, index=False)

# 1-1 Segmentation based on RFM

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


# Load the dataset
file_path = 'cleaned_CRM_dataset.csv'
df = pd.read_csv(file_path)

# Ensure data types are correct
df['Last_Visited_mins_Purchase_date'] = df['Last_Visited_mins_Purchase_date'].astype(int)
df['Support_Request'] = df['Support_Request'].astype(int)
df['Price_overall'] = df['Price_overall'].astype(float)

# Normalize Last_Visited_mins_Purchase_date using Min-Max scaling
scaler = MinMaxScaler()
df['Last_Visited_mins_Purchase_date'] = scaler.fit_transform(df[['Last_Visited_mins_Purchase_date']])

# Calculate RFM scores
df['Recency'] = df['Last_Visited_mins_Purchase_date']
df['Frequency'] = df['Support_Request']
df['Monetary'] = df['Price_overall']

# Define quantiles
quantiles = df[['Recency', 'Frequency', 'Monetary']].quantile([0.33, 0.66]).to_dict()

# Function to calculate RFM score
def rfm_score(x, p, d):
    if x <= d[p][0.33]:
        return 1
    elif x <= d[p][0.66]:
        return 2
    else:
        return 3

# Calculate R, F, M scores
df['R'] = df['Recency'].apply(rfm_score, args=('Recency', quantiles))
df['F'] = df['Frequency'].apply(rfm_score, args=('Frequency', quantiles))
df['M'] = df['Monetary'].apply(rfm_score, args=('Monetary', quantiles))

# Combine RFM scores into a single segment
df['RFM_Segment'] = df['R'].astype(str) + df['F'].astype(str) + df['M'].astype(str)
df['RFM_Segment'] = df['RFM_Segment'].astype('category')

# Ensure all 27 segments are represented, even those with zero members
all_segments = [f"{r}{f}{m}" for r in range(1, 4) for f in range(1, 4) for m in range(1, 4)]
segment_counts = df['RFM_Segment'].value_counts().reindex(all_segments, fill_value=0).sort_index()

# Plot bar graph of RFM segment counts
plt.figure(figsize=(18, 10))
segment_counts.plot(kind='bar', color='skyblue' , edgecolor='black')
plt.title('Number of Members in Each RFM Segment')
plt.xlabel('RFM Segment')
plt.ylabel('Number of Members')
plt.xticks(rotation=45)
plt.ylim(0, max(segment_counts) + 100)  # Adjust y-axis limit to ensure small counts are visible
for index, value in enumerate(segment_counts):
    plt.text(index, value + 10, str(value), ha='center', va='bottom', fontsize=10)  # Add value labels
plt.grid(axis='y', linestyle='--', linewidth=0.7)
plt.show()

# 1-1 Segmentation based on cell sorting

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'cleaned_CRM_dataset.csv'
df = pd.read_csv(file_path)

# Ensure data types are correct
df['Last_Visited_mins_Purchase_date'] = df['Last_Visited_mins_Purchase_date'].astype(int)
df['Support_Request'] = df['Support_Request'].astype(int)
df['Price_overall'] = df['Price_overall'].astype(float)

# Normalize Last_Visited_mins_Purchase_date using Min-Max scaling
scaler = MinMaxScaler()
df['Last_Visited_mins_Purchase_date'] = scaler.fit_transform(df[['Last_Visited_mins_Purchase_date']])

# Calculate RFM scores
df['Recency'] = df['Last_Visited_mins_Purchase_date']
df['Frequency'] = df['Support_Request']
df['Monetary'] = df['Price_overall']

# Ensure there are no negative values in Recency, Frequency, and Monetary columns
df = df[(df['Recency'] >= 0) & (df['Frequency'] >= 0) & (df['Monetary'] >= 0)]

# Function to calculate RFM cell sorting with dynamic bins
def rfm_cell_sorting(df):
    df = df.copy()

    # Adding a small noise to avoid duplicate bin edges
    df['Recency'] = df['Recency'] + np.random.rand(len(df)) * 0.01
    df['Frequency'] = df['Frequency'] + np.random.rand(len(df)) * 0.01
    df['Monetary'] = df['Monetary'] + np.random.rand(len(df)) * 0.01

    # Sorting by Recency
    df['R_rank'] = pd.qcut(df['Recency'], q=3, labels= [1,2,3])

    # Sorting by Frequency within each Recency group
    df['F_rank'] = df.groupby('R_rank')['Frequency'].transform(
        lambda x: pd.qcut(x.rank(method='first'), q=3, labels= [1,2,3])
    )

    # Sorting by Monetary within each Frequency group
    df['M_rank'] = df.groupby(['R_rank', 'F_rank'])['Monetary'].transform(
        lambda x: pd.qcut(x.rank(method='first'), q=3, labels= [1,2,3])
    )

    # Combining R, F, M ranks into a single RFM segment
    df['RFM_Segment'] = df['R_rank'].astype(str) + df['F_rank'].astype(str) + df['M_rank'].astype(str)

    return df

# Apply cell sorting to the dataset
df = rfm_cell_sorting(df)

# Calculate average Frequency and Monetary values for each segment
avg_values = df.groupby('RFM_Segment').agg({'Frequency': 'mean', 'Monetary': 'mean'}).reset_index()

# Plot the bar chart for average Frequency and Monetary values
fig, ax = plt.subplots(2, 1, figsize=(15, 10))

avg_values.plot(kind='bar', x='RFM_Segment', y='Frequency', ax=ax[0], color='skyblue', edgecolor='black', legend=False)
ax[0].set_title('Average Frequency for Each RFM Segment')
ax[0].set_xlabel('RFM Segment')
ax[0].set_ylabel('Average Frequency')
ax[0].grid(axis='y', linestyle='--', linewidth=0.7)

avg_values.plot(kind='bar', x='RFM_Segment', y='Monetary', ax=ax[1], color='lightpink', edgecolor='black', legend=False)
ax[1].set_title('Average Monetary Value for Each RFM Segment')
ax[1].set_xlabel('RFM Segment')
ax[1].set_ylabel('Average Monetary Value')
ax[1].grid(axis='y', linestyle='--', linewidth=0.7)

plt.tight_layout()
plt.show()

# Display the average values for interpretation
print(avg_values)

# Segmentation analysis based on cell sorting by adding Customer Satisfaction parameter

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'cleaned_CRM_dataset.csv'
df = pd.read_csv(file_path)

# Ensure data types are correct
df['Last_Visited_mins_Purchase_date'] = df['Last_Visited_mins_Purchase_date'].astype(int)
df['Support_Request'] = df['Support_Request'].astype(int)
df['Price_overall'] = df['Price_overall'].astype(float)

# Normalize Last_Visited_mins_Purchase_date using Min-Max scaling
scaler = MinMaxScaler()
df['Last_Visited_mins_Purchase_date'] = scaler.fit_transform(df[['Last_Visited_mins_Purchase_date']])

# Calculate RFM scores
df['Recency'] = df['Last_Visited_mins_Purchase_date']
df['Frequency'] = df['Support_Request']
df['Monetary'] = df['Price_overall']

# Ensure there are no negative values in Recency, Frequency, and Monetary columns
df = df[(df['Recency'] >= 0) & (df['Frequency'] >= 0) & (df['Monetary'] >= 0)]

# Function to calculate RFM cell sorting with dynamic bins
def rfm_cell_sorting(df):
    df = df.copy()

    # Adding a small noise to avoid duplicate bin edges
    df['Recency'] = df['Recency'] + np.random.rand(len(df)) * 0.01
    df['Frequency'] = df['Frequency'] + np.random.rand(len(df)) * 0.01
    df['Monetary'] = df['Monetary'] + np.random.rand(len(df)) * 0.01

    # Sorting by Recency
    df['R_rank'] = pd.qcut(df['Recency'], q=3, labels= [1,2,3])

    # Sorting by Frequency within each Recency group
    df['F_rank'] = df.groupby('R_rank')['Frequency'].transform(
        lambda x: pd.qcut(x.rank(method='first'), q=3, labels= [1,2,3])
    )

    # Sorting by Monetary within each Frequency group
    df['M_rank'] = df.groupby(['R_rank', 'F_rank'])['Monetary'].transform(
        lambda x: pd.qcut(x.rank(method='first'), q=3, labels= [1,2,3])
    )

    # Combining R, F, M ranks into a single RFM segment
    df['RFM_Segment'] = df['R_rank'].astype(str) + df['F_rank'].astype(str) + df['M_rank'].astype(str)

    return df

# Apply cell sorting to the dataset
df = rfm_cell_sorting(df)

# Calculate Customer Satisfaction as a combination of normalized Review and Support_Request
df['Customer_Satisfaction'] = (df['Support_Request'] + df['Review']) / 2

# Calculate average Frequency, Monetary, and Customer Satisfaction values for each segment
avg_values_with_satisfaction = df.groupby('RFM_Segment').agg({
    'Frequency': 'mean',
    'Monetary': 'mean',
    'Customer_Satisfaction': 'mean'
}).reset_index()

# Plot the bar chart for average Frequency, Monetary, and Customer Satisfaction values
fig, ax = plt.subplots(3, 1, figsize=(15, 15))

avg_values_with_satisfaction.plot(kind='bar', x='RFM_Segment', y='Frequency', ax=ax[0], color='skyblue', edgecolor='black', legend=False)
ax[0].set_title('Average Frequency for Each RFM Segment')
ax[0].set_xlabel('RFM Segment')
ax[0].set_ylabel('Average Frequency')
ax[0].grid(axis='y', linestyle='--', linewidth=0.7)

avg_values_with_satisfaction.plot(kind='bar', x='RFM_Segment', y='Monetary', ax=ax[1], color='lightpink', edgecolor='black', legend=False)
ax[1].set_title('Average Monetary Value for Each RFM Segment')
ax[1].set_xlabel('RFM Segment')
ax[1].set_ylabel('Average Monetary Value')
ax[1].grid(axis='y', linestyle='--', linewidth=0.7)

avg_values_with_satisfaction.plot(kind='bar', x='RFM_Segment', y='Customer_Satisfaction', ax=ax[2], color='lightgreen', edgecolor='black', legend=False)
ax[2].set_title('Average Customer Satisfaction for Each RFM Segment')
ax[2].set_xlabel('RFM Segment')
ax[2].set_ylabel('Average Customer Satisfaction')
ax[2].grid(axis='y', linestyle='--', linewidth=0.7)

plt.tight_layout()
plt.show()

# Display the average values for interpretation
print(avg_values_with_satisfaction)

#2-1 Density based segmentation

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics import pairwise_distances

# Load the dataset
file_path = 'CRM-Project-Noorbehbahani-Dataset.csv'
df = pd.read_csv(file_path)

# Step 1: Data Pre-processing

# Quantify missing data
missing_data = df.isnull().sum()

# Fill missing data with the mean of the column
df.fillna(df.mean(), inplace=True)

# Normalize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# Step 2: Calculate Correlation Matrix and Show it as a Heatmap

# Calculate the correlation matrix
correlation_matrix = pd.DataFrame(scaled_data, columns=df.columns).corr()

# Plot the heatmap
plt.figure(figsize=(14, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f',
            xticklabels=df.columns, yticklabels=df.columns)
plt.title('Correlation Matrix Heatmap')
plt.show()

# Find highly correlated features
high_corr_pairs = []
threshold = 0.8  # consider threshold
for i in range(len(correlation_matrix.columns)):
    for j in range(i):
        if abs(correlation_matrix.iloc[i, j]) > threshold:
            high_corr_pairs.append((df.columns[i], df.columns[j]))

print("Highly Correlated Features:")
for pair in high_corr_pairs:
    print(f"{pair[0]} and {pair[1]}")

# Choose one of the highly correlated features for segmentation
feature_for_segmentation = high_corr_pairs[0][0]  # Selecting the first feature

# Step 3: Segmentation using DBSCAN with selected feature

# Selecting the feature column
feature_column_index = df.columns.get_loc(feature_for_segmentation)
feature_data = scaled_data[:, feature_column_index].reshape(-1, 1)

# Determine the optimal epsilon using k-distance graph
distances = pairwise_distances(feature_data)
sorted_distances = np.sort(distances, axis=0)
k_distances = sorted_distances[:, 4]  # DBSCAN uses 4 as the default min_samples value

plt.plot(k_distances)
plt.xlabel('Points sorted by distance')
plt.ylabel('4th Nearest Neighbor Distance')
plt.title('k-distance Graph for DBSCAN')
plt.show()

# From the graph, choose an epsilon value (for example, 0.5)
epsilon = 0.5
dbscan = DBSCAN(eps=epsilon, min_samples=5)
clusters = dbscan.fit_predict(feature_data)

# Add the cluster labels to the original data
df['Cluster'] = clusters

# Display the number of sections
num_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
print(f"Number of sections (clusters): {num_clusters}")

# Identify features to keep (one from each highly correlated pair)
features_to_keep = set(df.columns)
for pair in high_corr_pairs:
    if pair[1] in features_to_keep:
        features_to_keep.remove(pair[1])

# Remove 'id' and 'target' from features_to_keep
features_to_keep.discard('id')
features_to_keep.discard('Target')

# Convert features_to_keep to a list
features_to_keep = list(features_to_keep)

# Analyze and visualize patterns in each section
for cluster in range(num_clusters):
    cluster_data = df[df['Cluster'] == cluster]
    print(f"\nCluster {cluster} - Mean values of selected features:")
    print(cluster_data[features_to_keep].mean())

    # Sort features based on mean values within the cluster
    sorted_features = cluster_data[features_to_keep].mean().sort_values(ascending=False)

    # Plot bar graph of mean values for the cluster
    plt.figure(figsize=(14, 6))  # Adjust figure size
    plt.bar(sorted_features.index, sorted_features.values)
    plt.title(f'Cluster {cluster} - Mean values of selected features')
    plt.xlabel('Features')
    plt.ylabel('Mean Value')
    plt.xticks(rotation=45, ha='right')  # Rotate labels and adjust alignment
    plt.tight_layout()  # Ensures labels are not cut off
    plt.show()

# 2- Customer repurchase prediction

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import SelectKBest, f_classif
import joblib

# Load the dataset
file_path = 'CRM-Project-Noorbehbahani-Dataset.csv'
df = pd.read_csv(file_path)

# Identify feature columns (excluding id and target)
feature_columns = [col for col in df.columns if col not in ['id', 'Target']]

# Handle missing data
imputer = SimpleImputer(strategy='median')
df[feature_columns] = imputer.fit_transform(df[feature_columns])

# Normalize numerical features
scaler = StandardScaler()
df[feature_columns] = scaler.fit_transform(df[feature_columns])

# Feature selection
X = df.drop('Target', axis=1)  # Assuming 'Target' is the column to be predicted
y = df['Target']

selector = SelectKBest(f_classif, k='all')
X_selected = selector.fit_transform(X, y)

# Balance the dataset using SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_selected, y)

# Split data into train and test sets (70/30 split)
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3, random_state=42, stratify=y_resampled)

# Initialize the classifier
clf = RandomForestClassifier(random_state=42)

# Training and testing using 10-fold cross-validation
kf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
cv_scores = cross_val_score(clf, X_resampled, y_resampled, cv=kf, scoring='accuracy')
cv_f1_scores = cross_val_score(clf, X_resampled, y_resampled, cv=kf, scoring='f1')

print(f"10-Fold Cross-Validation Accuracy: {np.mean(cv_scores):.4f}")
print(f"10-Fold Cross-Validation F1-Score: {np.mean(cv_f1_scores):.4f}")

# Training and testing using 70/30 split
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"70/30 Split Accuracy: {accuracy:.4f}")
print(f"70/30 Split F1-Score: {f1:.4f}")
print(f"Classification Report:\n{report}")

# Save the prediction results to a CSV file
results_df = pd.DataFrame({'Target_Label': y_test, 'Predicted_Target_Label': y_pred})
results_df.to_csv('prediction_results.csv', index=False)
print(results_df.head())