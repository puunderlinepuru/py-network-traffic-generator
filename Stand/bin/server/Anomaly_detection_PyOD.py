# https://www.geeksforgeeks.org/machine-learning/introduction-to-anomaly-detection-with-python/

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Using PyOD
from pyod.utils.data import generate_data, get_outliers_inliers
from pyod.models.pca import PCA
from pyod.utils.data import evaluate_print
from pyod.utils.example import visualize

from pandas import read_csv

from sklearn.model_selection import train_test_split

# Start by creating a dataset using generate_data() from pyod
# X_train, y_train = generate_data(train_only=True)

# url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
# names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']

url = "./generated/formatted_capture.csv"
# names = ['src', 'dst', 'id', 'checksum',]

dataset = read_csv(url)

array = dataset.values

X = array[:,3:4]
y = array[:,4]


print(X)
print(y)

X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1)

# Create dataframe from Pandas using the generated data
df_train = pd.DataFrame(X_train)
df_train['y'] = Y_train

# Display first few rows
df_train.head()

sns.scatterplot(x=0, y=1, hue='y', data=df_train, palette="hls", legend="full")
plt.title('Ground Truth')

# Create PCA model
clf = PCA()

# Trains PCA model
clf.fit(X_train)

# Store predictions for inlier and outlier in array as 0s and 1s
y_train_pred = clf.labels_
y_train_scores = clf.decision_scores_

print("Predictions:")
for prediction in clf.labels_:
    print(prediction)

print("Decision scores:")
for decision in clf.decision_scores_:
    print(decision)

# ax = sns.scatterplot(x=0, y=1, hue=y_train_scores, data=df_train, palette="RdBu_r")
displot = sns.displot(df_train)

# Using legends, results look bit varied
legend_labels = [f"{score:.2f}" for score in np.unique(y_train_scores)]  # Format scores up to 2 decimal places
# ax.legend(title="Anomaly Scores", labels=legend_labels)  # Create legend with title and labels
plt.title('Anomaly Scores by PCA')
plt.show()