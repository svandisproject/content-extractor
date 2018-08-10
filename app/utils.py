import requests
import json


API_URL = 'https://svandis-api-prod.herokuapp.com'

def upload_article_data(client_token, article_data):
    url = API_URL + '/api/post'
    headers = _get_request_headers(client_token)

    r = requests.post(url, headers=headers, data=json.dumps({'post': article_data}))
    r.raise_for_status()
    return r.status_code


def invalidate_url(client_token, article_url):
    url = API_URL + '/api/post/invalidate-url'
    headers = _get_request_headers(client_token)

    r = requests.post(url, headers=headers, data=json.dumps({'url': article_url}))
    r.raise_for_status()
    return r.status_code


def _get_request_headers(token):
    return {
        'X-WORKER-TOKEN': token,
        'Content-Type': 'application/json'
    }