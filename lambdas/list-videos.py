import json
import requests
from requests.auth import HTTPBasicAuth

def get_videos():
    
    v_list = []
    elastic_url = 'https://search-video-transcripts-oepaxx32bh7enx5pyrptt7fpjq.us-east-1.es.amazonaws.com/'
    elastic_url += 'video_list/_search'
    elastic_headers = {"Content-Type": "application/json"}
    
    # search query to get all videos in the library
    search_query = {
        "query": {
            "match_all": {}
        }
    }
    
    # Make GET call to get videos in the library
    result = requests.get(elastic_url, headers=elastic_headers, data=json.dumps(search_query),auth=HTTPBasicAuth('esuser','***'))
    videos_list = result.json()['hits']['hits']

    for elem in videos_list:
        video_elem = {}
        video_dict = elem['_source']
        
        video_elem['video_url'] = video_dict.get('video_url')
        video_elem['video_id'] = video_dict.get('video_id')
        video_elem['video_title'] = video_dict.get('video_title')
        
        id = ['restaurant_ID']
        print(f"Restaurant ID: {id}")
        v_list.append(video_elem)
    
    return v_list
        
def lambda_handler(event, context):
    
    return get_videos()
