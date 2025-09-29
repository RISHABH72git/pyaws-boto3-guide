import boto3


def get_lambda_details(function_name, region='us-east-2'):
    client = boto3.client('lambda', region_name=region)

    try:
        response = client.get_function_configuration(
            FunctionName=function_name
        )

        full_response = client.get_function(
            FunctionName=function_name
        )

        print(f"Function Name: {response['FunctionName']}")
        print(f"Runtime: {response['Runtime']}")
        print(f"Handler: {response['Handler']}")
        print(f"Memory Size: {response['MemorySize']} MB")
        print(f"Timeout: {response['Timeout']} sec")
        print(f"Role: {response['Role']}")
        print(f"Environment Variables: {response.get('Environment', {}).get('Variables', {})}")
        print(f"Last Modified: {response['LastModified']}")
        print(f"Version: {response['Version']}")
        print(f"Tracing Config: {response.get('TracingConfig', {})}")
        print(f"Package Type: {response.get('PackageType')}")
        print(f"Code Size: {full_response['Configuration']['CodeSize']} bytes")
        print(f"Code Location: {full_response['Code']['Location']}")

    except client.exceptions.ResourceNotFoundException:
        print(f"Lambda function '{function_name}' not found.")
    except Exception as e:
        print(f"Error fetching details: {str(e)}")


get_lambda_details("test", "")
