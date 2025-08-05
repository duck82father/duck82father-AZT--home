from flask import Blueprint, url_for, current_app
from werkzeug.utils import redirect

from homepage import db
# from homepage.forms import UserCreateForm, UserLoginForm
# from homepage.models import Users

bp = Blueprint('main', __name__, url_prefix='/')
# Blueprint(별칭, 인수("main_views"), '@bp.route()' 앞에 붙는 접두어 url)

@bp.route('/')
def index():
    return redirect(url_for('status.show'))