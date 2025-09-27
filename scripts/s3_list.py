import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')


def is_public(bucket_name):
    try:
        pab = s3.get_public_access_block(Bucket=bucket_name)
        config = pab['PublicAccessBlockConfiguration']
        if all(config.values()):
            return False
    except ClientError:
        pass

    try:
        policy = s3.get_bucket_policy_status(Bucket=bucket_name)
        return policy['PolicyStatus']['IsPublic']
    except ClientError:
        return False


def list_public_buckets():
    buckets = s3.list_buckets()['Buckets']
    print("🔎 Public Buckets:\n")
    for bucket in buckets:
        name = bucket['Name']
        print(f"✅ {name}")


if __name__ == "__main__":
    list_public_buckets()
