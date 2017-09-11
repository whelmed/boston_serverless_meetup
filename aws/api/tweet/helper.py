import json


def respond(err, res=None):
    # In a real app error messages shouldn't be sent to the end user.
    # This is a security concern. However, in a demo, for debugging, it's okay.
    body = {}
    if err:
        body = json.dumps({'error': err})
    else:
        body = json.dumps(res)
    return {
        'statusCode': '400' if err else '200',
        'body': body,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }

def created_key(today_minus=0, starting_date=None):
    ''' created_key returns a date string representing the 
        YYYY MM DD that a record was created on. This allows for lookups by day.
        This is not an exceptionally scalable method. However, it works for this demo.
    '''
    d = (starting_date or datetime.date.today()) - datetime.timedelta(days=today_minus)
    return int(d.strftime('%Y%m%d'))
