from __future__ import unicode_literals, print_function
import boto3
import os
from moto import mock_dynamodb2


def init():
    ''' Creates the databases and returns the client and the table 
    '''
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table_name = os.getenv('TWEET_TABLE', 'tweet_test')

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'created_key',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'created',
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[{
            'AttributeName': 'created_key',
            'AttributeType': 'N'
        }, {
            'AttributeName': 'created',
            'AttributeType': 'N'
        }],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        })

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    assert table.table_status == 'ACTIVE'

    return dynamodb, table