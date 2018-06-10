import sys
import requests
import time

from newspaper import Article
from newspaper.outputformatters import OutputFormatter
from newspaper.parsers import Parser
from newspaper.extractors import ContentExtractor
from newspaper.configuration import Configuration
from newspaper.cleaners import DocumentCleaner


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


def upload_data_to_api(token, data):
    url = API_URL + "/api/post"
    headers = { "X-WORKER-TOKEN": token }
    print(data)
    r = requests.post(url, headers=headers, data={'post': data})
    print(r.text)
    r.raise_for_status()


def extract(api_token, article_url):
    r = requests.get(article_url)

    article_data = get_data_from_html(r.text)
    article_data["url"] = article_url
    article_data["source"] = article_url
    upload_data_to_api(api_token, article_data)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise("Arguments number don't match")
    
    _, api_token, article_url = sys.argv

    extract(api_token, article_url)
