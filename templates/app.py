from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_random_number')
def get_random_number():
    """Generate a random number from the Python backend"""
    number = random.randint(1, 100)
    return jsonify({"number": number})

@app.route('/check_guess', methods=['POST'])
def check_guess():
    """Check if the user's guess matches the secret number"""
    data = request.json
    user_guess = data.get('guess')
    secret_number = data.get('secret')
    
    if user_guess == secret_number:
        return jsonify({
            "correct": True,
            "message": "Correct! You guessed it!"
        })
    elif user_guess < secret_number:
        return jsonify({
            "correct": False,
            "message": "Too low! Try a higher number."
        })
    else:
        return jsonify({
            "correct": False,
            "message": "Too high! Try a lower number."
        })

if __name__ == '__main__':
    app.run(debug=True)