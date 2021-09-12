import json
import boto3

def lambda_handler(event, context):
    
    # Extract details from event json
    print(event)
    user_ID = event.get('userID')
    video_ID = event.get('videoID')
    entry = event.get('entry')
    timestamp = event.get('timestamp')

    rdsData = boto3.client('rds-data')

    cluster_arn = 'arn:aws:rds:us-east-1:134022848573:cluster:video-library-rds' 
    secret_arn = 'arn:aws:secretsmanager:us-east-1:134022848573:secret:rds-db-credentials/cluster-QL3YLLQIRO4POVIXNHJKA742FA/admin-G8583j' 
    
    param1 = {'name':'user_id', 'value':{'stringValue': user_ID}}
    param2 = {'name':'video_id', 'value':{'stringValue': video_ID}}
    param3 = {'name':'entry', 'value':{'stringValue': entry}}
    param4 = {'name':'timestamp', 'value':{'stringValue': timestamp}}
    paramSet = [param1, param2, param3, param4]
    
    sql_cmd = 'insert into notes(user_id, video_id, entry, timestamp) '
    sql_cmd += 'VALUES(:user_id, :video_id, :entry, :timestamp);'
    # sql_cmd += 'SELECT LAST_INSERT_ID();'
    response = rdsData.execute_statement(
                resourceArn = cluster_arn, 
                secretArn = secret_arn, 
                database = 'video_db', 
                sql=sql_cmd,
                parameters = paramSet
    )

    print(response)
    
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        note_id = response['generatedFields'][0]['longValue']
        
        return {
            'statusCode': 200,
            'body': {'note_id': note_id}
        }
    else:
        return {
            'statusCode': 400
        }

