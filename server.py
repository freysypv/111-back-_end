from flask import Flask, jsonify,request

app = Flask(__name__)
import sqlite3

DB_NAME = "budget_manager.db" # aper cases ids costant
 


def init_db():
    connection = sqlite3.connect(DB_NAME) #Open a connectio to the D.B "budget_manager.db"
    cursor = connection.cursor() # Creates a cursor/tool that send commads (select, insert ...) to the D.B.

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL              
                   
                   )

""")
    
    connection.commit()# save changes to the D.B
    connection.close()# close the connection to the D>B




@app.get('/api/health')
def health_check():
    return jsonify({
        "status": "ok"
    }), 200


# ---users---
@app.post('/api/users')
def register():
    new_user = request.get_json()
    print(new_user)

    username = new_user["username"]
    password = new_user["password"]

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()# crerates a cursor/tool that lets you send commands (select, insert)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password)) # ? ? are the data caming from username , and userpassword (execute =s sql statement)

    connection.commit() # save changes to the D.B
    connection.close() # Close the connection to the D.B



    return jsonify({
        "success": True,
        "message": "user setup successful"
    }), 201


if __name__ == '__main__':
    init_db()
    app.run(debug=True)