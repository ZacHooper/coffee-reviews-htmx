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


def get_active_coffees(bucket: str) -> list[dict]:
    """Get the active coffees from S3"""
    s3 = boto3.client("s3")
    key = "coffees.json"
    # Download the coffees.json file
    all_coffees_raw = s3.get_object(Bucket=bucket, Key=key)

    # Load the JSON
    all_coffees = json.loads(all_coffees_raw["Body"].read())

    # Filter for active coffees
    active_coffees = [coffee for coffee in all_coffees if coffee["active"]]
    return active_coffees
