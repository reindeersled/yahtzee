from flask import render_template, jsonify, redirect
from flask import request
import os, sys

from Models import User_Model
User_DB_location = f"{os.getcwd()}/Models/yahtzeeDB.db"
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
    
    action = request.args.get('action')
    username = request.args.get('username')
    password = request.args.get('password')

    if action == 'Submit': #logging in

        if User.get(username=username)["status"] == 'success':
            user_dict = User.get(username=username)["data"]

            if password == user_dict["password"]:
                return render_template('user_games.html', feedback="Logged in!", user_dict=user_dict)
            
            else:
                return render_template('login.html', feedback="Wrong password!")
        
        else:
            return render_template('login.html', feedback="This user does not exist!")
        
    elif action == 'Create': #new user
        return redirect('/users')


    return render_template('user_details.html')