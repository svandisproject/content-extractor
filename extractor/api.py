import requests

API_URL = 'https://svandis-api-prod.herokuapp.com'

def upload_post_data(api_token, post_data):
    url = API_URL + '/api/post'
    headers = SvandisApi._get_request_headers()

    r = requests.post(url, headers=headers, data=json.dumps({'post': post_data}))
    r.raise_for_status()
    return r.status_code


def invalidate_url(api_token, url):
    url = API_URL + '/api/post/invalidate-url'
    headers = SvandisApi._get_request_headers()

    r = requests.post(url, headers=headers, data=json.dumps({'url': url}))
    r.raise_for_status()
    return r.status_code


def _get_request_headers(token):
    return {
        'X-WORKER-TOKEN': token,
        'Content-Type': 'application/json'
    }