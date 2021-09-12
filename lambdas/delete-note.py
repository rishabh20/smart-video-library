import json
import boto3
rdsData = boto3.client('rds-data')

def lambda_handler(event, context):
     # Extract details from event json
    print(event)
    note_ID=event["queryStringParameters"]['noteID']
    #query_params = event['params']['querystring']
    #note_ID = query_params.get('noteID')
    
    cluster_arn = 'arn:aws:rds:us-east-1:134022848573:cluster:video-library-rds' 
    secret_arn = 'arn:aws:secretsmanager:us-east-1:134022848573:secret:rds-db-credentials/cluster-QL3YLLQIRO4POVIXNHJKA742FA/admin-G8583j' 
    

    
    sql_cmd = 'delete from notes where'
    sql_cmd += ' note_id = "' + note_ID + '"'
    
    response = rdsData.execute_statement(
                resourceArn = cluster_arn, 
                secretArn = secret_arn, 
                database = 'video_db', 
                sql=sql_cmd
    )
    return {
        'statusCode': 200,
        'headers': { 
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' 
        },
        'body': json.dumps('Hello from Lambda!')
    }

