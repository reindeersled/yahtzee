from flask import jsonify, render_template
from flask import request
import os

from Models import User_Model
User_DB_location = f"{os.getcwd()}/Models/yahtzeeDB.db"
User = User_Model.User(User_DB_location, 'users')


def users():
    print("at users", request.method)
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")

    print(request.form)

    if request.method == 'GET':
        return render_template('user_details.html')
    
    elif request.method == 'POST':
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
            print("UPDATING")
            user_id = int(request.form.get('id'))
            if User.exists(username=user_id)['data'] == True:
                user_games = []
                high_scores = []

                return render_template('user_details.html', user_dict=user_dict, feedback="User info updated!", user_games=user_games, high_scores=high_scores)
            
            else:
                print(User.exists(username=user_id)['data'])
                return render_template('user_details.html', user_dict=user_dict, feedback="That user doesn't exist!")

        elif action == 'Create':
            print("CREATING")
            user_games = []
            high_scores = []
            user_exists = User.exists(username=user_info['username'])
            
            if user_exists["data"]:
                return render_template('user_details.html', user_dict=user_dict, feedback="This user already exists!")
            
            create_user = User.create(user_info)
            print("okay???", create_user)
            if create_user["status"] != 'success':
                return render_template('user_details.html', user_dict=user_dict, feedback=create_user['data'])
            else:
                return render_template('user_games.html', user_dict=user_dict, feedback="New user created!", user_games=user_games, high_scores=high_scores)
        
        elif action == 'Delete':
            print("DELETING")
            username = User.get(id=request.form.get('id'))['data']['username']
            delete_user(username=username)

    return render_template('user_details.html')

def specific_user(username):
    print("at specific user", request.method)
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")

    print(request.form)

    u_dict = User.get(username=username)['data']
    if (isinstance(u_dict, dict)):
        user_dict = u_dict
    else:
        user_dict = {}

    if request.method == 'GET':
        print("GETTING SPECIFIC USER")
        if user_dict:
            return render_template('user_details.html', user_dict=user_dict)
        else:
            return render_template('user_details.html', user_dict=user_dict, feedback="No user with this username exists!")
    
    if request.method == 'POST':
        action=request.form.get('action')
        print("action", action)

        user_info = {
                "username": request.form.get('username'),
                "password": request.form.get('password'),
                "email": request.form.get('email')
            }

        if action == 'Update':
            print("UPDATING SPECIFIC USER")
            user_id = int(request.form.get('id'))

            exists = User.exists(username=user_id)
            if exists['data'] == True:
                feedback = User.update(user_info)['data']
            else:
                feedback = exists['data']
            print(feedback)

            return render_template('user_details.html', user_dict=user_dict, feedback=feedback)
        
        elif action == 'Delete':
            print("DELETING SPECIFIC USER")
            delete_user(username)

def delete_user(username):
    print("trying to delete...")
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")

    u_dict = User.get(username=username)['data']
    if (isinstance(u_dict, dict)):
        user_dict = u_dict
    else:
        user_dict = {}

    removed_user = User.remove(username)

    if removed_user['status'] != 'success':
        print("UNSUCCESSFUL", removed_user['data'])
        return render_template('user_details.html', feedback=removed_user['data'], user_dict=u_dict)
    else:
        print("SUCCESSFUL", removed_user['data'])
        return render_template('login.html', feedback="User successfully deleted!")
