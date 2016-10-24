from wtforms import Form, StringField, SelectField, validators, ValidationError


class RequiredWithoutValidator(object):
    """Валидатор, который проверяет следующее условие:
    проверяемое поле должно присутствовать и иметь непустое значение,
    но только если не присутствует или имеет пустое значение указанное полей"""
    def __init__(self, field, message=None):
        self.field = field
        if not message:
            message = u'This field is required.'
        self.message = message

    def __call__(self, form, field):
        if getattr(form, self.field).data:
            raise validators.StopValidation()
        else:
            raise ValidationError(self.message)


def validator_phone_numbers_or_email(form, field):
    """Валидатор для проверки заполненности одного из полей phone_numbers или email"""
    if len(form.phone_numbers.data) == 0 and len(form.email.data) == 0:
        raise ValidationError('Both fields "Phone Numbers" and "Email" cannot be empty. '
                              'Please enter value to one of this fields or to both.')
    else:
        raise validators.StopValidation()


class AgentForm(Form):
    """Класс для генерации и валидации формы добавления/редактирования агентов.

    Атрибуты:
        - name: Поле Name.
        - agency: Поле Agency.
        - phone_numbers: Поле Phone numbers.
        - email: Поле Email.
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
    city_id = SelectField('City',
                          [validators.DataRequired()],
                          coerce=int)



