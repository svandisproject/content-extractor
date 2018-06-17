from flask import Flask, request

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
    page_html = request_payload['pageHtml']
    
    print('URL received for extraction:[%s]' % article_url)

    article_data = parser.get_data_from_html(page_html)
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