import os
import werkzeug
import requests

from flask import Flask, jsonify, request
from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema

import extractor
from logger import Logger


application = Flask(__name__)

extract_schema = {
    'type': 'object',
    'required': ['url'],
    'properties': {
        'url': { 'type': 'string', 'minLength': 10 }
    }
}

class JsonInputs(Inputs):
    json = [JsonSchema(schema=extract_schema)]


@application.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return jsonify(success=False, reason=e.get_description(), errors=[]), 400


@application.route('/extract', methods=['POST'])
def index():
    inputs = JsonInputs(request)

    if not inputs.validate():
        return jsonify(success=False, reason='Incorrect json payload', errors=inputs.errors), 400

    payload = request.get_json()
    url = payload['url']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }
    
    Logger.info(f'URL received for extraction:[{url}]')

    response = requests.get(url, headers=headers)

    if response.status_code is not 200:
        Logger.error(f'Cannot request page {url}')
        return jsonify(success=False, reason='Error during page request [{}]'.format(url)), 400

    try:
        html = response.text
        article_data = extractor.get_data_from_html(html)
        Logger.info(f'Content of {url} has been extracted')
    except Exception as e:
        Logger.error(f'Cannot parse HTML for [{url}]')
        Logger.error(e)
        return jsonify(success=False, reason='Error during content extraction of [{}]'.format(url), error=str(e)), 400

    return jsonify({ 'url': url, 'article': article_data })

    
if __name__ == '__main__':
    application.run(host='0.0.0.0', port=os.getenv('PORT') or 80)