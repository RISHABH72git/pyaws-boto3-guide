import boto3

ec2 = boto3.client('ec2')

response = ec2.describe_key_pairs()

print("AWS Key Pairs Found:")
for key in response['KeyPairs']:
    key_name = key['KeyName']
    key_fingerprint = key.get('KeyFingerprint', 'N/A')
    key_type = key.get('KeyType', 'N/A')
    print(f"- Key Name      : {key_name}")
    print(f"  Fingerprint   : {key_fingerprint}")
    print(f"  Key Type      : {key_type}")
    print()