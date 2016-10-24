******
Модели
******

Все классы, представленные ниже, являются моделями **SQLAlchemy**.
Подробнее про работу с этой библиотекой (а именно её "обёрткой" для фреймворка Flask) можно почитать `тут <http://flask-sqlalchemy.pocoo.org/2.1/>`_.


Исходный код классов расположен в файле `app/models.py`.

.. _listing-model:

Модель Listing
==============

Отвечает за взаимодействие с таблицей `listings`.

.. automodule:: app.models
 
.. autoclass:: Listing
    :members:
    :private-members:
    :special-members:

.. _city-model:

Модель City
===========

.. autoclass:: City
    :members:
    :private-members:
    :special-members:


.. _manager-model:

Модель Manager
==============

.. autoclass:: Manager
    :members:
    :private-members:
    :special-members:

.. _agent-model:

Модель Agent
============

.. autoclass:: Agent
    :members:
    :private-members:
    :special-members:
