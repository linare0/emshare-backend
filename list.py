import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
def lambda_handler(event, context):
    # TODO implement
    retval = {}
    dynamodb = boto3.resource('dynamodb')
    posts_table = dynamodb.Table('userpost')
    moment_table = dynamodb.Table('moment')
    user_table = dynamodb.Table('user')
    if int(event['queryStringParameters']['session']) == 0:
        posts_ids = posts_table.query(
            Limit = int(event['queryStringParameters']['count']),
            KeyConditionExpression = Key('person').eq(int(event['queryStringParameters']['user']))
        )
    else:
        posts_ids = posts_table.query(
            Limit = int(event['queryStringParameters']['count']),
            KeyConditionExpression = Key('person').eq(int(event['queryStringParameters']['user'])) & 
                Key('datetime').lt(int(event['queryStringParameters']['session'])),
        )
    if posts_ids['Items'] == []:
        body = {
            'status': 'success',
            'session': int(event['queryStringParameters']['session']),
            'moments': []
        }
    else:
        body = {
            'status': 'success',
            'moments': []
        }
        for mid in posts_ids['Items']:
            moment = moment_table.get_item(Key={'id': int(mid['moment'])})
            bm = {
                'moment': {
                    'id': int(moment['Item']['id']),
                    'user': {},
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
            user = user_table.get_item(Key = {'id': int(moment['Item']['userid'])})
            bm['moment']['user'] = {
                'id': int(user['Item']['id']),
                'name': user['Item']['name'],
                'icon': user['Item']['icon'],
            }
            for ec in moment['Item']['comment']:
                bm['moment']['comment'].append(int(ec))
            body['moments'].append(bm)
            body['session'] = int(moment['Item']['datetime'])
    retval['body'] = json.dumps(body)
    retval['headers'] = {'Access-Control-Allow-Origin': '*'}
    return retval;
