from flask import jsonify, render_template
from flask import request

from Models import User_Model
User_DB_location = '../yahtzeeDB.db'
User = User_Model.User(User_DB_location, 'users')


def users():
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")

    print(request.form)

    if request.method == 'GET':
        return render_template('user_details.html')
    
    elif request.method == 'POST': #create or update  user
        action=request.form.get('action')

        user_info = {
                "username": request.form.get('username'),
                "password": request.form.get('password'),
                "email": request.form.get('email')
            }
        
        if action == 'Update':
            if User.exists(username=user_info['username'])['data']:
                user_data = User.to_dict(User.get(username=user_info['username'])['data'])['data']
                user_games = []
                high_scores = []

                return render_template('user_games.html', user_data=user_data, user_games=user_games, high_scores=high_scores)
            
            else:
                return jsonify({
                    "That user doesn't exist!"
                })

        elif action=='Create':
            user_games = []
            high_scores = []
            user_data = User.create(user_info)["data"]

            return render_template('user_games.html', user_data=user_data, user_games=user_games, high_scores=high_scores)

        elif action=='Delete':
            removed_user = User.remove(user_info['username'])["data"]
            return render_template('user_games.html', removed_user=removed_user)

# def update_user():
#     print(f"request.url={request.url}")
    
#     if request.method == 'GET':

        
# def delete_user()