# flask --app server run
from flask import Flask
from flask import render_template
from flask import request
import os

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    
    return render_template('/login.html')

@app.route('/games')
def all_games():
    username = request.args.get('username')
    
    return render_template('/games.html', username=username)

@app.route('/games/<game_name>')
def game():
    username = request.args.get('username')
    
    return render_template('/game.html', username=username)

@app.route('/games/scorecards/<game_name>')
def scorecard_by_game():
    username = request.args.get('username')
    
    return render_template('/scorecards.html', username=username)

@app.route('/users/games/<user_name>')
def user_games():
    username = request.args.get('username')
    return render_template('/user_games.html',username=username)

@app.route('/users/', methods=['GET'])
def user_details():
    username = request.args.get('username')
    return render_template('/user_details.html',username=username)

@app.route('/scores')
def high_scores():
    username = request.args.get('username')
    return render_template('/scores.html',username=username)

@app.route('/scores/<user_name>')
def user_scores():
    username = request.args.get('username')
    return render_template('/user_scores.html',username=username)

@app.route('/scorecards')
def scorecards():
    username = request.args.get('username')
    return render_template('/scorecards.html',username=username)

@app.route('/scorecards/<scorecard_id>')
def scorecard():
    username = request.args.get('username')
    return render_template('/scorecard.html',username=username)

@app.route('/scorecards/game/<scorecard_id>')
def scorecard_by_game_scorecard():
    username = request.args.get('username')
    return render_template('/scorecard.html',username=username)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, port=port)