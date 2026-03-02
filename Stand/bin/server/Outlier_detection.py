import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

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

# Create a box plot to visualize the data and highlight any potential outliers
plt.boxplot(data[column], showfliers=True)
plt.title('Box plot of {} column'.format(column))
plt.show()
