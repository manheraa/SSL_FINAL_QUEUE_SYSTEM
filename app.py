from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "supersecretkey"

# --- MongoDB Setup ---
client = MongoClient("mongodb://localhost:27017/")
db = client["queueEase"]
tokens_collection = db["tokens"]
staff_collection = db["staff"]

# --- Flask-Login Setup --- Study 
login_manager = LoginManager()
login_manager.login_view = "home"
login_manager.init_app(app)

# --- Staff User Class --- 
class Staff(UserMixin):
    def __init__(self, id_, username):
        self.id = id_      # must be string
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    staff = staff_collection.find_one({"_id": ObjectId(user_id)})
    if staff:
        return Staff(str(staff["_id"]), staff["username"])
    return None

# --- Home Page ---
@app.route('/')
def home():
    today = datetime.now().strftime("%Y-%m-%d")
    login_error = request.args.get('login_error')
    return render_template('index.html', today=today, login_error=login_error)

# --- Staff Login ---
@app.route('/staff_login', methods=['POST'])
def staff_login():
    username = request.form.get("username")
    password = request.form.get("password")
    staff = staff_collection.find_one({"username": username})
    if staff and staff["password"] == password:  # plain text check
        user_obj = Staff(str(staff["_id"]), staff["username"])
        login_user(user_obj)
        return redirect(url_for("staff_dashboard"))
    else:
        return redirect(url_for("home") + "?login_error=1")

# --- Staff Logout ---
@app.route('/staff_logout')
@login_required
def staff_logout():
    logout_user()
    return redirect(url_for("home"))
