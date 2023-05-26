import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        adj = request.form["adj"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(adj),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    print(result)
    return render_template("index.html", result=result)


def generate_prompt(adj):
    return f"""
    Your task is to create an alcoholic coktail using the adjectives delimited by triple \
    backticks.

    Produce the following in a html format:
    Name: <drink name that is creative and does not contain the original adjectives>

    Ingredients: <drink ingredients (around 3-5)>

    Directions: <step by step drink directions>

    \"\"\"{adj}\"\"\"
    """