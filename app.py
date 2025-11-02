from flask import Flask, render_template, request
import sqlite3
import os
from PIL import Image
import random

app = Flask(__name__)

# Folder where uploaded images will be saved
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Simulated emotion detection (temporary)
def detect_emotion(image_path):
    emotions = ['happy', 'sad', 'angry', 'surprised', 'neutral']
    emotion = random.choice(emotions)
    messages = {
        'happy': "You are smiling. You look happy today!",
        'sad': "You are frowning. Why are you sad?",
        'angry': "You look angry. Take a deep breath!",
        'surprised': "You look surprised! What happened?",
        'neutral': "You look calm and composed."
    }
    return emotion, messages[emotion]

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Upload route
@app.route('/upload', methods=['POST'])
def upload():
    name = request.form['name']
    email = request.form['email']
    image = request.files['image']

    # Save uploaded image
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)

    # Simulate emotion detection
    emotion, message = detect_emotion(image_path)

    # Save info in database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email, emotion, image_path) VALUES (?, ?, ?, ?)',
                   (name, email, emotion, image_path))
    conn.commit()
    conn.close()

    return render_template('index.html', message=message)

if __name__ == '__main__':
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

