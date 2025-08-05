from flask import Blueprint, render_template, url_for, request, g, session
from werkzeug.utils import redirect
from flask_wtf.csrf import CSRFProtect

from homepage import db
from homepage.forms import RankForm
from homepage.models import Users, Solved
from homepage.views.auth_views import login_required

bp = Blueprint('rank', __name__, url_prefix='/rank')
csrf = CSRFProtect()

@bp.route('/status/', methods=('GET', 'POST'))
@login_required
def rank():
    solved = Solved.query.filter_by(user_id=g.user.id).all()
    solved_quiz_ids = []
    for solve in solved:
        solved_quiz_ids.append(solve.quiz_id)
    all_user_data = Users.get_users_data()
    form = RankForm()

    if request.method == 'POST' and form.validate_on_submit():
        user = Users.query.filter_by(id=g.user.id).first()
        user.comment = form.comment.data
        db.session.commit()
        return redirect(url_for('rank.rank'))
    return render_template('rank/rank.html', solved_quiz_ids=solved_quiz_ids, all_user_data=all_user_data, form=form)