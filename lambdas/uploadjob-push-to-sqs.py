import json
import boto3
import json
import time

sqs = boto3.client('sqs')
s3_client = boto3.client('s3')
transcribe_client = boto3.client('transcribe')
q_url = 'https://sqs.us-east-1.amazonaws.com/134022848573/transcription-jobs-queue'

def insert_to_sqs(body):
    
    response = sqs.send_message(
        QueueUrl = q_url,
        MessageBody = json.dumps(body)
    )
    print("SQS:")
    print(response)
    return response

def transcribe(extract):

    transcribe_job = {}
    job_uri = "https://"+extract['bucket']+".s3.amazonaws.com/"+extract['objectKey']
    job_name = "transcribe_"+extract['createdTimestamp'].replace(':','_')
    outputKey = 'transcript_'+extract['createdTimestamp'].replace(':','_')
    result = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        LanguageCode='en-US',
        OutputBucketName='project-cu-transcripts',
        OutputKey = outputKey
    )
    
    print(result)
    
    transcribe_job['OutputBucketName'] = 'project-cu-transcripts'
    transcribe_job['OutputKey'] = outputKey#'trascript_Apache_Kafka_in_5_minutes' #
    transcribe_job['job_name'] = job_name#'trascript_Apache_Kafka_in_5_minutes' #
    
    return transcribe_job
    


def lambda_handler(event, context):
    
    print(event)
    for ele in event['Records']:
        extract = {}
        extract['bucket'] = ele['s3']['bucket']['name']
        extract['objectKey'] = ele['s3']['object']['key']
        extract['size'] = ele['s3']['object']['size']
        extract['eTag'] = ele['s3']['object']['eTag']
        #extract['title'] = get_title(extract['bucket'],extract['objectKey'])#ele['responseElements']['x-amz-meta-customlabels']
        extract['createdTimestamp'] = ele['eventTime']
        
        transcribe_job = transcribe(extract)
        extract['transcribe_job'] = transcribe_job
        insert_to_sqs( extract)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

