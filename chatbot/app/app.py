from flask import Flask
from flask_cors import CORS
from .app_bp import bp

app = Flask(__name__)
app.register_blueprint(bp)
CORS(app)

# RUN ETL every time the app is run
import requests
import pandas as pd
import os

data = pd.read_csv("https://raw.githubusercontent.com/josephrmartinez/recipe-dataset/refs/heads/main/13k-recipes.csv")
data = data.dropna()
data = data.drop_duplicates()
data = data.reset_index(drop=True)
data = data[["Title","Instructions","Cleaned_Ingredients"]]
data.to_csv("recipes.csv", index=False)