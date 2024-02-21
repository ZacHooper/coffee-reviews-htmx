import boto3
import json
import uuid


def upload_review(review: dict, bucket: str) -> bool:
    """Uploads a review to S3"""
    s3 = boto3.client("s3")
    key = f"{uuid.uuid4()}.json"
    try:
        s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(review))
        return True
    except Exception as e:
        print(e)
        return False
