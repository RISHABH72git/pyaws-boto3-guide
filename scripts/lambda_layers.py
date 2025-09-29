import boto3

client = boto3.client('lambda')

def list_all_lambda_layers():
    paginator = client.get_paginator('list_layers')
    page_iterator = paginator.paginate()

    for page in page_iterator:
        for layer in page['Layers']:
            print("="*50)
            print(f"Layer Name      : {layer['LayerName']}")
            print(f"Latest Version  : {layer['LatestMatchingVersion']['Version']}")
            print(f"Description     : {layer['LatestMatchingVersion'].get('Description', 'No description')}")
            print(f"Created Date    : {layer['LatestMatchingVersion']['CreatedDate']}")
            print(f"Compatible Runtimes: {layer['LatestMatchingVersion'].get('CompatibleRuntimes', [])}")
            print(f"ARN             : {layer['LatestMatchingVersion']['LayerVersionArn']}")
            print("="*50 + "\n")

list_all_lambda_layers()
