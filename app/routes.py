from flask import request
from app import flask_app, extractor, utils
from app.logger import Logger
from tasks import extract_content

@flask_app.route("/extract", methods=["POST"])
def extract():
    if not request.is_json:
        return 'Invalid payload format. Should be application/json', 400
    
    request_payload = request.get_json()
    client_token = request_payload['token']
    if not client_token:
        Logger.error("Invalid [token] parameter")
        return 'Invalid [token] parameter', 400
    article_url = request_payload['url']
    if not article_url:
        Logger.error("Invalid [article_url] parameter")
        return 'Invalid [article_url] parameter', 400
    article_html = request_payload['pageHtml']
    if not article_html:
        Logger.error("Invalid [article_html] parameter")
        return 'Invalid [article_html] parameter', 400

    Logger.info('URL received for extraction:[%s]' % article_url)

    extract_content.delay(article_url, article_html, client_token)

    return 'Article content was sent to processing', 200