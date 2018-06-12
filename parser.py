import sys
import requests
import time
import json

from newspaper import Article
from newspaper.outputformatters import OutputFormatter
from newspaper.parsers import Parser
from newspaper.extractors import ContentExtractor
from newspaper.configuration import Configuration
from newspaper.cleaners import DocumentCleaner

# from logger import logger


API_URL = 'https://svandis-api-prod.herokuapp.com'


def get_data_from_html(html):
    result = {}
    parsed_html = Parser.fromstring(html)

    config = Configuration()
    extractor = ContentExtractor(config)
    formatter = OutputFormatter(config)
    cleaner = DocumentCleaner(config)

    result['title'] = extractor.get_title(parsed_html)
    result['published_at'] = extractor.get_publishing_date('', parsed_html).isoformat()

    cleaned_html = cleaner.clean(parsed_html)
    top_node = extractor.calculate_best_node(cleaned_html)
    top_node = extractor.post_cleanup(top_node)
    result['content'], _ = formatter.get_formatted(top_node)

    return result


def upload_data_to_api(token, payload):
    url = API_URL + '/api/post'
    headers = { 
        'X-WORKER-TOKEN': token,
        'Content-Type': 'application/json'
    }

    print({'post':payload})

    r = requests.post(url, headers=headers, data=json.dumps({'post':payload}))
    if r.status_code != 200 or r.status_code != 201:
        # logger.error('Error uploading content to API [%s]', r.text)
        print(r.text)
        r.raise_for_status()