import pandas as pd
import seaborn 
import numpy as np
import plotly
import matplotlib as plt

def classify_variable_types(df):
    variable_types = {}
    
    for column in df.columns:
        dtype = df[column].dtype
        
        if dtype == 'int64':
            # Check if the values are finite and countable
            unique_values = df[column].nunique()
            if unique_values < len(df):  # Heuristic: fewer unique values than rows
                variable_types[column] = 'Discrete'
            else:
                variable_types[column] = 'Continuous'
        elif dtype == 'float64':
            # Continuous variable
            variable_types[column] = 'Continuous'
        elif dtype == 'category':
            if df[column].cat.ordered:
                variable_types[column] = 'Ordinal'
            else:
                variable_types[column] = 'Nominal'
        elif dtype == 'object':
            # Could be nominal or ordinal if it has a limited number of unique values
            unique_values = df[column].nunique()
            if unique_values < len(df) / 2:  # Heuristic to guess if it's categorical
                variable_types[column] = 'Nominal'
            else:
                variable_types[column] = 'Text/String'
        else:
            variable_types[column] = 'Unknown'
    
    return variable_types

# Classify and print variable types
variable_types = classify_variable_types(df)
for variable, var_type in variable_types.items():
    print(f"{variable}: {var_type}")
