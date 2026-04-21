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
    


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT NOT NULL,
            date TEXT,
            amount INTEGER NOT NULL,
            category TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)      
        )
    """)
    
    connection.commit()# save changes to the D.B
    connection.close()# close the connection to the D.B




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

#http://127.0.0.1:5000/api/coupons
@app.post('/api/expenses')
def create_expenses():
    #logic here
    new_expense = request.get_json()
    print(new_expense)

    title = new_expense["title"]
    description = new_expense["description"]
    amount = new_expense["amount"]
    date = new_expense["date"]
    category = new_expense["category"]
    user_id = new_expense["user_id"]

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO expenses (title, description, amount, date, category, user_id)
          VALUES(?, ?, ?, ?, ?, ?)""",(title, description, amount, date, category, user_id))
    
    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Expenses created successfully"
    }), 201

if __name__ == '__main__':
    init_db()
    app.run(debug=True)