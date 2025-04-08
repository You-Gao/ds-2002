from flask import Blueprint, render_template, request, jsonify
from flask.views import MethodView
import requests
import os
import json

import google.generativeai as genai

API_KEY = os.getenv("SPOONACULAR_API_KEY")
PROMPT = "Respond with JSON containing the title (String), ingredients (Array), instructions (Array), and tips (Array) of the recipe. Just the JSON dictionary, no other text."
client = genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")
bp = Blueprint("app", __name__, url_prefix="/")

@bp.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        data = request.get_json()
        message = data.get("message")
        if "cook" in message:
            meal = message.split("cook")[-1].strip()
            
            local_response = local_instructions(meal)
            if local_response["title"] != "Recipe not found":
                return jsonify({"response": local_response})
            
            chatbot_response = chatbot_instructions(meal)
            response = json.loads(chatbot_response)
            print(response)
            return jsonify({"response": response})
        return jsonify({"response": "Please provide a meal to cook."})
    
    return render_template("chat.html")

def chatbot_instructions(meal_str):
    recipe_id = autocomplete(meal_str)
    instructions_response = instructions(recipe_id)
    gemini = gemini_response(instructions_response["instructions"])
    return gemini

def gemini_response(message):
    response = model.generate_content(message + PROMPT)
    cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
    return cleaned_response 

def autocomplete(meal_str):
    url = "https://api.spoonacular.com/recipes/autocomplete"
    requests_params = {
        "number": 1,
        "apiKey": API_KEY,
        "query": meal_str,
    }
    response = requests.get(url, params=requests_params).json()[0]["id"]
    return response

def instructions(recipe_id):
    url = "https://api.spoonacular.com/recipes/{}/information".format(recipe_id)
    requests_params = {
        "apiKey": API_KEY,
    }
    response = requests.get(url, params=requests_params).json()
    return response

def local_instructions(meal_str):
    import pandas as pd
    recipes = pd.read_csv("recipes.csv")
    similar_recipes = recipes[recipes["Title"].str.contains(meal_str, case=False)]
    if not similar_recipes.empty:
        recipe = similar_recipes.iloc[0]
        return {
            "title": recipe["Title"],
            "ingredients": recipe["Cleaned_Ingredients"].split(", "),
            "instructions": recipe["Instructions"].split(". "),
            "tips": ["Use fresh ingredients", "Adjust seasoning to taste"]
        }
    else:
        return {
            "title": "Recipe not found",
            "ingredients": [],
            "instructions": [],
            "tips": []
        }