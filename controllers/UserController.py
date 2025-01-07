from flask import jsonify, render_template
from flask import request
import os

from Models import User_Model
User_DB_location = f"{os.getcwd()}/Models/yahtzeeDB.db"
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
        if not user_info['username'] or not user_info['password'] or not user_info['email']:
            return render_template('user_details.html', feedback="You need to fill out the form!")
        
        u_dict = User.get(username=user_info['username'])['data']
        if (isinstance(u_dict, dict)):
            user_dict = u_dict
        else:
            user_dict = {}
        
        if action == 'Update':
            if User.exists(username=user_info['username'])['data']:
                user_games = []
                high_scores = []

                return render_template('user_games.html', user_dict=user_dict, feedback="User info updated!", user_games=user_games, high_scores=high_scores)
            
            else:
                return render_template('user_games.html', feedback="That user doesn't exist!")

        elif action == 'Create':
            user_games = []
            high_scores = []
            user_exists = User.exists(username=user_info['username'])
            
            if user_exists["data"]:
                return render_template('user_details.html', feedback="This user already exists!")
            
            create_user = User.create(user_info)
            print("okay???", create_user)
            if create_user["status"] != 'success':
                return render_template('user_details.html', user_dict=user_dict, feedback=create_user['data'])

            return render_template('user_games.html', user_dict=user_dict, feedback="New user created!", user_games=user_games, high_scores=high_scores)

        elif action=='Delete':
            removed_user = User.remove(user_info['username'])
            if removed_user["status"] != 'success':
                return render_template('user_details.html', user_dict=user_dict, feedback=removed_user['data'])
            else:
                return render_template('login.html', feedback="User deleted!")
        
    return render_template('user_details.html')