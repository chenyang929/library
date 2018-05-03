$(document).ready(function () {
    //借阅审核
    $(".bt-yn").click(function () {
        let historyId = $(this).closest("tr").attr("id");
        historyYesNo(historyId, $(this).attr("name"))
    });
});

function historyYesNo(historyId, msg) {
    $.ajax({
        url: '/library/api/history/' + historyId,
        type: 'POST',
        data: {"msg": msg},
        cache: false,
        dataType: 'json',
        xhrFields: {
             withCredentials: true
        },
        crossDomain: true,
        beforeSend: loadFunction,
        error: errorFunction,
        success: successFunction
    });
    function loadFunction(xhr) {
        xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
    }
    function errorFunction() {
            alert("请求失败");
        }
    function successFunction(response) {
        $("tr#" + historyId).hide();
    }
}

