import os
import json
import uuid
import datetime
import boto3
from boto3.dynamodb.conditions import Key
from .helper import respond, created_key


def handler(event, context):
    ''' The get handler '''
    table_name = os.getenv('TWEET_TABLE',
                           'tweet_test')  # Table from env vars or tweet_test
    region_name = os.getenv('AWS_REGION',
                            'us-east-1')  # Region from env vars or east 1
    client = boto3.resource('dynamodb', region_name=region_name)

    result = get_all(client, table_name)

    return respond(None, result)


def get_all(client, table_name):
    ''' Returns all tweets items for the given user.
        client is the dynamodb client
        table_name is the name of the dynamodb table where records are stored
    '''
    table = client.Table(table_name)
    # Get today's tweets
    response = table.query(
        KeyConditionExpression=Key('created_key').eq(created_key()))
    if 'Items' in response:
        return response['Items']