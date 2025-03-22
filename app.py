from flask import Flask, render_template, jsonify, request, session
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for sessions

@app.route('/')
def index():
    # Initialize streak tracking
    if 'streak' not in session:
        session['streak'] = 0
        session['last_played'] = None
        session['longest_streak'] = 0

    return render_template('index.html', streak=session['streak'], longest_streak=session['longest_streak'])

def update_streak():
    """Update the user's streak based on last played date."""
    today = datetime.utcnow().date()
    
    last_played = session.get('last_played')
    if last_played:
        last_played = datetime.strptime(last_played, "%Y-%m-%d").date()

        if last_played == today:
            return  # Already played today, no change
        elif last_played == today - timedelta(days=1):
            session['streak'] += 1  # Continue streak
        else:
            session['streak'] = 1  # Reset streak

    else:
        session['streak'] = 1  # First time playing

    session['longest_streak'] = max(session['longest_streak'], session['streak'])
    session['last_played'] = today.strftime("%Y-%m-%d")

@app.route('/tictactoe')
def tictactoe():
    update_streak()  # Update streak when game is played
    return render_template('tictactoe.html', streak=session['streak'], longest_streak=session['longest_streak'])

@app.route('/colorguess')
def colorguess():
    update_streak()
    return render_template('colorguess.html', streak=session['streak'], longest_streak=session['longest_streak'])

@app.route('/numberguess')
def numberguess():
    update_streak()
    return render_template('numberguess.html', streak=session['streak'], longest_streak=session['longest_streak'])

@app.route('/guessword')
def guessword():
    update_streak()
    return render_template('guessword.html', streak=session['streak'], longest_streak=session['longest_streak'])

@app.route('/games')
def games():
    update_streak()
    return render_template('games.html', streak=session['streak'], longest_streak=session['longest_streak'])

@app.route('/get_streak')
def get_streak():
    """Send the current streak data to the frontend via JSON."""
    return jsonify({
        "streak": session.get('streak', 0),
        "longest_streak": session.get('longest_streak', 0)
    })

if __name__ == '__main__':
    app.run(debug=True)