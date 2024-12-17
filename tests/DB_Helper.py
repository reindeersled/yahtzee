import os
import sys

fpath = os.path.join(os.path.dirname(__file__), '../Models')
sys.path.append(fpath)
import User_Model, Game_Model, Scorecard_Model

def wipe_and_clean_tables(yahtzee_db_name):
    print("yahtzee_db_name", yahtzee_db_name)
    user_table_name = "users"
    game_table_name = "games"
    scorecard_table_name = "scorecard"
    User_Model.User(yahtzee_db_name, user_table_name).initialize_table()
    Game_Model.Game(yahtzee_db_name, game_table_name).initialize_table()
    Scorecard_Model.Scorecard(yahtzee_db_name, scorecard_table_name, user_table_name, game_table_name).initialize_table()

if __name__ == '__main__':
    wipe_and_clean_tables(f"{os.getcwd()}/Models/yahtzeeDB.db") 