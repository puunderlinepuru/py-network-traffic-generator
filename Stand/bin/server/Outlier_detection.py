import pandas as pd
from sklearn.ensemble import IsolationForest

import matplotlib.pyplot as plt

import Display_data

# Load the CSV file into a DataFrame
data = pd.read_csv('./generated/formatted_capture.csv')

# Select the column you want to detect outliers in
column = 'tos'

# Create an IsolationForest model and fit it to the data
model = IsolationForest(contamination=0.05) # Adjust contamination parameter as needed
outliers = model.fit_predict(data[[column]])

# Add a new column to the DataFrame indicating whether each row is an outlier or not
data['Outlier'] = outliers == -1

# Print some statistical data about the outliers
print("Number of outliers:", sum(outliers == -1))
print("Percentage of outliers:", 100 * sum(outliers == -1) / len(data))

outliers_values = data[outliers == -1]['id'].to_numpy()
print("outliers_values: ", outliers_values)

print("outliers: \n", data[outliers == -1], type(data[outliers == -1]))

Display_data.dis()

# Create a box plot to visualize the data and highlight any potential outliers
plt.boxplot(data[column], showfliers=True)

plt.title('Box plot of {} column'.format(column))
plt.show()
