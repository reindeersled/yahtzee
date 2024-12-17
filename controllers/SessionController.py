from flask import render_template, jsonify, redirect
from flask import request

from Models import User_Model
User_DB_location = '../yahtzeeDB.db'
User = User_Model.User(User_DB_location, 'users')

def login():
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")
    print(f"request.url={request.args.get('index')}")

    print(request.form)
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'Submit': #logging in 

            if User.get(username=request.form.get('username'))["data"]:
                print(User.get(username=request.form.get('username'))["data"])
                
                if request.form.get('password') == User.to_dict(User.get(username=request.form.get('username'))["data"])["data"]["password"]:
                    user_info = {
                        "username": request.form.get('username'),
                        "password": request.form.get('password')
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

    return render_template('login.html')
