from flask import Flask, request, g
import sqlite3

app = Flask(__name__)
DATABASE = "users.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/search")
def search():
    username = request.args.get("username", "")
    db = get_db()
    cursor = db.cursor()
    
    # Vulnerable SQL query (concatenating user input directly)
    query = f"SELECT * FROM users WHERE username = '{username}'"
    print(f"Executing query: {query}")  # Debugging purposes
    cursor.execute(query)
    results = cursor.fetchall()
    
    return {"results": results}

if __name__ == "__main__":
    app.run(debug=True)