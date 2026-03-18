import boto3
from .config import AWS_REGION, BEDROCK_CHAT_MODEL_ID

client = boto3.client("bedrock-runtime", region_name=AWS_REGION)

def answer_with_evidence(question, context):
    response = client.invoke_model(
        modelId=BEDROCK_CHAT_MODEL_ID,
        body=str({"input": f"Question: {question}\nContext: {context}"})
    )
    return response["body"].read().decode()
