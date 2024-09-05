# flask --app data_server run
from flask import Flask
from flask import render_template
import json

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    f = open("data/Excel_dataset.json", "r")
    data = json.load(f)

    f.close()

    return render_template('/login.html')

@app.route('/game')
def about():
    
    return render_template('/game.html')

app.run(debug=True)