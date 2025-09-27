import boto3
import json
def list_sns_topics_with_lambda_subs(region='us-east-1'):
    sns = boto3.client('sns', region_name=region)
    lambda_arns = []

    paginator = sns.get_paginator('list_topics')

    for page in paginator.paginate():
        for topic in page['Topics']:
            topic_arn = topic['TopicArn']
            subs = sns.list_subscriptions_by_topic(TopicArn=topic_arn)['Subscriptions']
            for sub in subs:
                if sub['Protocol'] == 'lambda':
                    lambda_arns.append({
                        'TopicArn': topic_arn,
                        'LambdaFunctionArn': sub['Endpoint'],
                        'SubscriptionArn': sub['SubscriptionArn']
                    })

    return lambda_arns


# Print the results
if __name__ == '__main__':
    result = list_sns_topics_with_lambda_subs()
    print(json.dumps(result, indent=2))
