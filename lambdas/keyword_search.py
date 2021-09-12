import json
import requests
from requests.auth import HTTPBasicAuth

def search_phrase(video_id, phrase):
    
    occurences_list = []
    elastic_url = 'https://search-video-transcripts-oepaxx32bh7enx5pyrptt7fpjq.us-east-1.es.amazonaws.com/'
    elastic_url += 'transcripts/_search'
    elastic_headers = {"Content-Type": "application/json"}
    
    # search query to match a phrase for a video
    
    search_query = {
        "query": {
            "bool": {
                "must": [
                    { 
                      "match": {
                        "sentence" : {
                          "query" : phrase,
                          "operator" : "or"
                        }
                      }  
                    },
                    {
                        "match_phrase": {
                            "video_id" : video_id
                        }
                    }
                ]
            }
        }
    }
    
    # Make GET call to get sentences that match sentences in transcript
    result = requests.get(elastic_url, headers=elastic_headers, data=json.dumps(search_query),auth=HTTPBasicAuth('esuser','***'))
    search_res = result.json()['hits']['hits']

    print(result)
    print(search_res)
    for elem in search_res:
        phrase_occurence = {}
        t = elem['_source']
        
        phrase_occurence['sentence'] = t.get('sentence')
        phrase_occurence['timestamp'] = t.get('start_time')
        
        occurences_list.append(phrase_occurence)
    
    print(occurences_list)
    return occurences_list

        
def lambda_handler(event, context):
    
    query_params = event['params']['querystring']
    print(event)
    video_id = query_params.get('v')
    query_string = query_params.get('q')
    
    print(video_id)
    print(query_string)
    # logic to get video_id and search phrase from event
    matches = search_phrase(video_id, query_string)
    
    responsebody = {"records": matches}
    
    return {
        'statusCode': 200,
        'headers': { 
            'Content-Type': 'application/json',
        },
        'body': responsebody
    }
