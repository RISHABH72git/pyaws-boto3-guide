import boto3

client = boto3.client('cloudwatch')


def list_alarms():
    paginator = client.get_paginator('describe_alarms')
    for page in paginator.paginate():
        for alarm in page['MetricAlarms']:
            print(f"Name       : {alarm['AlarmName']}")
            print(f"State      : {alarm['StateValue']}")
            print(f"Metric     : {alarm['MetricName']}")
            print(f"Namespace  : {alarm['Namespace']}")
            print(f"Threshold  : {alarm['Threshold']}")
            print(f"Comparison : {alarm['ComparisonOperator']}")
            print(f"Period     : {alarm['Period']} seconds")
            print(f"Evaluation : {alarm['EvaluationPeriods']} periods")
            print("-" * 50)


if __name__ == '__main__':
    list_alarms()
