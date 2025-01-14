from flask import jsonify, render_template, redirect, url_for
from flask import request
import os

from Models import Game_Model, User_Model, Scorecard_Model
User_DB_location = f"{os.getcwd()}/Models/yahtzeeDB.db"
Game = Game_Model.Game(User_DB_location, 'games')
User = User_Model.User(User_DB_location, 'users')
Scorecard = Scorecard_Model.Scorecard(User_DB_location, 'scorecard', 'users', 'games')

def user_games(username):
    print("at user games", request.method)
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")

    if not User.exists(username=username)['data']:
        return render_template('login.html', feedback="That user does not exist!")
    
    user_dict = User.get(username=username)['data']

    game_names = Scorecard.get_all_user_game_names(username)['data']
    games = [Game.get(game_name=name)['data'] for name in game_names]

    scorecards = [(name, Scorecard.get(name=name+"|"+user_dict['username'])['data']) for name in game_names]
    high_scores = [ (scorecard[0], Scorecard.tally_score(scorecard[1]['categories'])) for scorecard in scorecards]
    high_scores.sort(key=lambda x: x[1], reverse=True)

    return render_template('user_games.html', user_dict=user_dict, games=games, high_scores=high_scores)

def create_game():
    print("at games", request.method)
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")

    username = request.form.get('username')
    print('creating game, username is', username)
    user_dict = User.get(username=username)['data']

    game_info = {
        "name": request.form.get('game_name_input')
    }

    game_names = Scorecard.get_all_user_game_names(username)['data']
    game = Game.create(game_info)
    if game['status'] == 'success':
        print("successfully created game")
        feedback = 'Game successfully created!'
        game_names.append(request.form.get('game_name_input'))
        print(game_names)
    else:
        feedback = game['data']
    games = [Game.get(game_name=name)['data'] for name in game_names]

    return render_template('user_games.html', username=username, games=games, user_dict=user_dict, feedback=feedback)


def join_game():
    print("joining game", request.method)
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")

    username = request.form.get('username')
    user_dict = User.get(username=username)['data']
    user_id = request.form.get('id')

    game_names = Scorecard.get_all_user_game_names(username)['data']
    games = [Game.get(game_name=name)['data'] for name in game_names]

    name = request.form.get('game_name_input')
    card_id = Game.get(game_name=name)['data']['id']

    create = Scorecard.create(card_id, user_id, name+"|"+username)
    if create['status'] == 'success':
        feedback = 'Successfully joined game!'
    else:
        feedback = create['data']

    return render_template('user_games.html', games=games, user_dict=user_dict, feedback=feedback)

def delete_user_game(game_name, username):
    print("deleting game", request.method)
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")

    user_dict = User.get(username=username)['data']
    game_names = Scorecard.get_all_user_game_names(username)['data']
    games = [Game.get(game_name=name)['data'] for name in game_names]

    remove = Game.remove(game_name)
    if remove['status'] == 'success':
        feedback = 'Successfully removed user from game'
        games = [game for game in games if game['name'] != game_name]
    else:
        feedback = remove['data']
    return render_template('user_games.html', games=games, user_dict=user_dict, feedback=feedback)

def user_game(game_name, username):
    print("getting specific game", request.method)
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")

    user_dict = User.get(username=username)['data']
    game = Game.get(game_name=game_name)

    return render_template('game.html', username=user_dict['username'], game_name=game_name)

