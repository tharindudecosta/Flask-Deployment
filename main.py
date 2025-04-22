from flask import Flask
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed_frames"

os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/home')
def home():
    return "Welcome All"
    
# GitAction WorkFlow is successfully doing it;s job!!


#app.run(port=5008, debug=True)