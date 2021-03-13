from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    team_leader = StringField('Руководитель', validators=[DataRequired()])
    job = TextAreaField("Описание работы")
    collaborators = StringField("Участники")
    is_finished = BooleanField("Закончена")
    submit = SubmitField('Применить')
