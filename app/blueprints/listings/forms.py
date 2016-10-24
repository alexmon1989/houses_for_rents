from wtforms import Form, StringField, SelectField, IntegerField, FloatField, validators, ValidationError


def validator_phone_numbers_or_email(form, field):
    """Валидатор для проверки заполненности одного из полей agent_phone или agent_email"""
    if len(form.agent_phone.data) == 0 and len(form.agent_email.data) == 0:
        raise ValidationError('Both fields "Agent phone" and "Agent email" cannot be empty. '
                              'Please enter value to one of this fields or to both.')
    else:
        raise validators.StopValidation()


class ListingForm(Form):
    """Класс для генерации и валидации формы добавления/редактирования листинга.

    Атрибуты:
        - city_id: Поле City.
        - street_address: Поле Street name
        - street_number: Поле Street Number
        - suburb: Поле Suburb
        - property_type: Поле Property type
        - bedrooms: Поле Bedrooms
        - government_value: Поле Government value
        - current_rates: Поле Current rates
        - median_rent_qv: Поле Median rent qv
        - capital_growth : Поле Capital growth
        - median_rent_tb: Поле Median rent tb
        - agent_name: Поле Agent name
        - agent_phone: Поле Agent phone
        - agent_email: Поле Agent email
        - appraised_by: Поле Appraised by
    """
    city_id = SelectField('City',
                          [validators.DataRequired()],
                          coerce=int)
    street_address = StringField('Street name', [validators.DataRequired(), validators.Length(max=255)])
    street_number = StringField('Street number', [validators.DataRequired(), validators.Length(max=255)])
    suburb = StringField('Suburb', [validators.DataRequired(), validators.Length(max=255)])
    property_type = SelectField('Property type',
                                [validators.DataRequired()],
                                choices=[(c, c) for c in ('House', 'Apartment', 'Townhouse', 'Unit')])
    bedrooms = SelectField('Bedrooms',
                           [validators.DataRequired()],
                           default=3,
                           coerce=int,
                           choices=[(c, c) for c in range(1, 7)])
    government_value = IntegerField('Government value', [validators.Optional(), validators.NumberRange(min=0)])
    current_rates = IntegerField('Current rates', [validators.Optional(), validators.NumberRange(min=0)])
    median_rent_qv = IntegerField('Median rent qv', [validators.Optional(), validators.NumberRange(min=0)])
    capital_growth = FloatField('Capital growth ', [validators.Optional(), validators.NumberRange(min=0)])
    median_rent_tb = IntegerField('Median rent tb', [validators.Optional(), validators.NumberRange(min=0)])
    agent_name = StringField('Agent name', [
        validators.DataRequired(),
        validators.Optional(),
        validators.Length(max=255)
    ])
    agent_phone = StringField('Agent phone', [
        validator_phone_numbers_or_email,
        validators.Length(max=255)
    ])
    agent_email = StringField('Agent email', [
        validator_phone_numbers_or_email,
        validators.email(),
        validators.Length(max=255)
    ])
    appraised_by = StringField('Appraised by', [validators.Optional(), validators.Length(max=255)])
