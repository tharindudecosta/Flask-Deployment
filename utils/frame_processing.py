import os
import shutil
import cv2
import uuid

def extract_frames(video_path, output_folder,video_name, frame_rate=1):
    shutil.rmtree(output_folder, ignore_errors=True)
    os.makedirs(output_folder, exist_ok=True)

    # cap = cv2.VideoCapture(video_path)
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # interval = int(fps / frame_rate)
    # frame_id = 0
    
    # while cap.isOpened():
    #     ret, frame = cap.read()
    #     if not ret:
    #         break
    #     if frame_id % interval == 0:
    #         unique_id = uuid.uuid4().hex[:10]  # Generate a random UID
    #         frame_path = os.path.join(output_folder, f"frame_{video_name}_{frame_id}_{unique_id}.jpg")
    #         cv2.imwrite(frame_path, frame)
    #     frame_id += 1


    cap = cv2.VideoCapture(video_path)
    os.makedirs(output_folder, exist_ok=True)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        unique_id = uuid.uuid4().hex[:10]  # Generate a random UID
        frame_path = os.path.join(output_folder, f"frame_{video_name}__{unique_id}.jpg")
        cv2.imwrite(frame_path, frame)

    cap.release()
    return sorted(os.listdir(output_folder))