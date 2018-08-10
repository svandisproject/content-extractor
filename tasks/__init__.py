from app import celery
from app.extractor import get_data_from_html
from app.logger import Logger
from app.utils import invalidate_url, upload_article_data


@celery.task()
def extract_content(article_url, article_html, client_token):
    try: 
        article_data = get_data_from_html(article_url, article_html)
        article_data['url'] = article_url
        article_data['source'] = article_url
    except Exception as e:
        Logger.error('Error during content extraction for [%s : %s]' % (article_url, client_token))
        Logger.error(e)
        invalidate_url(client_token, article_url)
        return {'status': 'extraction_error', 'url': article_url, 'token': client_token}
    
    try:
        upload_article_data(client_token, article_data)
    except Exception as e:
        Logger.error('Error during content api upload [%s : %s]' % (article_url, client_token))
        return {'status': 'api_upload_error', 'url': article_url, 'token': client_token}
    
    return {'status': 'ok', 'url': article_url, 'token': client_token}