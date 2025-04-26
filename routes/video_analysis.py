from flask import Blueprint, request, jsonify
import os
from utils.video_processing import process_video
import time

video_analysis_blueprint = Blueprint("video_analysis", __name__)

UPLOAD_FOLDER = "uploads"

@video_analysis_blueprint.route("/api/analyzeVideo", methods=["POST"])
def analyze_video():
    start_time = time.time()
    print("Request init 2")

    if "video" not in request.files or request.files["video"].filename == "":
        print("Video Missing")
        return jsonify({"error": "No video file provided"}), 400

    # Get the user's email (optional)
    user_email = request.form.get("email")
    if not user_email or request.files["email"] == "":
        print("Email Missing")
        return jsonify({"error": "Email is required"}), 400

    print("Processing start 2")

    video = request.files["video"]
    
    print("Processing start 2")
    # Analyze video using the video processing function
    result, fake_count, total_count,real_count = process_video(video)
    end_time = time.time()
    total_time = end_time - start_time
    total_time = round(total_time, 2)
    
    return jsonify({
        "video": video.filename,
        "prediction": result,
        "fake_count": fake_count,
        "real_count":real_count,
        "total_count": total_count,
        "total_time":total_time
    }), 200
