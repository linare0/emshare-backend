import boto3;
import pprint;
import json;
def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    moment_table = dynamodb.Table('moment')
    user_table = dynamodb.Table('user')
    moment = moment_table.get_item(Key={'id': int(event['queryStringParameters']['id'])})
    retval = {}
    if moment['Item'] == {}:
        body = {
               'status': 'fail: no such moment'
        }    
    else:
        body = {
            'status': 'success',
            'moment': {
                'id': int(moment['Item']['id']),
                'user': {
                    
                },
                'video': moment['Item']['video'],
                'music': {
                    'identifier': moment['Item']['music'],
                    'start': int(moment['Item']['music-start']),
                    'duration': int(moment['Item']['music-duration']),
                },
                'comment': [],
                'datetime': int(moment['Item']['datetime'])
            }
        }
        for comment in moment['Item']['comment']:
            body['moment']['comment'].append(int(comment))
        user = user_table.get_item(Key = {'id': int(moment['Item']['userid'])})
        body['moment']['user'] = {
            'id': int(user['Item']['id']),
            'name': user['Item']['name'],
            'icon': user['Item']['icon'],
        }
    retval['body'] = json.dumps(body)
    retval['headers'] = {'Access-Control-Allow-Origin': '*'}
    return retval
