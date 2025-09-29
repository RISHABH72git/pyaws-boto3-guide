import boto3

dynamodb = boto3.client('dynamodb')
lambda_client = boto3.client('lambda')
event_source = boto3.client('lambda')


def list_dynamodb_tables_and_triggers():
    tables_info = []

    paginator = dynamodb.get_paginator('list_tables')
    for page in paginator.paginate():
        for table_name in page['TableNames']:
            info = {'table_name': table_name, 'stream_arn': None, 'lambda_triggers': []}
            table_desc = dynamodb.describe_table(TableName=table_name)
            stream_spec = table_desc['Table'].get('StreamSpecification', {})
            stream_arn = table_desc['Table'].get('LatestStreamArn')
            if stream_spec.get('StreamEnabled'):
                info['stream_arn'] = stream_arn
                mappings = event_source.list_event_source_mappings(
                    EventSourceArn=stream_arn
                )
                for mapping in mappings['EventSourceMappings']:
                    function_name = mapping.get('FunctionArn')
                    info['lambda_triggers'].append(function_name)

            tables_info.append(info)

    return tables_info




if __name__ == "__main__":
    table_trigger_info = list_dynamodb_tables_and_triggers()
    for table in table_trigger_info:
        print(f"Table: {table['table_name']}")
        print(f"Stream ARN: {table['stream_arn']}")
        if table['lambda_triggers']:
            print("Lambda Triggers:")
            for func in table['lambda_triggers']:
                print(f"  - {func}")
        else:
            print("No Lambda Triggers attached.")
        print("-" * 50)