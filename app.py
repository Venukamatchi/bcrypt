from flask import Flask, request, redirect, url_for, render_template, g, session
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session
DATABASE = "users.db"

# ---------- DB SETUP ----------
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS User (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        db.commit()

# ---------- ROUTES ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode("utf-8")
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        db = get_db()
        try:
            db.execute("INSERT INTO User (username, password_hash) VALUES (?, ?)", (username, hashed))
            db.commit()
            return redirect("/login")
        except sqlite3.IntegrityError:
            return "Username already exists!"
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM User WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode("utf-8"), user[2]):
            session["username"] = username
            return render_template("welcome.html")
        else:
            return "Invalid credentials ❌"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    username = session.get("username")
    if not username:
        return redirect("/login")
    return render_template("dashboard.html", username=username)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")

# ---------- MAIN ----------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)