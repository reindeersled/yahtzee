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

            # Check if the user already has a scorecard for this game
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE card_id = ? AND user_id = ?", (card_id, user_id,))
            existing_user_scorecard = cursor.fetchall()
            if existing_user_scorecard:
                return {"status": "error", 
                        "data": "User already has a scorecard for this game"}

            cursor.execute(f"SELECT * FROM {self.table_name} WHERE card_id = ?", (card_id,))
            existing_scorecards = cursor.fetchall()

            # Check if there are already 4 scorecards (players)
            if len(existing_scorecards) > 3:
                return {"status": "error", 
                        "data": "Too many players already in this game"}
            else:
                turn_order = len(existing_scorecards) + 1

                categories = json.dumps(self.create_blank_score_info())
                cursor.execute(f"INSERT INTO {self.table_name} (id, card_id, user_id, categories, turn_order, name) VALUES (?, ?, ?, ?, ?, ?);",
                            (scorecard_id, card_id, user_id, categories, turn_order, name,))
                db_connection.commit()

                card_tuple = (scorecard_id, card_id, user_id, categories, turn_order, name)

                return {"status": "success", "data": self.to_dict(card_tuple)}

        except sqlite3.Error as error:
            return {"status": "error", "data": str(error)}

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
                            "data": "No card found"}
            
            if id:
                cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?;", (id,))
                card_info = cursor.fetchone()  

                if card_info:
                    return {"status": "success",
                            "data": self.to_dict(card_info)}  #
                else:
                    return {"status": "error",
                            "data": "No card found"}
            
            return {"status": "error",
                    "data": "No name or id given"}

        except sqlite3.Error as error:
            return {"status": "error",
                    "data": str(error)} 
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
    
    def get_all_game_scorecards(self, game_name:str): #4 games max, 1 scorecard each
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if game_name:
                g_name = game_name.split('|')[0]
                game_id = cursor.execute(f"SELECT id FROM {self.card_table_name} WHERE name = ?;", (g_name,)).fetchall()

                if len(game_id) == 0:
                    return {"status": "success",
                            "data": game_id}
                else:
                    game_id = game_id[0]

                cursor.execute(f"SELECT * FROM {self.table_name} INNER JOIN {self.card_table_name} ON {self.table_name}.card_id = ?;", (game_id,))
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

    def get_all_game_usernames(self, game_name:str): #wow there is such an easier way to do this... select the second part from names in scorecard, those are the usernames bro
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if game_name:

                usernames = []

                exists = cursor.execute(f"SELECT * FROM {self.table_name} WHERE name = ?;", (game_name,)).fetchall()
                if len(exists) == 0:
                    return {"status": "success",
                            "data": usernames}
                
                g_name = game_name.split('|')[0]
                game_id = cursor.execute(f"SELECT id from {self.card_table_name} WHERE name = ?;", (g_name,)).fetchall()
                if len(game_id) == 0:
                    return {"status": "success",
                            "data": usernames}
                else: 
                    game_id = game_id[0]

                scorecard_names = cursor.execute(f"SELECT name FROM {self.table_name} WHERE card_id = ?;", (game_id,)).fetchall()
                for sc_name in scorecard_names:
                    usernames.append(sc_name[0].split('|')[1])

                return {"status":"success",
                        "data": usernames}
            else:
                return {"status":"error",
                        "data":"no card name given"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def get_all_user_game_names(self, username: str):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if username:
                cursor.execute(f"""
                    SELECT name 
                    FROM {self.table_name}
                    INNER JOIN {self.user_table_name} 
                    ON {self.table_name}.user_id = {self.user_table_name}.id
                    WHERE {self.user_table_name}.username = ?;
                """, (username,))

                game_names = cursor.fetchall()
                all_game_names = [game_name[0].split('|')[0] for game_name in game_names]

                return {
                    "status": "success",
                    "data": all_game_names
                }

            else:
                return {
                    "status": "error",
                    "data": "No username provided",
                }

        except sqlite3.Error as error:
            return {
                "status": "error",
                "data": str(error), 
            }
        finally:
            db_connection.close()

    def update(self, id, name=None, categories=None): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            
            cates = json.dumps(categories)

            if id:
                if self.get(id=id)["status"] == "error":
                    return {"status": "error",
                            "data": "There is no scorecard with that id"}
                cursor.execute(f"UPDATE {self.table_name} SET categories={cates} WHERE id={id};")
                db_connection.commit()
                return {
                    "status": "success",
                    "data": self.to_dict(self.get(id=id)["categories"])
                }
            if name:
                if self.get(name=name)["status"] == "error":
                    return {"status": "error",
                        "data": "There is no scorecard with that name"}
                cursor.execute(f"UPDATE {self.table_name} SET categories={cates} WHERE name={name};")
                db_connection.commit()
                return {
                    "status": "success",
                    "data": self.to_dict(self.get(name=name)["categories"])
                }
            else:
                return {
                    "status": "error",
                    "data": "No id or name provided for updating."
                }

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
                if self.get(id=id)["status"] == "error":
                    return {"status": "error",
                            "data": "no game exists at that id"}
                
                deleted_data = self.get(id=id)["data"] #a dict

                cursor.execute(f"DELETE FROM {self.table_name} WHERE id = {id};")
                db_connection.commit()

                return {"status": "success",
                        "data": deleted_data} 
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

    def tally_score(self, score_info):
        total_score = 0

        # Tally upper section
        upper_score = sum([score for score in score_info["upper"].values() if score != -1])
        total_score += upper_score

        # Add upper section bonus if total of upper section exceeds 63
        if upper_score >= 63:
            total_score += 35  # Upper section bonus

        # Tally lower section
        lower_score = sum([score for score in score_info["lower"].values() if score != -1])
        total_score += lower_score

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

    results = Scorecards.get_all_game_usernames(game_details["name"])
    print("Returned game-", results)
