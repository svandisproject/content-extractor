from flask import Flask, request, json
import requests

import parser
# from logger import logger


application = Flask(__name__)

@application.route('/extract', methods=['POST'])
def index():
    if not request.is_json:
        return 'Invalid payload format. Should be application/json', 400
    
    request_payload = request.get_json()
    api_token = request_payload['token']
    article_url = request_payload['url']
    
    print('URL received for extraction:[%s]' % article_url)

    r = requests.get(article_url)

    if r.status_code != 200: 
        return 'Error fetching content from ' + article_url, 500

    article_data = parser.get_data_from_html(r.text)
    # logger.info('Content from %s has been extracted', article_url)    
    
    article_data['url'] = article_url
    article_data['source'] = article_url
    
    try:
        parser.upload_data_to_api(api_token, article_data)
    except Exception:
        return 'Errors during API upload', 400

    return 'ok', 200

    
if __name__ == '__main__':
    application.run(host='0.0.0.0')