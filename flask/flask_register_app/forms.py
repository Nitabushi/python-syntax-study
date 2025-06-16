from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('メールアドレス', validators=[DataRequired(), Email()])
    password = PasswordField('パスワード', validators=[DataRequired(), Length(min=6)])
    role = SelectField('ユーザ区分', choices=[('user', '一般ユーザ'), ('admin', '管理者')], validators=[DataRequired()])
    
    submit = SubmitField("登録", render_kw={"id": "submit-btn"})
