from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from homepage import db
from homepage.forms import QuestionForm, AnswerForm
from homepage.models import Question, Answer, Users
from homepage.views.auth_views import login_required
from homepage.views.status_views import solvedCount
from datetime import datetime

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list')
def _list():
    solved_quiz_ids = solvedCount()
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    question_list = Question.query.order_by(Question.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, Users.username) \
            .join(Users, Answer.user_id == Users.id).subquery()
        question_list = question_list \
            .join(Users) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |
                    Question.content.ilike(search) |
                    Users.username.ilike(search) |
                    sub_query.c.content.ilike(search) |
                    sub_query.c.username.ilike(search)
                    ) \
            .distinct()
    question_list = question_list.paginate(page=page, per_page=10)
    question_notice = Question.query.get_or_404(0)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw, solved_quiz_ids=solved_quiz_ids, question_notice=question_notice)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    solved_quiz_ids = solvedCount()
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form, solved_quiz_ids=solved_quiz_ids)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    solved_quiz_ids = solvedCount()
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('question._list'))
    return render_template('question/question_form.html', form=form, solved_quiz_ids=solved_quiz_ids)

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question.id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)
        return render_template('question/question_form.html', form=form)
    
@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))

@bp.route('/vote/<int:question_id>')
@login_required
def vote(question_id):
    _question = Question.query.get_or_404(question_id)
    if g.user == _question.user:
        flash('본인이 작성한 글은 추천할 수 없습니다')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))