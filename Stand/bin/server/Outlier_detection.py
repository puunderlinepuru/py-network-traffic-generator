import pickle
from pydoc import text
from xml.parsers.expat import model

import pandas as pd
from sklearn.ensemble import IsolationForest

import matplotlib.pyplot as plt
import yaml

import Display_data

from math import log2
from collections import Counter

from rich.console import Console

console = Console()

def write_to_yml(file_path, data):
    """Write dictionary data to a YAML file."""
    with open(file_path, 'w') as file:
        yaml.dump(data, file)
        
def read_yml(file_path):
    """Load a YAML file and return a dictionary."""
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def shannon_entropy(data):
    """Calculate the Shannon entropy of a list."""
    # Create a frequency dictionary
    freq_dict = Counter(data)

    # Total number of elements in the list
    total_elements = len(data)

    # Calculate the probability of each element and sum up their contributions to the entropy
    entropy = 0
    for count in freq_dict.values():
        prob = count / total_elements
        entropy -= prob * log2(prob)

    return entropy


def detect_outliers(model, field_name):
    column = field_name
    
    data = pd.read_csv('./generated/formatted_capture.csv')

    # Predict outliers using the loaded model
    outliers = model.fit_predict(data[[column]])

    # Add a new column to the DataFrame indicating whether each row is an outlier or not
    data['Outlier'] = outliers == -1
    
    outliers_values = data[outliers == -1][field_name].to_numpy()
    
    return outliers_values, data[outliers == -1]

def learn():
    # Load the CSV file into a DataFrame
    data = pd.read_csv('./generated/formatted_capture.csv')
    
    fig, axs = plt.subplots(2, 2, figsize=(10, 5))
    
    # FIELDS
    
    # IPv4
    # src
    print('\n[SRC]')
    column = 'src'
    model = IsolationForest(contamination=0.001)
    outliers = model.fit_predict(data[[column]])
    # Add a new column to the DataFrame indicating whether each row is an outlier or not
    data['Outlier'] = outliers == -1
    outliers_values = data[outliers == -1][column].to_numpy()
    print("Number of outliers:", sum(outliers == -1))
    print("Percentage of outliers:", 100 * sum(outliers == -1) / len(data))
    print("outliers_values: ", outliers_values)
    print("outliers: \n", data[outliers == -1], type(data[outliers == -1]))
    axs[0][0].hist(data[column], bins='auto', edgecolor='black')
    axs[0][0].set_title(column)
    
    shannon_entropy_value = shannon_entropy(data[column])
    print(f"Shannon entropy of {column}: {shannon_entropy_value}")
    
    # tos
    print('\n[TOS]')
    column = 'tos'
    model = IsolationForest(contamination=0.001)
    outliers = model.fit_predict(data[[column]])
    # Add a new column to the DataFrame indicating whether each row is an outlier or not
    data['Outlier'] = outliers == -1
    outliers_values = data[outliers == -1][column].to_numpy()
    print("Number of outliers:", sum(outliers == -1))
    print("Percentage of outliers:", 100 * sum(outliers == -1) / len(data))
    print("outliers_values: ", outliers_values)
    print("outliers: \n", data[outliers == -1], type(data[outliers == -1]))
    axs[0][1].hist(data[column], bins='auto', edgecolor='black')
    axs[0][1].set_title(column)
    
    shannon_entropy_value = shannon_entropy(data[column])
    print(f"Shannon entropy of {column}: {shannon_entropy_value}")
    
    # id
    print('\n[ID]')
    column = 'id'
    model = IsolationForest(contamination=0.001)
    outliers = model.fit_predict(data[[column]])
    # Add a new column to the DataFrame indicating whether each row is an outlier or not
    data['Outlier'] = outliers == -1
    outliers_values = data[outliers == -1][column].to_numpy()
    print("Number of outliers:", sum(outliers == -1))
    print("Percentage of outliers:", 100 * sum(outliers == -1) / len(data))
    print("outliers_values: ", outliers_values)
    print("outliers: \n", data[outliers == -1], type(data[outliers == -1]))
    axs[1][0].hist(data[column], bins='auto', edgecolor='black')
    axs[1][0].set_title(column)
    
    shannon_entropy_value = shannon_entropy(data[column])
    print(f"Shannon entropy of {column}: {shannon_entropy_value}")
    
    plt.tight_layout()
    plt.show()    
    
    save_model_bool = input("Do you want to save the model? (Y/n)" )
    if save_model_bool.upper() == "Y" or save_model_bool == "":
        with open("model.pkl", 'wb') as f:
            pickle.dump(model, f)

def use_model(file_name):
    # Load the trained model from the pickle file
    with open(file_name, 'rb') as f:
        model = pickle.load(f)

    # FIELDS
    
    # IPv4
    # src
    column = 'src'
    data = pd.read_csv('./generated/formatted_capture.csv')
    outliers = model.fit_predict(data[[column]])
    # Add a new column to the DataFrame indicating whether each row is an outlier or not
    data['Outlier'] = outliers == -1
    outliers_values = data[outliers == -1][column].to_numpy()
    print("Number of outliers:", sum(outliers == -1))
    print("Percentage of outliers:", 100 * sum(outliers == -1) / len(data))
    print("outliers_values: ", outliers_values)
    print("outliers: \n", data[outliers == -1], type(data[outliers == -1]))
    
    # tos
    column = 'tos'
    outliers = model.fit_predict(data[[column]])
    # Add a new column to the DataFrame indicating whether each row is an outlier or not
    data['Outlier'] = outliers == -1
    outliers_values = data[outliers == -1][column].to_numpy()
    print("Number of outliers:", sum(outliers == -1))
    print("Percentage of outliers:", 100 * sum(outliers == -1) / len(data))
    print("outliers_values: ", outliers_values)
    print("outliers: \n", data[outliers == -1], type(data[outliers == -1]))
    
    # id
    column = 'id'
    outliers = model.fit_predict(data[[column]])
    # Add a new column to the DataFrame indicating whether each row is an outlier or not
    data['Outlier'] = outliers == -1
    outliers_values = data[outliers == -1][column].to_numpy()
    print("Number of outliers:", sum(outliers == -1))
    print("Percentage of outliers:", 100 * sum(outliers == -1) / len(data))
    print("outliers_values: ", outliers_values)
    print("outliers: \n", data[outliers == -1], type(data[outliers == -1]))

def use_existing_model():
    file_name = input("Enter the name of pickle file:")
    use_model(file_name)



def calculate_shannon_entropy():
    shannon_entropy_values = {}
    for column in data.columns:
        shannon_entropy_value = shannon_entropy(data[column])
        shannon_entropy_values[column] = shannon_entropy_value
        print(f"Shannon entropy of {column}: {shannon_entropy_value}")
    print("[1] - Compare")
    print("[2] - Save")
    choice = input("Choose: ")
    
    if choice == "1":
        existing_shannon_entropy_values = read_yml("shannon_entropy.yml").get("shannon_entropy_values", {})
        print("Existing Shannon entropy values: ", existing_shannon_entropy_values)
        print("type: ", type(existing_shannon_entropy_values))
        if compare_dicts(shannon_entropy_values, existing_shannon_entropy_values):
            console.print("The Shannon entropy values are the same as the existing ones.")
        save_shannon_entropy_bool = input("Do you want to save(update) the Shannon entropy values? (Y/n)" )
        if save_shannon_entropy_bool.upper() == "Y" or save_shannon_entropy_bool == "":
            write_to_yml("shannon_entropy.yml", {"shannon_entropy_values": shannon_entropy_values})
        
    elif choice == "2":
        write_to_yml("shannon_entropy.yml", {"shannon_entropy_values": shannon_entropy_values})
        
def compare_dicts(dict1, dict2):
    """Compare two dictionaries for equality."""
    if len(dict1) != len(dict2):
        console.print("[red]Lengths of dictionaries are different and can't be compared.")
        return False
    for i in range(len(dict1)):
        key1 = list(dict1.keys())[i]
        if dict1[key1] != dict2[key1]:
            console.print(f"[red] Mismatch: '{key1}' {dict1[key1]}[current] vs {dict2[key1]} [existing]")
            return False
    return True
    
if __name__ == "__main__":
    with console.status("Reading existing data...", spinner="dots"):
        try:
            data = pd.read_csv('./generated/formatted_capture.csv')
        except FileNotFoundError:
            console.print("[red]No existing data found. Please run \n   1.CSV generator.py \n   2.CSV formatter \nfirst.")
            exit()
    
    print("[1] - Learn")
    print("[2] - Use Model")
    print("[3] - Calculate Shannon entropy")
    choice = input("Press Enter to exit")
    while choice != "":
        if choice == "1":
            learn()
        elif choice == "2":
            use_existing_model()
        elif choice == "3":
            calculate_shannon_entropy()
            
        print("[1] - Learn")
        print("[2] - Use Model")
        choice = input("Press Enter to exit")
