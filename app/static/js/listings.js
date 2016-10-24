var fillAgentFields = function(agent) {
    $("#agent_name").val(agent.name);
    $("#agent_phone").val(agent.phone_numbers);
    $("#agent_email").val(agent.email);
};

/**
 * Превращает поля в поля с подсказками
 */
var typeaheadFields = function(cityId) {
    // Обнуление typeahead, если остались с "прошлого" раза
    $('#agent_name').typeahead('destroy');
    $('#agent_phone').typeahead('destroy');
    $('#agent_email').typeahead('destroy');
    $('#street_address').typeahead('destroy');
    $('#suburb').typeahead('destroy');
    $('#appraised_by').typeahead('destroy');

    // Автоподсказки для поля Agent name
    $.get('/agents/names.json/' + cityId + '/', function(data){
        $("#agent_name").typeahead({
            source: data,
            afterSelect: function () {
                $.get('/agents/get_agent_by_name/' + $("#agent_name").val(), function(data){
                    fillAgentFields(data);
                }, 'json');
            }
        });
    }, 'json');

    // Автоподсказки для поля Agent phone
    $.get('/agents/phones.json/' + cityId + '/', function(data){
        $("#agent_phone").typeahead({
            source: data,
            afterSelect: function () {
                $.get('/agents/get_agent_by_phone/' + $("#agent_phone").val(), function(data){
                    fillAgentFields(data);
                }, 'json');
            }
        });
    }, 'json');

    // Автоподсказки для поля Agent email
    $.get('/agents/emails.json/' + cityId + '/', function(data){
        $("#agent_email").typeahead({
            source: data,
            afterSelect: function () {
                $.get('/agents/get_agent_by_email/' + $("#agent_email").val(), function(data){
                    fillAgentFields(data);
                }, 'json');
            }
        });
    }, 'json');

    // Автополдсказки для поля Street name
    $.get('/listings/street-addresses.json/' + cityId + '/', function(data){
        $("#street_address").typeahead({
            source: data
        });
    }, 'json');

    // Автоподсказки для поля Suburb
    $.get('/listings/suburbs.json/' + cityId + '/', function(data){
        $("#suburb").typeahead({
            source: data
        });
    }, 'json');

    // Автоподсказки для поля Appraised by
    $.get('/managers/names.json/' + cityId + '/', function(data){
        $("#appraised_by").typeahead({
            source: data
        });
    }, 'json');
};

$(function () {
    // Инициализация плагина DataTable
    $('#data-listings').DataTable({
        "stateSave": true,
        "processing": true,
        "serverSide": true,
        "ajax": "/listings/data/"
    });

    // Инициализация плагина select2
    $(".select2").select2();

    // Обработчик изменения значения поля City
    $("#city_id").change(function () {
        // Превращение полей в поля с подсказками
        typeaheadFields($("#city_id").val());
    });

    // Обработчик изменения значения поля Property type
    $("#property_type").change(function () {
        if ($("#property_type").val() == 'House') {
            $('#bedrooms').val('3');
            $('#bedrooms').trigger('change.select2');
        }
    });

    // Обработчик отправки формы
    $( "#listing-form-submit" ).click(function() {
        // Если поле Appraised by не заполнено, то отправляем форму
        if ($("#appraised_by").val() == '') {
            $( "#listing-form" ).submit();
        } else {
            // Проверка существует ли выбранный менеджер
            $.get('/managers/get_manager_by_name/' + $("#appraised_by").val() + '/' + $("#city_id").val() + '/')
            // Если существует - отправка формы
            .success(function () {
                $("#listing-form").submit();
            })
            // Если не существует - демонстрация формы создания менеджера
            .fail(function () {
                $('#manager_name').val($("#appraised_by").val());
                $('#manager-modal-form').modal();
            });
        }
    });

    // Обработчик создания менеджера с помощью модальной формы
    $( "#manager-form-submit" ).click(function () {
        // Отправка данных на сохранение
        $.post( "/managers/create/",
            {
                name: $("#manager_name").val(),
                phone_numbers: $("#manager_phone").val(),
                email: $("#manager_email").val(),
                city_id: $("#city_id").val()
            }
        )
        // Если менеджер создан успешно
        .success(function () {
            // Закрытие модальной формы
            $( "#manager-modal-form" ).modal("hide");
            // Очистка сообщений об ошибках
            $('#manager-modal-form-errors').html('');
            // Обновление значения поля appraised_by основной формы
            $("#appraised_by").val($("#manager_name").val());
            // Отправка основной формы
            $( "#listing-form" ).submit();
        })
        // Если есть ошибки (валидация)
        .fail(function (data) {
            $('#manager-modal-form-errors').html(data.responseText);
        });
    });
});