$(document).ready(function () {
    $(".button4").click(function () {
        historyYesNo($(this).val(), $(this).text())
    });
    $("#book_submit").click(function () {
        if ($("#book_in").val().length > 0) {
            bookNew($("#book_in").val())
        } else {
            alert("请输入图书名")
        }
    });
    $("#user_submit").click(function () {
        let email = $("#email_in").val();
        let name = $("#name_in").val();
        if (email.length>0 && name.length>0) {
            //alert('ok');
            userNew(email, name)
        } else {
            alert("用户信息不完整")
        }
    });
});

function historyYesNo(historyId, msg) {
    $.ajax({
        url: '/library/history/' + historyId,
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
        location.href = '/library/backend/'
    }
}

function bookNew(book) {
    $.ajax({
        url: '/library/storage',
        type: 'POST',
        data: {"book": book},
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
        alert("新书入库成功");
        location.href = '/library/backend/'
    }
}

function userNew(email, name) {
    $.ajax({
        url: '/library/user/',
        type: 'POST',
        data: {"email": email, "name": name},
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
        let info = eval(response).info;
        alert(info);
        location.href = '/library/backend/'
    }
}