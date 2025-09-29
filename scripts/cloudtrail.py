import boto3

client = boto3.client('cloudtrail')

response = client.describe_trails()
trails = response.get('trailList', [])

if not trails:
    print("No CloudTrail trails found.")
else:
    for trail in trails:
        print(f"Trail Name: {trail['Name']}")
        print(f"  - S3 Bucket: {trail.get('S3BucketName', 'N/A')}")
        print(f"  - Is Multi-region: {trail.get('IsMultiRegionTrail')}")
        print(f"  - Home Region: {trail.get('HomeRegion')}")
        print(f"  - Log Group ARN: {trail.get('CloudWatchLogsLogGroupArn', 'N/A')}")
        status = client.get_trail_status(Name=trail['Name'])
        print(f"{trail['Name']} Logging: {status['IsLogging']}")
        print("------")
