from flask import jsonify
from flask import request

from Models import User_Model
User_DB_location = '../yahtzeeDB.db'
User = User_Model.User_Model(User_DB_location)

def user():
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")
    print(f"request.url={request.args.get('index')}")

    # curl "http://127.0.0.1:5000/fruit/"
    if request.method == 'GET':
        return jsonify(User.get_all_fruit())
    
    #curl -X POST -H "Content-type: application/json" -d '{ "name" : "tomato", "url":"https://en.wikipedia.org/wiki/Tomato"}' "http://127.0.0.1:5000/fruit/new"
    elif request.method == 'POST':
        return jsonify(User.create_fruit(request.form))


def single_user(fruit_name):
    print(f"request.url={request.url}")
    
    if request.method == 'GET':
        # curl "http://127.0.0.1:5000/fruit/apples"
        all_fruit = User.get_all_fruit()
        if fruit_name in all_fruit:
            fruit = {fruit_name: all_fruit[fruit_name]}
            return jsonify(fruit)
        else:
            return {}