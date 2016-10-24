***************
Модуль Listings
***************

Модель
======

Основной моделью модуля является :ref:`listing-model`.

Контроллер
==========

Исходный код контроллера модуля расположен в файле *app/blueprints/listings/views.py*.


Методы контроллера:

.. automodule:: app.blueprints.listings.views
	:members:


Шаблоны
=======

Шаблоны модуля расположены в каталоге *app/templates/listings*.

Формы
=====

Форма для добавления и редактирования листинга описывается классом **ListingForm** в файле *app/blueprints/listings/forms.py*.
Этот класс отвечает также за валидацию введённых пользователем данных.

.. automodule:: app.blueprints.listings.forms
	:members:

Javascript
==========

Исходный код для Javascript, который выполняется на веб-страницах модуля, находится в файле *static/js/listings.js*.

*Примечания*.

На странице со списком листингов используется плагин `jQuery Datatables <https://datatables.net/>`_, который настроен так, что данные запрашиваются
динамически. Запрос производится на действие контроллера **data()**.

На странице создания и редактирования листинга для реализации подсказок при заполнении используется
плагин jQuery - `Bootstrap Typeahead <https://github.com/bassjobsen/Bootstrap-3-Typeahead/>`_.