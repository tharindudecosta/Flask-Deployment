import boto3
import os

import os
import boto3

def getModel():
    bucket_name = "deepfake-project-bucket"
    model_key = "models/best.pt"
    local_path = "models/best.pt"

    os.makedirs("models", exist_ok=True)

    if not os.path.isfile(local_path):
        print("Model not found locally. Downloading from S3...")
        s3 = boto3.client('s3')
        s3.download_file(bucket_name, model_key, local_path)
        print("Model downloaded successfully.")
    else:
        print("Model already exists locally. Skipping download.")
