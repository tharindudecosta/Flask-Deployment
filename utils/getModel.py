import boto3
import os

def getModel():
    bucket_name = "deepfake-project-bucket"
    model_key = "models/best.pt"
    local_path = "models/best.pt"

    os.makedirs("models", exist_ok=True)

    s3 = boto3.client('s3')
    s3.download_file(bucket_name, model_key, local_path)