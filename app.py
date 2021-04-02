import json
import os

import boto3
import timeline.api as api

BUCKET_NAME = os.environ.get('S3_BUCKET')
TOKEN_KEY = os.environ.get('TOKEN_KEY')
CAL_ID = os.environ.get('CAL_ID')
TIMELINE_LINK = os.environ.get('TIMELINE_LINK')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    token_bytes = s3.get_object(
        Bucket=BUCKET_NAME, Key=TOKEN_KEY)['Body'].read()
    service = api.authorize_using_token(token_bytes)
    response_url = api.insert_timeline_event(service)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Response URL: {response_url}",
        }),
    }
