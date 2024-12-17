from flask import render_template, jsonify, redirect
from flask import request

from Models import User_Model
User_DB_location = '../yahtzeeDB.db'
User = User_Model.User(User_DB_location, 'users')

def index():
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")
    print(f"request.url={request.args.get('index')}")

    return render_template('login.html')

def login():
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")
    print(f"request.url={request.args.get('index')}")

    print(request.form)
    
    action = request.form.get('action')
    username = request.args.get('username')
    password = request.args.get('password')

    if action == 'Submit': #logging in 

        if User.get(username=username)["data"]:
            print(User.get(username=username)["data"])
            
            if password == User.to_dict(User.get(username=username)["data"])["data"]["password"]:
                user_info = {
                    "username": username,
                    "password": password
                }
                return render_template('user_games.html', user_info=user_info)
            
            else:
                return jsonify({
                    "wrong password!"
                })
        
        else:
            return jsonify({
                "this user does not exist!"
            })
        
    elif action == 'Create': #new user
        return redirect('/users')


    return render_template('user_details.html')
