# https://mljourney.com/basic-machine-learning-python-example/

from sklearn.datasets import load_iris
import pandas as pd
 
# Load dataset
iris = load_iris()
 
# Convert to DataFrame
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target
 
# View first few rows
print(df.head())

X = df[iris.feature_names]  # Features
y = df['target']            # Labels

from sklearn.model_selection import train_test_split
 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.tree import DecisionTreeClassifier
 
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
 
from sklearn.metrics import accuracy_score, classification_report
 
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# from sklearn.ensemble import RandomForestClassifier
# model = RandomForestClassifier(n_estimators=100)
# model.fit(X_train, y_train)