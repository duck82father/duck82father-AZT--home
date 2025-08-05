from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class UserCreateForm(FlaskForm):
    username = StringField('사용자 이름', validators=[DataRequired('사용자 이름을 입력해주세요.'), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired('비밀번호를 입력해주세요.'), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired('비밀번호 확인을 입력해주세요.')])
    email = EmailField('이메일', validators=[DataRequired('이메일을 입력해주세요.'), Email()])
    comment = StringField('코멘트', validators=[Length(max=20)])
    
class QuestionForm(FlaskForm):
    subject = StringField('제목 오류', validators=[DataRequired('제목을 입력해주세요.')])
    content = TextAreaField('내용 오류', validators=[DataRequired('내용을 입력해주세요.')])

class AnswerForm(FlaskForm):
    content = TextAreaField('답변 내용 오류', validators=[DataRequired('답변 내용을 입력해주세요.')])

class UserLoginForm(FlaskForm):
    username = StringField('사용자 이름', validators=[DataRequired('사용자 이름을 입력해주세요.'), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired('비밀번호를 입력해주세요.')])

class RankForm(FlaskForm):
    comment = StringField('코멘트', validators=[DataRequired(), Length(max=30, message='글자수는 최대 30자까지 가능합니다.')])