# flask --app server run
from flask import Flask
from flask import render_template
from flask import request
import os

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():

    return render_template('/login.html', )

@app.route('/game')
def about():
    username = request.args.get('username')
    
    return render_template('/game.html', username=username)

@app.route('/games')
def all_games():
    username = request.args.get('username')
    
    return render_template('/games.html', username=username)

@app.route('/games/<game_name>')
def about():
    username = request.args.get('username')
    
    return render_template('/game.html', username=username)

@app.route('/games/score')
def about():
    username = request.args.get('username')
    
    return render_template('/game.html', username=username)

@app.route('/users/games/<user_name>')
def user_games():
    username = request.args.get('username')
    return render_template('/user_games.html',username=username)

@app.route('/users/<user_name>')
def user_details():
    username = request.args.get('username')
    return render_template('/user_details.html',username=username)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, port=port)