from flask import request

from . import extractor_blueprint
from . import extractor
from . import api
from .logger import Logger

@extractor_blueprint.route("/extract", methods=["POST"])
def extract():
    if not request.is_json:
        return 'Invalid payload format. Should be application/json', 400
    
    request_payload = request.get_json()
    api_token = request_payload['token']
    if not api_token:
        Logger.error("Invalid [token] parameter")
        return 'Invalid [token] parameter', 400
    article_url = request_payload['url']
    if not article_url:
        Logger.error("Invalid [article_url] parameter")
        return 'Invalid [article_url] parameter', 400
    page_html = request_payload['pageHtml']
    if not page_html:
        Logger.error("Invalid [page_html] parameter")
        return 'Invalid [page_html] parameter', 400
    
    Logger.info('URL received for extraction:[%s]' % article_url)

    try:
        article_data = extractor.get_data_from_html(page_html)
        Logger.info('Content from %s has been extracted' % article_url)
    except Exception as e:
        api.invalidate_url(api_token, article_url)
        Logger.error('Cannot parse HTML for [%s]' % article_url)
        Logger.error(e)
        return 'Error during HTML parsing', 400

    article_data['url'] = article_url
    article_data['source'] = article_url

    try:
        api.upload_post_data(api_token, article_data)
    except Exception as e:
        Logger.error('Cannot upload data to API (token:[%s])' % api_token)
        Logger.error(e)
        return 'Errors during API upload', 400

    return 'ok', 200