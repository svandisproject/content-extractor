from flask import Blueprint

extractor_blueprint = Blueprint("extractor", __name__)

from . import routes