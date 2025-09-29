import boto3

client = boto3.client('cloudtrail')

events = client.lookup_events(
    LookupAttributes=[
        {
            'AttributeKey': 'AccessKeyId',
            'AttributeValue': ''
        },
    ],
    MaxResults=1000
)

for event in events['Events']:
    print(event)