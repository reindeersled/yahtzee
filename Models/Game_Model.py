#Reina Lin
import sqlite3
import random

class Game:
    def __init__(self, db_name, table_name):
        self.db_name =  db_name
        self.max_safe_id = 9007199254740991 
        self.table_name = table_name #"games"
    
    def initialize_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    name TEXT UNIQUE,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    finished TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def exists(self, game_name=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if game_name:
                cursor.execute(f"SELECT * FROM {self.table_name} WHERE name = ?;", (game_name,))
                exists = cursor.fetchall()
                if len(exists) > 0:
                    return {"status":"success",
                                "data": True}
                else:
                    return {"status":"success",
                            "data": False}
            
            else:
                return {"status":"error",
                        "data": "no game name or id provided"}
            
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def create(self, game_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            game_id = random.randint(0, self.max_safe_id)

            if self.exists(game_name=game_info["name"])["data"] == True:
                return {"status": "error",
                        "data": "that game name already exists!"
                        }
            
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?;", (game_id,))
            exists = cursor.fetchall()
            if len(exists) > 0:
                return {"status": "error",
                        "data": "that game id already exists!"
                        }
            
            #other requirements
            for letter in game_info["name"]:
                if letter.isalpha() == False and letter.isdigit() == False and letter != '-' and letter != '_':
                    return {"status": "error",
                            "data": "bad name! no symbols or spaces"
                            }
            
            game_data = (game_id, game_info["name"])

            cursor.execute(f"INSERT INTO {self.table_name} (id, name) VALUES (?, ?);", game_data)
            db_connection.commit()

            cursor.execute(f"SELECT created, finished FROM {self.table_name} WHERE id = ?;", (game_id,))
            times = cursor.fetchone()
 
            created = times[0]
            finished = times[1]

            game_data = (game_id, game_info["name"], created, finished)
            
            return {"status": "success",
                    "data": self.to_dict(game_data)
                    }
        except sqlite3.IntegrityError as e:
            return {"status":"error",
                    "data":"tried to insert duplicate columns"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        
        finally:
            db_connection.close()
    
    def get(self, id=None, game_name=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if id:       
                cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?;", (id,))
                get_game = cursor.fetchone()
                if get_game == None:
                    return {"status":"error",
                        "data": "no game found with that id"}
                else:
                    return {"status":"success",
                        "data": self.to_dict(get_game)}
            
            if game_name:
                if self.exists(game_name=game_name)["data"] == False:
                    return {"status": "error",
                            "data": "game with this name does not exist!"}
            
                cursor.execute(f"SELECT * FROM {self.table_name} WHERE name = ?;", (game_name,))
                get_game = cursor.fetchone()
                return {"status":"success",
                        "data": self.to_dict(get_game)}
            
            else:
                return {"status": "error",
                        "data": "no game name given!"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    
    def get_all(self): #returns list of dictionaries i think
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            
            cursor.execute(f"SELECT * FROM {self.table_name};")
            games_data = cursor.fetchall() #list of tuples i think
            all_games = []
            for game_data in games_data:
                all_games.append(self.to_dict(game_data))

            return {"status":"success",
                    "data": all_games}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()


    def update(self, game_info): #game info is a dict 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if not game_info:
                return {"status":"error",
                        "data":"no game info provided"}

            if self.get(id=game_info["id"])["status"] == "error":
                return {"status":"error",
                        "data": "id probably doesn't exist"}
            
            original_game = self.get(id=game_info['id'])["data"]
            if game_info["name"] != original_game["name"]:
                if self.exists(game_name=game_info["name"])["data"] == True:
                    return {"status":"error",
                            "data": "another game already has this name!"}
            
            cursor.execute(f"UPDATE {self.table_name} SET name = ?, finished = ? WHERE id = ?;", (game_info["name"], game_info["finished"], game_info["id"],))
            db_connection.commit()
            return {"status":"success",
                    "data": game_info}
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()


    def remove(self, game_name): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if self.exists(game_name=game_name)["data"] == False:
                return {"status": "error",
                        "data": "game with this name does not exist!"}
            
            deleted_game_info = self.get(game_name=game_name)["data"]
            
            cursor.execute(f"DELETE FROM {self.table_name} WHERE name=?;", (game_name,))
            db_connection.commit()
            return {"status":"success",
                    "data": deleted_game_info}
        
        except sqlite3.Error as error:
            return {"status": "error",
                    "data":error}
        finally:
            db_connection.close()

    def is_finished(self, game_name=None):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if game_name:
                if self.exists(game_name=game_name)["data"] == False:
                    return {"status": "error",
                            "data": "game with this name does not exist!"}

                finished_game = self.get(game_name=game_name)["data"] #should be dict      
                if finished_game["created"] != finished_game["finished"]:
                    return {"status": "success",
                            "data": True}
                else:
                    return {"status": "success",
                            "data": False}
            else:
                return {"status": "error",
                            "data": "no game name provided"}
        
        except sqlite3.Error as error:
            return {"status": "error",
                    "data":error}
        finally:
            db_connection.close()
    

    def to_dict(self, game_info):
        game_dict={}
        if game_info:
            game_dict["id"]=game_info[0]
            game_dict["name"]=game_info[1]
            game_dict["created"]=str(game_info[2])
            game_dict["finished"]=str(game_info[3])
        return game_dict

if __name__ == '__main__':
    import os
    #print("Current working directory:", os.getcwd())
    DB_location=f"{os.getcwd()}/yahtzeeDB.db"
    #print("location", DB_location)
    Games = Game(DB_location, "games")
    Games.initialize_table()

    game_details={
        "name":"ourGame4",
    }
    results = Games.is_finished(game_details["name"])
    print("Returned game-", results)

