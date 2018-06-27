import datetime

from newspaper import Article
from newspaper.outputformatters import OutputFormatter
from newspaper.parsers import Parser
from newspaper.extractors import ContentExtractor
from newspaper.configuration import Configuration
from newspaper.cleaners import DocumentCleaner


def get_data_from_html(html):
    result = {}
    parsed_html = Parser.fromstring(html)

    config = Configuration()
    extractor = ContentExtractor(config)
    formatter = OutputFormatter(config)
    cleaner = DocumentCleaner(config)

    result['title'] = extractor.get_title(parsed_html)
    
    publishing_date = extractor.get_publishing_date('', parsed_html)
    if publishing_date is None:
        publishing_date = datetime.datetime.now()

    result['published_at'] = publishing_date.isoformat()

    cleaned_html = cleaner.clean(parsed_html)
    top_node = extractor.calculate_best_node(cleaned_html)
    top_node = extractor.post_cleanup(top_node)
    result['content'], _ = formatter.get_formatted(top_node)

    return result