import boto3

# Replace with your Lambda log group name
LOG_GROUP = '/aws/lambda/test'
def get_latest_log_stream_name(log_group):
    logs = boto3.client('logs')
    response = logs.describe_log_streams(
        logGroupName=log_group,
        orderBy='LastEventTime',
        descending=True,
        limit=1
    )
    if not response['logStreams']:
        raise Exception("No log streams found.")
    return response['logStreams'][0]['logStreamName']

def get_last_log_events(log_group, log_stream, limit=5):
    logs = boto3.client('logs')
    response = logs.get_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        limit=limit,
        startFromHead=False  # Fetch latest logs
    )
    print(response)
    return [event['message'] for event in response['events']]

def main():
    try:
        log_stream = get_latest_log_stream_name(LOG_GROUP)
        print(f"Latest log stream: {log_stream}")

        logs = get_last_log_events(LOG_GROUP, log_stream, limit=50)
        print("\n🔹 Last 5 log messages:\n")
        for line in logs:
            print(line)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
