import json
import boto3
import time
import requests
from requests.auth import HTTPBasicAuth
from wordcloud import WordCloud, STOPWORDS
import io
import matplotlib.pyplot as plt

transcribe_client = boto3.client('transcribe')
s3_client = boto3.client('s3')
sqs = boto3.client('sqs')
q_url = 'https://sqs.us-east-1.amazonaws.com/134022848573/transcription-jobs-queue'
elastic_video_list = 'https://search-video-transcripts-oepaxx32bh7enx5pyrptt7fpjq.us-east-1.es.amazonaws.com/video_list/_doc'
elastic_transcripts = 'https://search-video-transcripts-oepaxx32bh7enx5pyrptt7fpjq.us-east-1.es.amazonaws.com/transcripts/_doc'
elastic_headers = {"Content-Type": "application/json"}

def get_title(s3bucket,s3_object_key):
    response = s3_client.head_object(
        Bucket = s3bucket,
        Key = s3_object_key
    )
    return response['Metadata'].get('customlabels','')
    
def insert_to_elastic(transcribe_op, extract):
    es_video_obect = {}
    es_transcript_obj = {}
    es_video_obect['video_url'] = "https://"+extract['bucket']+".s3.amazonaws.com/"+extract['objectKey']
    es_video_obect['wordcloud_url'] = "https://project-cu-wordcloud.s3.amazonaws.com/"+extract['transcribe_job']['OutputKey']+".png"
    es_video_obect['timestamp'] = extract['createdTimestamp']
    es_video_obect['video_id'] = extract['eTag']
    es_video_obect['video_title'] = get_title(extract['bucket'],extract['objectKey'])
    
    start_time = 0.01
    sentence = ""
    for word_json in transcribe_op['items']:
        #print(word_json)
        word = word_json['alternatives'][0]['content']
        #print(word)
        type = word_json['type']
        
        if sentence == "":
            #print("setting start_time")
            start_time = word_json['start_time']
            
        if type=='punctuation' and ( word== '.' or word == '?'):
            #print("breaking the sentence")
            sentence = sentence + word
            #print("sentence so far:"+sentence)
            es_transcript_obj['sentence'] = sentence
            es_transcript_obj['start_time'] = start_time
            es_transcript_obj['video_id'] = extract['eTag']
            es_transc_response = requests.post(elastic_transcripts,
                                data=json.dumps(es_transcript_obj).encode("utf-8"),
                                auth=HTTPBasicAuth('esuser','***'),
                                headers=elastic_headers)
                                
            sentence = ""
            
        else:
            sentence = sentence + " "+ word
            #print("sentence so far:"+sentence)
            
    
    es_video_response = requests.post(elastic_video_list+'/'+extract['eTag'],
                                data=json.dumps(es_video_obect).encode("utf-8"),
                                auth=HTTPBasicAuth('esuser','***'),
                                headers=elastic_headers)
     
    print("Inserted to elastic")                           
    print(es_video_response)
    print(es_transc_response)
    

def get_transcript(bucket,key):
    s3_object = s3_client.get_object(Bucket=bucket, Key=key)
    output = json.loads(s3_object['Body'].read().decode('utf-8'))
    transcribe_op = output['results']
    return transcribe_op

def create_word_cloud(transcribe_op,sqs_object):
    stopwords_wc = set(STOPWORDS)
    stopwords_wc.update(['actually','sure','really','still','make','let','lot','want','important','going','okay','everyone','parts','old','people','ready','Hey','well','talk','done','want','back','modern','good','right','talking','awesome','work','example'])
    transcript = transcribe_op['transcripts'][0]['transcript']
    wordcloud = WordCloud(width = 800, height = 800,background_color ='black',stopwords = stopwords_wc,min_font_size = 10).generate(transcript)
    plt.figure(figsize = (10, 10))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('project-cu-wordcloud')
    bucket.put_object(Body=img_data, ContentType='image/png', Key=sqs_object['transcribe_job']['OutputKey']+".png")
    
    
def check_complete(extract):
    try:
        status = transcribe_client.get_transcription_job(TranscriptionJobName=extract['transcribe_job']['job_name'])
    except Exception as e:
        return True
    
    print(status)    
    
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED']:
        return True
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['FAILED']:
        print("TranscriptionJob Failed")
        return False

    print("Not ready yet")
    return False 

def pull_from_sqs():
    response = sqs.receive_message(
        QueueUrl=q_url,
        VisibilityTimeout=60
    )
    
    if 'Messages' in response and len(response['Messages']) > 0:
        for message in response['Messages']:
            sqs_object = json.loads(message['Body'])
            print(sqs_object)
            if check_complete(sqs_object):
                sqs.delete_message(
                    QueueUrl=q_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
                print('Received and deleted message: %s' % message)
                transcribe_op = get_transcript(sqs_object['transcribe_job']['OutputBucketName'],sqs_object['transcribe_job']['OutputKey'])
                create_word_cloud(transcribe_op,sqs_object)
                print("saving to S3")
                insert_to_elastic(transcribe_op, sqs_object)
                
                
            
    

def lambda_handler(event, context):
    pull_from_sqs()
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

