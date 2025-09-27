import boto3


def list_sqs_with_lambda_triggers(region='ap-south-1'):
    lambda_client = boto3.client('lambda', region_name=region)
    sqs_client = boto3.client('sqs', region_name=region)

    # Get all queues
    queues = sqs_client.list_queues().get('QueueUrls', [])

    result = {}
    for queue_url in queues:
        attrs = sqs_client.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['QueueArn'])
        queue_arn = attrs['Attributes']['QueueArn']

        mappings = lambda_client.list_event_source_mappings(EventSourceArn=queue_arn)
        lambdas = []
        for m in mappings.get('EventSourceMappings', []):
            lambdas.append({
                "FunctionName": m['FunctionArn'],
                "UUID": m['UUID'],
                "State": m['State'],
                "LastModified": m.get('LastModified')
            })
        result[queue_url] = {
            "QueueArn": queue_arn,
            "LambdaTriggers": lambdas
        }

    return result


if __name__ == "__main__":
    details = list_sqs_with_lambda_triggers()
    for q, info in details.items():
        print(f"\nQueue URL: {q}")
        print(f" ARN: {info['QueueArn']}")
        if info['LambdaTriggers']:
            print(" Lambda-triggered functions:")
            for l in info['LambdaTriggers']:
                print(f"  - {l['FunctionName']} (State: {l['State']}, UUID: {l['UUID']})")
        else:
            print(" No Lambda triggers found.")
