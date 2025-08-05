from homepage import db

question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)

class azquiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz = db.Column(db.String(150), nullable=False)
    answer = db.Column(db.String(50), nullable=False)
    hint = db.Column(db.String(50), nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('Users', backref=db.backref('question_set'))
    voter = db.relationship('Users', secondary=question_voter, backref=db.backref('question_voter_set'))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('Users', backref=db.backref('answer_set'))
    voter = db.relationship('Users', secondary=answer_voter, backref=db.backref('answer_voter_set'))

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    comment = db.Column(db.String(20), nullable=True)

    @classmethod
    def get_users_data(cls):
        users = cls.query.join(Solved, cls.id == Solved.user_id).group_by(cls.id).order_by(
            db.func.count(Solved.quiz_id).desc()
        ).all()
        for user in users:
            user.comment = user.comment or '오늘도 행복한 하루 되세요'
            user.quiz_id_count = Solved.query.filter_by(user_id=user.id).count()
        return users

class Solved(db.Model):
    __tablename__ = 'solved'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    user = db.relationship('Users', backref=db.backref('solved_set', lazy=True))
    quiz_id = db.Column(db.Integer, db.ForeignKey('azquiz.id', ondelete='CASCADE'), primary_key=True)
    quiz = db.relationship('azquiz', backref=db.backref('solved_set', lazy=True))