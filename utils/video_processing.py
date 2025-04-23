import tempfile
import os
import cv2
from ultralytics import YOLO
# from google.cloud import storage

# # Initialize the GCP Storage client
# storage_client = storage.Client()
# bucket = storage_client.bucket('deepfakemodel')

# # Function to load YOLO model from GCP Storage
# def load_yolo_model():
#     model_blob = bucket.blob('best.pt')
#     model_path = '/tmp/best.pt'
#     model_blob.download_to_filename(model_path)
#     model = YOLO(model_path)
#     return model

# Function to process video and detect fake frames
def process_video(video_file):
    # Load YOLO model
    # model = load_yolo_model()

    model_path = 'models/best.pt' 
    model = YOLO(model_path)
    # Save the uploaded video temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
        video_path = temp_video.name
        video_file.save(video_path)

    # Process video frames
    fake_frames = 0
    real_frames = 0
    total_frames = 0
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Run YOLOv8 detection on each frame
        results = model(frame)
        
        for result in results:
            for box in result.boxes:
                label = int(box.cls)
                if label == 1:  # Assuming '1' represents 'fake' class in your model
                    fake_frames += 1
                    break  # Move to the next frame after detecting a "fake" label

        total_frames += 1


        # probs = results[0].probs  # Extract probabilities for the first image

        # # Get the predicted class ID with the highest probability
        # predicted_class_id = probs.top1  # Class ID with the highest probability
        # confidence = probs.data[predicted_class_id]  # Confidence score for the prediction

        # # Get the class label
        # label = model.names[predicted_class_id]
        # print(f"Predicted Class: {label}, Confidence: {confidence:.2f}")
        
        # print(model.names)

        # if label == model.names[0]:
        #     fake_frames += 1
        # elif label == model.names[1]:
        #     real_frames += 1


    # total_frames = fake_frames + real_frames
    cap.release()
    os.remove(video_path)  # Clean up

    # Decide if the video is fake based on the proportion of "fake" frames
    fake_threshold = 0.5  # Adjust this threshold as needed
    is_fake = (fake_frames / total_frames) > fake_threshold
    real_frames = total_frames - fake_frames

    return "Fake" if is_fake else "Real", fake_frames, total_frames,real_frames
