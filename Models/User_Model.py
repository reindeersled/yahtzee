#Reina Lin
import sqlite3
import random

class User:
    def __init__(self, db_name, table_name):
        print("user model constructor", db_name)
        self.db_name =  db_name
        self.max_safe_id = 9007199254740991 #maximun safe Javascript integer
        self.table_name = table_name
    
    def initialize_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    email TEXT UNIQUE,
                    username TEXT UNIQUE,
                    password TEXT
                );
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def exists(self, username=None, id=None): #true is for exists, false is for not
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if not username and not id: 
                return {"status": "error",
                        "data": "username and id not provided!"}
            
            if username:
                cursor.execute(f"SELECT * FROM {self.table_name} WHERE username = ?;", (username,))
                exists = cursor.fetchall()
                if len(exists) == 0:
                    return {"status":"success",
                            "data": False}
                else:
                    return {"status":"success",
                            "data": True}
            if id:
                cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?;", (id,))
                exists = cursor.fetchall()
                if len(exists) == 0:
                    return {"status":"success",
                            "data": False}
                else:
                    return {"status":"success",
                            "data": True}
            

            return {"status":"error",
                    "data":"did not provide a username or id!"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def create(self, user_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            user_id = random.randint(0, self.max_safe_id)

            if self.exists(id=user_id)["data"] == True:
                return {"status": "error",
                        "data": "id already exists"
                        }
            if self.exists(username=user_info["username"])["data"] == True:
                return {"status": "error",
                        "data": "username already exists"
                        }
            
            #other requirements
            for letter in user_info["username"]:
                if letter.isalpha() == False and letter.isdigit() == False and letter != '_' and letter != '-':
                    return {"status": "error",
                            "data": "bad username! no symbols or spaces"
                            }
            if len(user_info["password"]) < 8:
                return {"status": "error",
                        "data": "password too short, try again with a longer one"
                        } 
            if "@" not in user_info["email"] or "." not in user_info["email"]:
                return {"status": "error",
                        "data": "bad email, must contain @ and ."} 
            for chara in user_info["email"]:
                if chara == " ":
                    return {"status": "error",
                            "data": "bad email, no spaces allowed"}
            
            
            user_data = (user_id, user_info["email"], user_info["username"], user_info["password"])

            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", user_data)
            db_connection.commit()
            
            return {"status": "success",
                    "data": self.to_dict(user_data)
                    }
        except sqlite3.IntegrityError as e:
            return {"status":"error",
                    "data":"tried to insert duplicate columns"}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        
        finally:
            db_connection.close()
    
    def get(self, username=None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            
            if username:
                if self.exists(username=username)["data"] == False:
                    return {"status": "error",
                        "data": "player with this username does not exist!"}
            
                cursor.execute(f"SELECT * FROM {self.table_name} WHERE username = ?;", (username,))
                get_user = cursor.fetchone()
                return {"status":"success",
                        "data": self.to_dict(get_user)}
            
            if id:
                if self.exists(id=id)["data"] == False:
                    return {"status": "error",
                        "data": "player with this id does not exist!"}
                cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?;", (id,))
                get_user = cursor.fetchone()
                return {"status":"success",
                        "data": self.to_dict(get_user)}
            
            else:
                return {"status": "error",
                        "data": "no username or id given!"}

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
            users_data = cursor.fetchall() #list of tuples i think
            all_users = []
            for user_data in users_data:
                all_users.append(self.to_dict(user_data))

            return {"status":"success",
                    "data": all_users}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def update(self, user_info): #user info is a dict
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if not user_info:
                return {"status":"error",
                        "data":"no user info provided"}

            if self.exists(id=user_info["id"])["data"] == False:
                return {"status":"error",
                        "data": "this id doesn't exist!"}
            
            #return error if someone already has that username
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE username = ?;", (user_info["username"],))
            exists = cursor.fetchall()
            if len(exists) > 0:
                return {"status":"error",
                        "data": "someone already has this username!"}
            
            for letter in user_info["username"]:
                if letter.isalpha() == False and letter.isdigit() == False and letter != '_' and letter != '-':
                    return {"status": "error",
                            "data": "bad username! no symbols or spaces"
                            }
            if len(user_info["password"]) < 4:
                return {"status": "error",
                        "data": "password too short, try again with a longer one"
                        } 
            if "@" not in user_info["email"] or "." not in user_info["email"]:
                return {"status": "error",
                        "data": "bad email, probably invalid"} 

            
            cursor.execute(f"""UPDATE {self.table_name} 
                           SET email = ?, username = ?, password = ? 
                           WHERE id = ?;""", (user_info["email"], user_info["username"], user_info["password"], user_info["id"],))
            db_connection.commit()
            return {"status":"success",
                    "data": user_info}
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def remove(self, username): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if self.exists(username=username)["data"] == False:
                return {"status": "error",
                        "data": "player with this username does not exist!"}
            
            deleted_user_info = self.get(username=username)["data"]
            
            cursor.execute(f"DELETE FROM {self.table_name} WHERE username=?;", (username,))
            db_connection.commit()
            return {"status":"success",
                    "data": deleted_user_info}
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def to_dict(self, user_tuple):
        '''Utility function which converts the tuple returned from a SQLlite3 database
           into a Python dictionary
        '''
        user_dict={}
        if user_tuple:
            user_dict["id"]=user_tuple[0]
            user_dict["email"]=user_tuple[1]
            user_dict["username"]=user_tuple[2]
            user_dict["password"]=user_tuple[3]
        return user_dict

if __name__ == '__main__':
    import os
    print("Current working directory:", os.getcwd())
    DB_location=f"{os.getcwd()}/Models/yahtzeeDB.db"
    table_name = "users"
    
    Users = User(DB_location, table_name) 
    Users.initialize_table()

    user_details={
        "email":"justin.gohde@trinityschoolnyc.org",
        "username":"justingohde",
        "password":"123TriniT"
    }
    results = Users.create(user_details)

    updated_user_info={
        "id": 1708164685697912,
        "email":"reina.lin26@trinityschoolnyc.org",
        "username": "reinalin",
        "password": "something"
    }
    check = Users.create(updated_user_info)
    print("check", check)