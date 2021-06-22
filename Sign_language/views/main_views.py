from flask import Blueprint, render_template, request
from werkzeug import secure_filename

bp = Blueprint('main', __name__, url_prefix='/')


