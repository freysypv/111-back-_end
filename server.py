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


# GET Http://127.0.0.1:5000/api/users/2

@app.get('/api/users/<int:user_id>')
def get_user_by_id(user_id):
    #logic here
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row # allows columns values to be retrieved by name, row = ["username"]
    cursor = connection.cursor()
    cursor.execute("SELECT id username FROM users WHERE id=?", (user_id,)) # the * print all collumns but by beun expesific we can get exacly what we need.
    row = cursor.fetchone()
    print(row)
    print(dict(row))
    user_information = dict(row)
    connection.close()

    return jsonify({
        "success": "true",
        "message": "user successfuly retrived",
        "data": user_information
    }), 201 #ok


#GET http://127.0.0.1:5000/api/users
@app.get('/api/users')
def get_users():
    #logic here 
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row #
    cursor = connection.cursor()
    cursor.execute("SELECT id, username FROM users")
    rows = cursor.fetchall()
    print(rows)
    # print(dict(row))
    connection.close()

    users = []
    for row in rows:
        print (dict(row))
        users.append(dict(row))

    return jsonify({
        "success": True,
        "message": "user access successful",
        "data": users
    }), 200


#put
@app.put('/api/users/<int:user_id>')
def update_user(user_id):
    updated_user = request.get_json()
    username = updated_user["username"]
    password = updated_user["password"]

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
  
    # VALIDATION
    cursor.execute("""SELECT * FROM users WHERE id=?""", (user_id,))
    row = cursor.fetchone()
    if not row:
        connection.close()
        return jsonify({
            "success": False,
             "message": "user not found"
    }), 404

    cursor.execute("""UPDATE users SET username=?, password=?, WHERE id=?""", (username,password,user_id))
    connection.commit()
    connection.close()

    return jsonify({
        "success": "True",
        "message": "User updated successfully"
                    
      }), 200



#DELETE
@app.delete('/api/users/<int:user_id>')
def delete_user(user_id):
    #logic here 
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    connection.commit()
    connection.close()

    return jsonify({
    "success":"True",
    "message": "User deleted successfully"
    })


# expenses functions


#http://127.0.0.1:5000/api/expenses
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

# Get /api/expenses
@app.get('/api/expenses')
def get_expenses():
    #logic
    connection = sqlite3.connect(DB_NAME) 
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, description, amount, date, category FROM expenses")
    rows = cursor.fetchall()
    # print(rows)
    connection.close()

    expenses = []
    for row in rows:
        print(dict(row))
        expenses.append(dict(row))


   
    return jsonify({
            "success": True,
            "message": "Expenses reprieved successfully",
            "data": expenses
        }), 200
    
    #GET /api/expenses/
    #GET Http://127.0.0.1:5000/api/
@app.get('/api/expenses/<int:expense_id>')
def get_expenses_by_id(expense_id):
    #logic
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id=?", (expense_id,))
    row = cursor.fetchone()
    print(row)
    print(dict(row))
    expense_information = (dict(row))
    connection.close()

    return jsonify({
        "success": True,
        "message":  "Expenses successfully retrived",
        "data": expense_information

    }), 201 #ok

#put /api/expenses/<expenses_id>
#http://127.0.0.1:5000/api/expenses/

@app.put('/api/expenses/<int:expense_id>')
def update_expense(expense_id):
    updated_expense = request.get_json()
    title = updated_expense["title"]
    description = updated_expense["description"]
    amount = updated_expense["amount"]
    date = updated_expense["date"]
    category = updated_expense["category"]

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    #validation
    cursor.execute("""SELECT * FROM users WHERE id=?""", (expense_id,))    
    row = cursor.fetchone()
    if not row:
        connection.close()
        return jsonify({
        "success": False,
        "message": "expense not found"
    }),404


    cursor.execute("""UPDATE expenses SET title=?, description=?, amount=?, date=?, category=? WHERE id=?""", (title, description, amount, date, category, expense_id))
    connection.commit()
    connection.close()

    return jsonify({
        "success": "True",
        "message": "Expenses updated successfully"
    }), 200

    
    

# http://127.0.0.1:5000/api/expenses
#DELETE expenses
@app.delete('/api/expenses/<int:expense_id>')
def delete_expense(expense_id):
    #logic here 
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
   
    # VALIDATION
    cursor.execute("""SELECT id FROM expenses WHERE id=?""", (expense_id,))
    row = cursor.fetchone()
    if not row:
        return jsonify({
            "success": False,
            "message": "expense not found"
    }),404

    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    connection.commit()
    connection.close()

    return jsonify({
    "success":"True",
    "message": "expenses deleted successfully"
    }), 200
    


if __name__ == '__main__':
    init_db()
    app.run(debug=True)