from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,Form
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class StockForm(FlaskForm):
    name = StringField('Look up a stock', validators=[DataRequired()])
    submit = SubmitField('Submit')
    search = StringField('')