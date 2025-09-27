import boto3
from datetime import datetime, timedelta

lambda_function_name = "demo-lambda"
client = boto3.client('cloudwatch')
end_time = datetime.utcnow()
start_time = end_time - timedelta(days=1)

metrics = ["Invocations", "Errors", "Throttles", "Duration", "ConcurrentExecutions"]
for metric in metrics:
    response = client.get_metric_statistics(
        Namespace='AWS/Lambda',
        MetricName=metric,
        Dimensions=[{'Name': 'FunctionName', 'Value': lambda_function_name}],
        StartTime=start_time,
        EndTime=end_time,
        Period=60,
        Statistics=['Sum', 'Average', 'Maximum']
    )

    print(f"\n🔹 Metric: {metric}")
    for datapoint in sorted(response['Datapoints'], key=lambda x: x['Timestamp']):
        print(
            f"{datapoint['Timestamp']} | Sum: {datapoint.get('Sum')} | Avg: {datapoint.get('Average')} | Max: {datapoint.get('Maximum')}")
