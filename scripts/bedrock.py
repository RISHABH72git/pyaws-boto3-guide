import json
import boto3

bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
model = "anthropic.claude-3-sonnet-20240229-v1:0"
try:
    prompt = "Give all models"
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {
                "role": "user",
                "content": prompt.strip()
            }
        ],
        "max_tokens": 2000
    })

    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=model,
        accept='application/json',
        contentType='application/json'
    )
    response_body = json.loads(response.get('body').read())
    answer = response_body.get('content')[0].get('text')
    print(answer)
except Exception as e:
    print(e)
