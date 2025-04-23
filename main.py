from flask import Flask
import os
from utils.getModel import getModel
from routes.video_analysis import video_analysis_blueprint 

app = Flask(__name__)
app.register_blueprint(video_analysis_blueprint)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed_frames"

os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
getModel()

@app.route('/home')
def home():
    return "Welcome All"
    
@app.route('/test', methods=['POST'])
def predict():
    return "this is a test"
    
# GitAction WorkFlow is successfully doing it;s job!!

# app.run(port=5008, debug=True)