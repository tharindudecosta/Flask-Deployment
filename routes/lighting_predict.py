from flask import Blueprint, request, jsonify
import os
import torch
import cv2
from torchvision.transforms import ToTensor
from tqdm import tqdm
from utils.lighting_model import load_model
from utils.color_correction import ace_color_constancy
import time

predict_blueprint = Blueprint("predict", __name__)

PROCESSED_FRAMES = "frames"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model path

def predict_video(video_path, video_name, user_email):
    model = load_model("models/lighting_model.pth", device)

    transform = ToTensor()
    fake_count = 0
    real_count = 0

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = 30  # You can adjust this
    interval = int(fps / frame_rate)
    frame_id = 0

    # Initialize tqdm progress bar
    pbar = tqdm(total=total_frames, desc="Processing Frames", unit="frame")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % interval == 0:
            image = frame
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

        frame_id += 1
        pbar.update(1)  # Update progress by 1 frame

    pbar.close()
    cap.release()

    sampled_frame_count = fake_count + real_count
    scaling_factor = total_frames / sampled_frame_count if sampled_frame_count > 0 else 1

    estimated_fake_count = int(fake_count * scaling_factor)
    estimated_real_count = int(real_count * scaling_factor)
    estimated_total_count = estimated_fake_count + estimated_real_count

    result = "Fake" if estimated_fake_count > estimated_real_count else "Real"

    return result, estimated_fake_count, estimated_real_count, estimated_total_count


@predict_blueprint.route("/api/predictLightning", methods=["POST"])
def predict():
    try:
        start_time = time.time()
        print("Files received:", request.files)
        print("Form received:", request.form)
        if "video" not in request.files or request.files["video"].filename == "":
            print("Video Missing")
            return jsonify({"error": "No video file provided"}), 400
        
        # Get the user's email (optional)
        user_email = request.form.get("email")
        if not user_email:
            print("Email Missing")
            return jsonify({"error": "Email is required"}), 400
        UPLOAD_FOLDER = "uploads"

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
