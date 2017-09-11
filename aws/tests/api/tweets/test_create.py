from __future__ import unicode_literals, print_function
import unittest
import boto3
import sys
import os
import uuid
import json
from os.path import dirname, join
from moto import mock_dynamodb2

from api.tweet.get import create, handler
from .dbconfig import init


class TestCreateAPI(unittest.TestCase):
    @mock_dynamodb2
    def test_create_function(self):
        client, table = init()
        item = {
            'content': 'I need to finish this test!',
            'header': 'Always busy!',
            'fake': 8675309
        }

        results = create(client, item, table.table_name, ['content', 'header'])

        # Verify the results are not null
        assert results
        # Verify that the created property was set
        assert results['created']
        assert results['created_key']

        # Verify the items that a user can set were set correctly.
        assert results['content'] == item['content']
        assert results['header'] == item['header']

        # Verify that the fake attribute is removed by the whitelist
        assert 'fake' not in results

    @mock_dynamodb2
    def test_create_function_error(self):
        client, table = init()
        # Verify todo items with no item raise an error
        with self.assertRaises(ValueError):
            create(client, {}, table.table_name, ['content', 'header'])

    @mock_dynamodb2
    def test_create_handler(self):
        client, table = init()

        event = {
            'body':
            json.dumps({
                'content': 'I need to finish this test!',
                'header': 'c',
                'fake': 8675309
            }),
            # Not using, but adding for the sake of the demo
            'requestContext': {
                'identity': {
                    'cognitoIdentityId': '1'
                }
            }
        }

        # not using the context, so no need to mock it.
        results = handler(event, {})

        # Verify the results are not null
        assert results
        # Verify the status code is '200'
        assert 'statusCode' in results and results['statusCode'] == '200'
        # Verify the contents of the body
        assert 'body' in results
        body = json.loads(results['body'])

        assert body['created']
        # Verify the items that a user can set were set correctly.
        assert body['content'] == json.loads(event['body'])['content']
        assert body['header'] == json.loads(event['body'])['header']
        # Verify that the fake attribute is removed by the whitelist
        assert 'fake' not in body


if __name__ == '__main__':
    unittest.main()