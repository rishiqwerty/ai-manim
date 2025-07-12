import boto3
import io
import os

def upload_code_to_s3(file_content, s3_key):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name=os.environ["AWS_REGION"]
    )

    bucket_name = os.environ["AWS_BUCKET_NAME"]

    s3.upload_fileobj(io.BytesIO(file_content.encode()), bucket_name, s3_key)

    s3_url = f"https://{bucket_name}.s3.{os.environ['AWS_REGION']}.amazonaws.com/{s3_key}"
    return s3_url

def upload_file_to_s3(local_file_path, s3_key):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name=os.environ["AWS_REGION"]
    )

    bucket_name = os.environ["AWS_BUCKET_NAME"]

    s3.upload_file(local_file_path, bucket_name, s3_key)

    s3_url = f"https://{bucket_name}.s3.{os.environ['AWS_REGION']}.amazonaws.com/{s3_key}"
    return s3_url
