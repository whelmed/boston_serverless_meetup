import os
import json
import uuid
import datetime
import boto3
from .helper import respond, created_key


def handler(event, context):
    data = None

    try:
        data = json.loads(event['body'])
    except Exception as ex:
        return respond(ex.args[0], None)  # Bail out and return an error

    # Make sure users don't add more properties than they should
    # A whitelist will ensure that any property non in this list is removed
    whitelist = ['content', 'header']
    table_name = os.getenv('TWEET_TABLE',
                           'tweet_test')  # Table from env vars or tweet_test
    region_name = os.getenv('AWS_REGION',
                            'us-east-1')  # Region from env vars or east 1
    client = boto3.resource('dynamodb', region_name=region_name)

    result = create(client, user_id, data, table_name, whitelist)

    return respond(None, result)


def create(client, data, table_name, whitelist):
    ''' client is the dynamodb client
        data is a dict for properties to store in dynamodb.
        table_name is the name of the dynamodb table where records are stored
        whitelist is a list of properties that users are allowed to edit for their own records.
    '''
    if 'content' not in data or 'header' not in data:
        raise ValueError(
            'The tweet requires both a content and header property')

    table = client.Table(table_name)
    # Create a new dict that contains just whitelisted properties.
    whitelisted_data = {k: v for k, v in data.items() if k in whitelist}

    whitelisted_data['created'] = str(uuid.uuid4())
    whitelisted_data['created_key'] = created_key()

    table.put_item(Item=whitelisted_data)

    return whitelisted_data