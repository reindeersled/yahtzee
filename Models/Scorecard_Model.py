#Reina Lin
import sqlite3
import random
import json

class Scorecard:
    def __init__(self, db_name, scorecard_table_name, user_table_name, card_table_name):
        self.db_name =  db_name
        self.max_safe_id = 9007199254740991 #maximun safe Javascript integer
        self.table_name = scorecard_table_name #all the scorecards
        self.user_table_name = user_table_name #all the users
        self.card_table_name = card_table_name #all the games
    
    def initialize_table(self):
        db_connection = sqlite3.connect(self.db_name, )
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    card_id INTEGER,
                    user_id INTEGER,
                    categories TEXT,
                    turn_order INTEGER,
                    name TEXT,
                    FOREIGN KEY(card_id) REFERENCES {self.card_table_name}(id) ON DELETE CASCADE,
                    FOREIGN KEY(user_id) REFERENCES {self.user_table_name}(id) ON DELETE CASCADE
                )
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def create(self, card_id, user_id, name):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            scorecard_id = random.randint(0, self.max_safe_id)
            
            cursor.execute(f"""SELECT * FROM {self.table_name}
                           WHERE {self.table_name}.card_id = {card_id};""")
            print(cursor.fetchall()) #empty list
            turn_order = len(cursor.fetchall())
            if turn_order > 4:
                return {"status": "error",
                        "data": "too many players already in this game"}

            categories = json.dumps(self.create_blank_score_info())

            cursor.execute(f"INSERT INTO {self.table_name} (id, card_id, user_id, categories, turn_order, name) VALUES (?, ?, ?, ?, ?, ?);", (scorecard_id, card_id, user_id, categories, turn_order, name,))
            db_connection.commit()

            card_tuple = (scorecard_id, card_id, user_id, categories, turn_order, name)

            return {"status": "success",
                    "data": self.to_dict(card_tuple)}
   
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def get(self, name=None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if name:
                cursor.execute(f"SELECT * FROM {self.table_name} WHERE name = ?;", (name,))
                card_info = cursor.fetchone()

                if card_info:
                    return {"status": "success",
                            "data": self.to_dict(card_info)}
                else:
                        return {"status": "error",
                                "data": "no card found"}
            if id:
                cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?;", (id,))
                card_info = cursor.fetchone()

                if card_info:
                    return {"status": "success",
                            "data": self.to_dict(card_info)}
                else:
                    return {"status": "error",
                            "data": "no card found"}
            
            else:
                return {"status": "error",
                        "data": "no name or id given"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all(self): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            cursor.execute(f"SELECT * FROM {self.table_name};")
            cards_data = cursor.fetchall()

            all_cards = []
            for card_data in cards_data:
                all_cards.append(self.to_dict(card_data))
            
            return {"status":"success",
                    "data": all_cards}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all_card_scorecards(self, card_name:str): #each game can have up to 4 scorecards
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if card_name:
                cursor.execute(f"SELECT id FROM {self.card_table_name} WHERE name = ?;", (card_name,))
                game_id = cursor.fetchone()

                cursor.execute(f"SELECT * FROM {self.table_name} INNER JOIN {self.card_table_name} ON {self.table_name}.game_id = {game_id};")
                all_scorecards = cursor.fetchall()

                all_scorecards_list = []
                for scorecard in all_scorecards:
                    all_scorecards_list.append(self.to_dict(scorecard))
            
                return {"status":"success",
                    "data": all_scorecards_list}
            else:
                return {"status": "error",
                        "data": "no card name given"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def get_all_card_usernames(self, card_name:str): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if card_name:
                cursor.execute(f"SELECT name FROM {self.card_table_name}")
                card_usernames = cursor.fetchall()
                return {"status":"success",
                        "data": card_usernames}
            else:
                return {"status":"error",
                        "data":"no card name given"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def get_all_user_card_names(self, username:str): #based on the username provided, select all the names of the games with user_id = that
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if username:

                cursor.execute(f"SELECT name FROM {self.card_table_name} WHERE username = ?;", (username,))
                card_names = cursor.fetchall()
                all_card_names = []
                for username_data in username_data:
                    all_card_names.append(self.to_dict(username_data))
            
                return {"status":"success",
                    "data": all_card_names}
            
            else: 
                return {"status":"error",
                    "data": "no username provided"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def update(self, id, name=None, score_info=None): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def remove(self, id): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if id:
                deleted_data = self.get(id=id)["data"]

                cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?;", (id,))
                db_connection.commit()

                return {"status": "success",
                        "data": self.to_dict(deleted_data)} 
            else:
                return {"status": "error",
                        "data": "no id provided"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def to_dict(self, card_tuple):
        card_dict={}
        if card_tuple:
            card_dict["id"]=card_tuple[0]
            card_dict["game_id"]=card_tuple[1]
            card_dict["user_id"]=card_tuple[2]
            card_dict["categories"]=json.loads(card_tuple[3])
            card_dict["turn_order"]=card_tuple[4]
            card_dict["name"]=card_tuple[5]
        return card_dict
    
    def create_blank_score_info(self):
        return {
            "dice_rolls":0,
            "upper":{
                "ones":-1,
                "twos":-1,
                "threes":-1,
                "fours":-1,
                "fives":-1,
                "sixes":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }

    def tally_score(self, score_info): #assuming score_info is just the upper and lower and dice_rolls
        total_score = 0

        for category in score_info["upper"]:
            if score_info["upper"][category] != -1:
                total_score += score_info["upper"][category]
        for category in score_info["lower"]:
            if score_info["lower"][category] != -1:
                total_score += score_info["lower"[category]]

   
        return total_score
    

if __name__ == '__main__':
    import os
    DB_location=f"{os.getcwd()}/yahtzeeDB.db"
    #print("location", DB_location)
    Scorecards =Scorecard(DB_location, "scorecards", "users", "games")
    Scorecards.initialize_table()

    game_details={ 
        "game_id": 123456789101112,
        "user_id": 123456789101112,
        "categories": {
                    "dice_rolls":3,
                    "upper":{
                        "ones":-1,
                        "twos":-1,
                        "threes":-1,
                        "fours":-1,
                        "fives":-1,
                        "sixes":-1
                    },
                    "lower":{
                    "three_of_a_kind":-1,
                        "four_of_a_kind":-1,
                        "full_house":-1,
                        "small_straight":-1,
                        "large_straight":-1,
                        "yahtzee":-1,
                        "chance":-1
                    }
                },
        "turn_order": 1,
        "name": "N64-Reunion|mario_official" 
    }

    results = Scorecards.create(game_details["game_id"], game_details["user_id"], game_details["name"])
    print("Returned game-", results)