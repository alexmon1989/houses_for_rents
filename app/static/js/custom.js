$(function () {

    // Все таблицы с id="data" превращаются в datatables
    $('table#data').DataTable({
        "stateSave": true
    });

    // Подтверждение удаления
    $('body').on('click', 'a.delete', function() {
        return confirm('Are you sure?');
    });
});