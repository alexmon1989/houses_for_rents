from wtforms import Form, StringField, SelectField, FloatField, validators, ValidationError


def validator_phone_numbers_or_email(form, field):
    """Валидатор для проверки заполненности одного из полей phone_numbers или email"""
    if len(form.phone_numbers.data) == 0 and len(form.email.data) == 0:
        raise ValidationError('Both fields "Phone Numbers" and "Email" cannot be empty. '
                              'Please enter value to one of this fields or to both.')
    else:
        raise validators.StopValidation()


class ManagerForm(Form):
    """Класс для генерации и валидации формы добавления/редактирования менеджеров.

    Атрибуты:
        - name: Поле Name.
        - agency: Поле Agency.
        - phone_numbers: Поле Phone numbers.
        - email: Поле Email.
        - rate: Поле Rate.
        - city_id: Поле City.
    """
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=3, max=255)])
    agency = StringField('Agency', [validators.Optional(), validators.Length(min=3, max=255)])
    phone_numbers = StringField('Phone numbers', [
        validator_phone_numbers_or_email,
        validators.Length(min=3, max=255)
    ])
    email = StringField('Email', [
        validator_phone_numbers_or_email,
        validators.Email()
    ])
    rate = FloatField('Rate', [validators.Optional(), validators.NumberRange(min=0)], default=0)
    city_id = SelectField('City',
                          [validators.DataRequired()],
                          coerce=int)
