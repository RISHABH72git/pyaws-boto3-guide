import boto3

client = boto3.client("elasticache", region_name="us-east-1")
response = client.describe_serverless_caches()
print("Found Serverless Redis Caches:\n")

for cache in response.get("ServerlessCaches", []):
    print(f"Name           : {cache['ServerlessCacheName']}")
    print(f"Engine         : {cache['Engine']}")
    print(f"Endpoint       : {cache['Endpoint']['Address']}:{cache['Endpoint']['Port']}")
    print(f"Status         : {cache['Status']}")
    print(f"ARN            : {cache['ARN']}")
    print(f"Subnet Group   : {cache.get('SubnetGroupName', 'N/A')}")
    print(f"Auth Enabled   : {cache.get('TransitEncryptionEnabled', True)}")
    print("-" * 50)
