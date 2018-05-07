$(document).ready(function () {
    //借阅审核
    $(".bt-yn").click(function () {
        let historyId = $(this).closest("tr").attr("id");
        let type = $(this).attr('name');
        let st = $(this).closest("tr").attr("st");
        let status = 2;
        alert(type);
        if (type=='y') {
            if (st==4) {
                status=5
            }
        } else {
            if (st==1) {
                status=0
            } else {
                status=3
            }
        }
        historyYesNo(historyId, status)
    });
});

function historyYesNo(historyId, status) {
    $.ajax({
        url: '/library/api/history/' + historyId,
        type: 'POST',
        data: {"status": status},
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
