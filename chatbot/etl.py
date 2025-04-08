# ETL Data from https://raw.githubusercontent.com/josephrmartinez/recipe-dataset/refs/heads/main/13k-recipes.csv
import requests
import pandas as pd
import os

data = pd.read_csv("https://raw.githubusercontent.com/josephrmartinez/recipe-dataset/refs/heads/main/13k-recipes.csv")
data = data.dropna()
data = data.drop_duplicates()
data = data.reset_index(drop=True)
data.to_csv("recipes.csv", index=False)