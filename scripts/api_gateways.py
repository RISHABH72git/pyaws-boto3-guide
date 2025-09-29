import boto3


def get_api_ids():
    client = boto3.client('apigateway', 'us-east-1')
    response = client.get_rest_apis()
    for item in response['items']:
        print(f"{item['name']} - {item['id']}")


if __name__ == "__main__":
    get_api_ids()
