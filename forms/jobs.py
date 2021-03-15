from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = TextAreaField("Работа", validators=[DataRequired()])
    team_leader = StringField('Ответственный', validators=[DataRequired()])
    work_size = DecimalField('Время работы в ч', validators=[DataRequired()])
    collaborators = StringField("Участники", validators=[DataRequired()])
    start_date = StringField('Время начала', validators=[DataRequired()])
    end_date = StringField('Время конца')
    is_finished = BooleanField("Работа закончена")
    submit = SubmitField('Добавить')
