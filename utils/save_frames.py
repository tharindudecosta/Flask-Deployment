import os
import random
import cv2
import numpy as np
import matplotlib.pyplot as plt
import firebase_admin
from firebase_admin import credentials, firestore, storage
from ultralytics import YOLO
import sys
import uuid

sys.path.append(os.path.join(os.getcwd(), "utils", "YOLO-V8-CAM"))
from yolo_cam.eigen_cam import EigenCAM
from yolo_cam.utils.image import show_cam_on_image

# cred = credentials.Certificate("utils/blood-donation-ac142-firebase-adminsdk-i8oz1-23eb9eab7e.json")  # Path to your Firebase service account key
cred = credentials.Certificate("utils/blood-donation-ac142-firebase-adminsdk-i8oz1-44046042e9.json")  # Path to your Firebase service account key
firebase_admin.initialize_app(cred, {'storageBucket': 'blood-donation-ac142.appspot.com'})  # Your Firebase Storage bucket
db = firestore.client()
bucket = storage.bucket()

PROCESSED_FOLDER = r"processed_frames"
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Function to extract multiple random frames
def get_random_frames(video_path, num_frames, resize_shape=(832, 832)):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Error: Unable to open video")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        raise Exception("Error: The video has no frames")

    # Get unique random frame indices
    random_frame_indices = sorted(random.sample(range(total_frames), num_frames))
    frame_number = 0
    selected_frames = []
    rgb_imgs = []
    next_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_number == random_frame_indices[next_index]:
            resized_frame = cv2.resize(frame, resize_shape)
            rgb_imgs.append(resized_frame.copy())
            normalized_frame = np.float32(resized_frame) / 255
            selected_frames.append(normalized_frame)

            next_index += 1
            if next_index >= len(random_frame_indices):
                break

        frame_number += 1

    cap.release()

    if len(selected_frames) < num_frames:
        raise Exception("Error: Unable to extract the required number of frames")

    return selected_frames, rgb_imgs

def upload_to_firebase_storage(local_image_path, remote_path):
    try:
        # Upload the processed image to Firebase Storage
        blob = bucket.blob(remote_path)
        blob.upload_from_filename(local_image_path)
        
        # Make the image publicly accessible
        blob.make_public()
        
        # Return the public URL of the uploaded image
        return blob.public_url
    except Exception as e:
        print(f"Error uploading image to Firebase: {e}")
        return None

def generate_cam(video_path,user_email,num_frames):
    frames, rgb_imgs = get_random_frames(video_path,num_frames)
    # Load YOLO model
    model = YOLO("models/best_visual.pt") 
    model.cpu()
    target_layers = [model.model.model[-2]]

    cam = EigenCAM(model, target_layers, task="cls")
    uploaded_image_urls = []
    for i, (img, rgb_img) in enumerate(zip(frames, rgb_imgs)):
        grayscale_cam = cam(rgb_img)[0, :, :]
        cam_image = show_cam_on_image(img, grayscale_cam, use_rgb=True)

        # Save the processed frame locally
        unique_id = uuid.uuid4().hex[:10]  # Generate a random UID
        frame_filename = f"frame_{random.randint(1000, 9999)}_{unique_id}.jpg"
        filename = os.path.join(frame_filename)

        USER_SPECIFIC_OUTPUT = os.path.join(PROCESSED_FOLDER, f"{user_email}")
        os.makedirs(USER_SPECIFIC_OUTPUT, exist_ok=True)

        output_path = os.path.join(USER_SPECIFIC_OUTPUT, filename)
        plt.imsave(output_path, cam_image)

        # Upload the processed frame to Firebase Storage
        remote_path = f"VideoVerification/{user_email}/processed_frames/{filename}"
        public_url = upload_to_firebase_storage(output_path, remote_path)

        if public_url:
            uploaded_image_urls.append(public_url)

        os.remove(output_path)
        


    # Remove the temporary files if needed
    # os.remove(output_path)

    return uploaded_image_urls
