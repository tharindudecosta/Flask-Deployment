import boto3
import os

def getDeepfakeModel():
    bucket_name = "deepfake-project-bucket"
    model_key = "models/best.pt"
    local_path = "models/best.pt"

    os.makedirs("models", exist_ok=True)

    if not os.path.isfile(local_path):
        print("Best.pt model not found locally. Downloading from S3...")
        s3 = boto3.client('s3')
        s3.download_file(bucket_name, model_key, local_path)
        print("Best.pt model downloaded successfully.")
    else:
        print("Best.pt model already exists locally. Skipping download.")

def getVisualizationModel():
    bucket_name = "deepfake-project-bucket"
    model_key = "models/best_visual.pt"
    local_path = "models/best_visual.pt"

    os.makedirs("models", exist_ok=True)

    if not os.path.isfile(local_path):
        print("Visualization model not found locally. Downloading from S3...")
        s3 = boto3.client('s3')
        s3.download_file(bucket_name, model_key, local_path)
        print("Visualization model downloaded successfully.")
    else:
        print("Visualization model already exists locally. Skipping download.")