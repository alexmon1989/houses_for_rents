*************
Модуль Cities
*************

Модель
======

Основной моделью модуля является :ref:`city-model`.

Контроллер
==========

Исходный код контроллера модуля расположен в файле *app/blueprints/cities/views.py*.


Методы контроллера:

.. automodule:: app.blueprints.cities.views
	:members:


Шаблоны
=======

Шаблоны модуля расположены в каталоге *app/templates/cities*.

Формы
=====

Форма для добавления и редактирования листинга описывается классом **CityForm** в файле *app/blueprints/cities/forms.py*.
Этот класс отвечает также за валидацию введённых пользователем данных.

.. automodule:: app.blueprints.cities.forms
	:members: