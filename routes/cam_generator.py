from flask import Blueprint, request, jsonify
import os
from utils.save_frames import generate_cam
import time

cam_blueprint = Blueprint("generateCAM", __name__)

UPLOAD_FOLDER = "uploads"

@cam_blueprint.route("/api/generateCAM", methods=["POST"])
def generate_image():
    start_time = time.time()
    print("Request init 1")

    # Check for video file
    if "video" not in request.files or request.files["video"].filename == "":
        return jsonify({"error": "No video file provided"}), 400
    
    # Get number of frames
    num_frames = request.form.get("num_frames")
    try:
        num_frames = int(num_frames)
    except (TypeError, ValueError):
        num_frames = 5 

    user_email = request.form.get("email")
    if not user_email:
        return jsonify({"error": "Email is required"}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    video = request.files["video"]
    video_path = os.path.join(UPLOAD_FOLDER, f"temp_video_{video.filename}")
    video.save(video_path)

    saved_images = generate_cam(video_path, user_email, num_frames)
    os.remove(video_path)

    end_time = time.time()
    return jsonify({
        "processed_images": saved_images,
        "total_time": round(end_time - start_time, 2)
    }), 200
