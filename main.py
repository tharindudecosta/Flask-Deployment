from flask import Flask
import os
from utils.getModel import getDeepfakeModel,getVisualizationModel
from routes.video_analysis import video_analysis_blueprint 
from routes.cam_generator import cam_blueprint

app = Flask(__name__)
app.register_blueprint(video_analysis_blueprint)
app.register_blueprint(cam_blueprint)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed_frames"

os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
getDeepfakeModel()
getVisualizationModel()

@app.route('/home')
def home():
    return "Welcome All"
    
@app.route('/test', methods=['POST'])
def predict():
    return "this is a test"
    
# GitAction WorkFlow is successfully doing it;s job!!

app.run(port=5008, debug=True)