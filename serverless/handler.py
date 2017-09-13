import json
import datetime


def endpoint(event, context):
    current_time = datetime.datetime.now().time()
    body = {
        "message": "Hello, Boston Serverless Meetup. " + str(current_time)
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response