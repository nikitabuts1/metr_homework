from flask_wtf import FlaskForm
from wtforms.validators import NumberRange, ValidationError, InputRequired
from wtforms import FileField, IntegerField, FloatField

def filename_check(sub: str='.txt'):
    message: str = f'Файл должен иметь расширение {sub}'
    def _filename_check(field):
        if str(field.data.filename).find(sub) == -1:
            raise ValidationError(message)
        return _filename_check

class Form(FlaskForm):
    file = FileField(validators=filename_check(".txt"))
    num_parts = IntegerField(
        validators=[
            NumberRange(min=2, message='Значение должно быть больше 1')
        ]
    )
    conf_level = FloatField(
        validators=[
            NumberRange(min=0.0000001, message='Значение должно быть больше 0.0000001')
        ]
    )