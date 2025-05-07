import boto3
from botocore.exceptions import ClientError

def list_buckets(s3_client):
    response = s3_client.list_buckets()
    return [bucket["Name"] for bucket in response.get("Buckets", [])]

def print_bucket_info(s3_client):
    buckets = list_buckets(s3_client)
    for bucket in buckets:
        print(f"Bucket: {bucket}")
        try:
            policy = s3_client.get_bucket_policy(Bucket=bucket)
            print(f"  Policy: {policy['Policy']}")
        except ClientError as e:
            # Check if the error is due to missing bucket policy
            if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
                print("  No policy found.")
            else:
                print(f"  Unexpected error: {e}")
