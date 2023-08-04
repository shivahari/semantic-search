# reference https://stackoverflow.com/questions/39614604/autocomplete-search-box-and-pass-value-to-flask
from flask import Flask, request, render_template, jsonify
import os
import requests

app = Flask(__name__)
BASE_URL = os.environ.get('SEM_SEARCH_APP', 'http://localhost:8000/sem-search/')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search/<box>")
def sem_search(box):
    query = request.args.get('query')
    url = BASE_URL + query

    response = requests.get(url=url)
    print(response.json())

    return jsonify({"suggestions":response.json()})

if __name__ == "__main__":
    app.run(debug=True)