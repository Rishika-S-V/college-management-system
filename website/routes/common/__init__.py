from flask import Blueprint

common = Blueprint("common", __name__)

from . import utils
from . import view
