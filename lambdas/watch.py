import json
import requests
from requests.auth import HTTPBasicAuth

def get_video_info(video_ID):
    
    elastic_url = 'https://search-video-transcripts-oepaxx32bh7enx5pyrptt7fpjq.us-east-1.es.amazonaws.com/'
    elastic_url += 'video_list/_search'
    elastic_headers = {"Content-Type": "application/json"}
    
    # search query to get all videos in the library
    search_query = {
        "query": {
             "match_phrase": {
               "video_id": video_ID
             }
        }
    }
    
    result = requests.get(elastic_url, headers=elastic_headers, data=json.dumps(search_query),auth=HTTPBasicAuth('esuser','***'))
    print(result)
    records = result.json()['hits']['hits']
    
    video_elem = {}
    
    for elem in records:
        video_dict = elem['_source']
        video_elem['video_url'] = video_dict.get('video_url')
        video_elem['video_title'] = video_dict.get('video_title')
        video_elem['wordcloud_url'] = video_dict.get('wordcloud_url')
        
    
    return video_elem
        
def lambda_handler(event, context):
    print(event)
    query_params = event['params']['querystring']
    video_ID = query_params.get('v')
    
    return get_video_info(video_ID)
