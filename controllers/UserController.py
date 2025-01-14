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
    
    elif request.method == 'POST': #create
        user_info = {
                "username": request.form.get('username'),
                "password": request.form.get('password'),
                "email": request.form.get('email')
            }

        if not user_info['username'] or not user_info['password'] or not user_info['email']:
            return render_template('user_details.html', feedback="You need to fill out the form!")
        
        create_user = User.create(user_info)
        print(user_info)
        print("okay???", create_user)

        if create_user["status"] == 'error':
            feedback = create_user['data']
            user_dict = {}
        else:
            feedback = "New user created!"
            user_dict = create_user['data']
            return render_template('user_games.html', user_dict=user_dict, feedback=feedback)

        return render_template('user_details.html', user_dict=user_dict, feedback=feedback)

def update_user(username):
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")
    print(request.form)

    if request.method == 'GET':
        get = User.get(username=username)
        if get['status'] != 'success':
            feedback = get['data']
            user_dict = {}
        else:
            user_dict = get['data']
        return render_template('user_details.html', user_dict=user_dict, feedback=get['data'])

    elif request.method == 'POST':
        user_info = User.get(username=username)
        new_user_info = {
                "id": user_info['data']['id'],
                "username": request.form.get('username'),
                "password": request.form.get('password'),
                "email": request.form.get('email')
            }
        update = User.update(new_user_info)
        if update['status'] != 'success':
            feedback = update['data']
            u_dict = user_info['data']
        else:
            feedback = "Succesfully updated user details!"
            u_dict = new_user_info

        return render_template('user_details.html', user_dict=u_dict, feedback=feedback)

def delete_user(username):
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")

    removed_user = User.remove(username)
    if removed_user['status'] == 'error':
        user_dict = User.get(username=username)['data']
        return render_template('user_details.html', feedback=removed_user['data'], user_dict=user_dict)
    else:
        return render_template('login.html', feedback="User successfully deleted!")
