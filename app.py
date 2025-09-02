import os
from flask import Flask, render_template, request
import mysql.connector
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Flask app
app = Flask(__name__)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", 26370)),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB"),
    )

@app.route("/", methods=["GET", "POST"])
def index():
    recipes = []
    if request.method == "POST":
        ingredients = request.form["ingredients"]

        try:
            # Query OpenAI
            prompt = f"Suggest 3 simple recipes with the following ingredients: {ingredients}"
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7
            )
            recipes_text = response.choices[0].message.content.strip().split("\n")
        except Exception as e:
            # Fallback dummy recipes
            recipes_text = [
                f"Simple {ingredients} Stir Fry",
                f"{ingredients} Salad with Olive Oil",
                f"Grilled {ingredients} with Herbs"
            ]

        # Save recipes to DB
        conn = get_db_connection()
        cursor = conn.cursor()
        for recipe in recipes_text:
            cursor.execute("INSERT INTO recipes (ingredients, recipe_text) VALUES (%s, %s)", 
                           (ingredients, recipe))
            conn.commit()
            recipes.append(recipe)
        cursor.close()
        conn.close()

    return render_template("index.html", recipes=recipes)


if __name__ == "__main__":
    app.run(debug=True)
