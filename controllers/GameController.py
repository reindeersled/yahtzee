from flask import jsonify, render_template
from flask import request

from Models import Game_Model
User_DB_location = '../yahtzeeDB.db'
Game = Game_Model.Game(User_DB_location, 'games')