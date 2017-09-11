from __future__ import unicode_literals, print_function
import unittest
import boto3
import sys
import os
import uuid
import json
from os.path import dirname, join
from moto import mock_dynamodb2

from todo.api.create import create
from todo.api.get import get_all, get_one, handler
from dbconfig import init


class TestGetAPI(unittest.TestCase):

    @mock_dynamodb2
    def test_get_all_function(self):
        client, table = init()
        items = [{
            'content': 'A',
            'header': 'A'
        }, {
            'content': 'B',
            'header': 'B'
        }, {
            'content': 'C',
            'header': 'C'
        }]

        create(client, items[0], table.table_name, ['content', 'header'])
        create(client, items[1], table.table_name, ['content', 'header'])
        create(client, items[2], table.table_name, ['content', 'header'])

        todo_items = get_all(client, table.table_name)

        assert len(todo_items) == 3
        # Verify items with content A, B, and C are returned.
        assert all([i['content'] in ['A', 'B', 'C'] for i in todo_items])


    @mock_dynamodb2
    def test_get_handler_all(self):
        client, table = init()

        items = [{
            'content': 'A',
            'header': 'A'
        }, {
            'content': 'B',
            'header': 'B'
        }, {
            'content': 'C',
            'header': 'C'
        }]

        create(client, items[0], table.table_name, ['content', 'header'])
        create(client, items[1], table.table_name, ['content', 'header'])
        create(client, items[2], table.table_name, ['content', 'header'])

        todo_items = get_all(client, table.table_name)

        event = {'requestContext': {'identity': {'cognitoIdentityId': '1'}}}
        
        # not using the context, so no need to mock it.
        results = handler(event, {})  
        # Verify the results are not null
        assert results
        # Verify the status code is '200'
        assert 'statusCode' in results and results['statusCode'] == '200'
        # Verify the contents of the body
        assert 'body' in results
        body = json.loads(results['body'])
        assert len(body) == 2
        # Verify that the correct records are returned
        assert all([i['content'] in ['A', 'B', 'C'] for i in todo_items])


if __name__ == '__main__':
    unittest.main()