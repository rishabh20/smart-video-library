import json
import boto3

def lambda_handler(event, context):
    
    query_params = event['params']['querystring']
    user_ID = query_params.get('userID')
    video_ID = query_params.get('videoID')

    notes_list = []

    rdsData = boto3.client('rds-data')

    cluster_arn = 'arn:aws:rds:us-east-1:134022848573:cluster:video-library-rds' 
    secret_arn = 'arn:aws:secretsmanager:us-east-1:134022848573:secret:rds-db-credentials/cluster-QL3YLLQIRO4POVIXNHJKA742FA/admin-G8583j' 
    
    sql_cmd = 'select note_id, entry, timestamp from notes where'
    sql_cmd += ' user_id = "' + user_ID + '" AND'
    sql_cmd += ' video_id = "' + video_ID + '"'
    
    print(sql_cmd)
    response = rdsData.execute_statement(
                resourceArn = cluster_arn, 
                secretArn = secret_arn, 
                database = 'video_db', 
                sql=sql_cmd
    )
    print(response)    
    for row in response.get('records'):
        note = {}
        note['note_id'] = row[0].get('longValue')
        note['entry'] = row[1].get('stringValue')
        note['timestamp'] = row[2].get('stringValue')
        notes_list.append(note)

    responsebody = {"notes": notes_list}
    
    return {
        'statusCode': 200,
        'headers': { 
            'Content-Type': 'application/json',
        },
        'body': responsebody
    }

