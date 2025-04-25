from flask import Blueprint, request, jsonify
import os
import torch
import cv2
from torchvision.transforms import ToTensor
from tqdm import tqdm
from models.lighting_model import load_model
from utils.frame_processing import extract_frames
from utils.color_correction import ace_color_constancy
import time

predict_blueprint = Blueprint("predict", __name__)

UPLOAD_FOLDER = "uploads"
PROCESSED_FRAMES = "frames"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model path

def predict_video(video_path,video_name,user_email):
    model = load_model("models/lighting_model.pth", device)

    USER_SPECIFIC_OUTPUT = os.path.join(PROCESSED_FRAMES, f"{user_email}")
    os.makedirs(USER_SPECIFIC_OUTPUT, exist_ok=True)

    frames = extract_frames(video_path, USER_SPECIFIC_OUTPUT,video_name)
    transform = ToTensor()
    fake_count = 0
    real_count = 0

    for frame in tqdm(frames, desc="Processing Frames"):
        frame_path = os.path.join(USER_SPECIFIC_OUTPUT, frame)
        image = cv2.imread(frame_path)
        processed = ace_color_constancy(image)
        difference = cv2.absdiff(image, processed)
        image_tensor = transform(image)
        difference_tensor = transform(difference)
        input_tensor = torch.cat((image_tensor, difference_tensor), dim=0).unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(input_tensor)
            _, predicted = torch.max(output, 1)

        if predicted.item() == 0:
            fake_count += 1
        else:
            real_count += 1
        
        total_count = fake_count + real_count

        os.remove(frame_path)


    return ("Fake" if fake_count > real_count else "Real"), fake_count, real_count,total_count

@predict_blueprint.route("/api/predictLightning", methods=["POST"])
def predict():
    try:
        start_time = time.time()
        if "video" not in request.files:
            return jsonify({"error": "No video file provided"}), 400
        
        user_email = request.form.get("email")

        if not user_email:
            return jsonify({"error": "Email is required"}), 400

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        video = request.files["video"]
        video_path = os.path.join(UPLOAD_FOLDER, video.filename)
        video.save(video_path)
        result, fake_count, real_count,total_count = predict_video(video_path,video.filename,user_email)
        os.remove(video_path)
        end_time = time.time()
        total_time = end_time - start_time
        total_time = round(total_time, 2)

        return jsonify({
            "video": video.filename,
            "prediction": result,
            "fake_count": fake_count,
            "real_count": real_count,
            "total_count":total_count,
            "total_time":total_time
        }), 200
    except Exception as e:
        print("An error occurred:", e)
