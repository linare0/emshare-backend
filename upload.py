import boto3
import json

def lambda_handler(event, context):
    retval = {}
    dynamodb = boto3.resource('dynamodb')
    user_table = dynamodb.Table('user')
    user = user_table.get_item(Key={'id': int(event['queryStringParameters']['user'])})
    if user['Item'] == {}:
        body = {
            'status': 'fail: invalid user id'
        }
    else
        s3 = boto3.client('s3')
        updata = s3.generate_presigned_post(
            Bucket = 'emshare',
            Key = 'uploaded-${filename}',
            Conditions = [{"acl": "public-read"}]
        )
        body = {
            'status': 'success',
            'url': updata['url'],
            'fields': updata['fields']
        }
    retval['body'] = json.dumps(body)
    retval['headers'] = {'Access-Control-Allow-Origin': '*'}
    return retval
