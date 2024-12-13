from flask import jsonify, render_template
from flask import request

from Models import User_Model
User_DB_location = '../yahtzeeDB.db'
User = User_Model.User(User_DB_location, 'users')

def create_user():
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")

    print(request.form)

    if request.method == 'GET':
        return render_template('user_details.html')
    
    elif request.method == 'POST': #creating a user...
        user_games = []
        high_scores = []

        user_info = {
            "username": request.form.get('username'),
            "password": request.form.get('password'),
            "email": request.form.get('email')
        }

        user_data = User.create(user_info)["data"]

        return render_template('user_games.html', user_data=user_data, user_games=user_games, high_scores=high_scores)


# def update_user():
#     print(f"request.url={request.url}")
    
#     if request.method == 'GET':

        
# def delete_user()