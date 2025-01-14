# flask --app server run
from flask import Flask
from flask import render_template
from flask import request
import os, sys

#Connect Controller definitions
fpath = os.path.join(os.path.dirname(__file__), 'controllers')
sys.path.append(fpath)
fpath = os.path.join(os.path.dirname(__file__), 'models')
sys.path.append(fpath)
from controllers import UserController, GameController, ScorecardController, SessionController

app = Flask(__name__, static_url_path='', static_folder='static')

#The Router section of our application conects routes to Contoller methods

#session
app.add_url_rule('/', view_func=SessionController.index, methods = ['GET'])
app.add_url_rule('/login', view_func=SessionController.login, methods = ['GET'])

#game
app.add_url_rule('/games/<username>', view_func=GameController.user_games, methods = ['GET'])
app.add_url_rule('/games', view_func=GameController.create_game, methods = ['POST'])
app.add_url_rule('/games/join', view_func=GameController.join_game, methods = ['POST'])
app.add_url_rule('/games/delete/<game_name>/<username>', view_func=GameController.delete_user_game, methods = ['GET'])
app.add_url_rule('/game/<game_name>/<username>', view_func=GameController.user_game, methods = ['GET'])

#scorecards
#app.add_url_rule('/scorecards/<scorecard_id>', view_func=ScorecardController.single_fruit, methods = ['POST'])

#users
app.add_url_rule('/users', view_func=UserController.users, methods = ['GET', 'POST'])
app.add_url_rule('/users/<username>', view_func=UserController.update_user, methods = ['GET', 'POST'])
app.add_url_rule('/users/delete/<username>', view_func=UserController.delete_user, methods = ['GET', 'POST'])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, port=port)