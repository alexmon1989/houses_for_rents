from wtforms import Form, StringField, validators, ValidationError
from app.models import City


class UniqueValidator(object):
    """Валидатор для проверки значения поля на уникальность."""
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = u'this element already exists'
        self.message = message

    def __call__(self, form, field):
        existing = self.model.query.filter(getattr(self.model, self.field) == field.data).first()
        if existing:
            raise ValidationError(self.message)


class CityForm(Form):
    """Класс для генерации и валидации формы добавления/редактирования горола.

        Атрибуты:
            - title: Поле Title.
        """
    title = StringField('Title', [
        validators.DataRequired(),
        validators.Length(max=255),
        UniqueValidator(
            City,
            'title',
            'Title with the same value exists.'
        )
    ])
