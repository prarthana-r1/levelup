from flask import Flask, render_template, jsonify, request, session
import random
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity,jwt_required, JWTManager
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime,timedelta

app = Flask(__name__)
CORS(app)

# Secret keys
app.config["SECRET_KEY"] = "levelupgame"  # Required for session
app.config["JWT_SECRET_KEY"] = "prarthanalevelup"  # JWT authentication
jwt = JWTManager(app)

# MongoDB Atlas Connection
client = MongoClient("mongodb+srv://prarthanainfoin:atlasprar@cluster0.gybms.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["levelup"]
users_collection = db["gameuser"]

# User Signup
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json

    if users_collection.find_one({"email": data["email"]}):
        return jsonify({"message": "Email already exists"}), 400

    # Make sure password is hashed correctly
    hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")
    print("✅ Hashed Password:", hashed_password)  # Debugging

    users_collection.insert_one({"name": data["name"],"email": data["email"], "password": hashed_password})
    
    return jsonify({"message": "User registered successfully"}), 201


# Protected Route (For Testing)
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify({"message": "This is a protected route"}), 200

# Routes to Render HTML Pages
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET"])
def login_page():
    return render_template('login.html')

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        print("🔍 Received login request:", data)  # Debugging
        
        if not data or "email" not in data or "password" not in data:
            return jsonify({"message": "Invalid request data"}), 400

        user = users_collection.find_one({"email": data["email"]})
        print("📌 User found in DB:", user)  # Debugging

        if not user or not check_password_hash(user["password"], data["password"]):
            return jsonify({"message": "Invalid email or password"}), 401

        access_token = create_access_token(identity=data["email"])
        print("✅ Login successful, token generated")  # Debugging

        access_token = create_access_token(identity={
            "email": user["email"],
            "name": user["name"]
        })


        return jsonify({"token": access_token}), 200
    
        

    except Exception as e:
        print("❌ Error in /login:", str(e))  # Debugging
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500



@app.route('/tictactoe')
def tictactoe():
    return render_template('tictactoe.html')

@app.route('/colorguess')
def colorguess():
    return render_template('colorguess.html')

@app.route('/memorymatch')
def memorymatch():
    return render_template('memorymatch.html')

@app.route('/guessword')
def guessword():
    return render_template('guessword.html')

@app.route('/games')
def games():
    return render_template('games.html')

@app.route("/update_streak", methods=["POST"])
@jwt_required()
def update_streak():
    user_id = get_jwt_identity()
    data = request.json
    new_streak = data.get("streak")

    if not isinstance(new_streak, int):
        return jsonify({"error": "Invalid streak value"}), 400

    # Update user streak in MongoDB
    users_collection.update_one(
        {"_id": user_id},
        {"$set": {"streak": new_streak, "lastUpdated": datetime.datetime.utcnow()}},
        upsert=True
    )

    return jsonify({"message": "Streak updated successfully", "streak": new_streak})

# 🟢 API: Get Streak for Logged-in User
@app.route("/get_streak", methods=["GET"])
@jwt_required()
def get_streak():
    user_id = get_jwt_identity()
    user_data = users_collection.find_one({"_id": user_id}, {"streak": 1, "_id": 0})

    if user_data:
        return jsonify({"streak": user_data.get("streak", 0)})
    else:
        return jsonify({"streak": 0})  # Default if user has no streak

if __name__ == '__main__':
    app.run(debug=True)
