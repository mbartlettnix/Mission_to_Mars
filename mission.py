# Mission to Mars Flask App 
import pandas as pandas
from flask import Flask, render_template, jsonify, redirect
import pymongo

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mission_db
collection = db.mars

@app.route("/")
def index():
    # hurricanes = list(db.collection.find())
    # print(hurricanes)
    # return render_template("index.html", hurricanes=hurricanes)


if __name__ == "__main__":
    app.run(debug=True)
