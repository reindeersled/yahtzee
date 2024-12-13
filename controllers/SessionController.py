from flask import render_template
from flask import request

def login():
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")
    print(f"request.url={request.args.get('index')}")

    return render_template('login.html')
