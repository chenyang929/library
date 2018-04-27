$(document).ready(function () {
    //借阅审核
    $(".bt-yn").click(function () {
        let historyId = $(this).closest("tr").attr("id");
        historyYesNo(historyId, $(this).attr("name"))
    });
    //新增借阅
    $("#history_submit").click(function () {
        let userId = $("#changelist-check select.user").val();
        let storageId = $("#changelist-check select.book").val();
        historyNew(userId, storageId);
    });
    //新增图书
    $("#storage_submit").click(function () {
        let book = $("#book_in").val();
        let inventory = $("#inventory_in").val();
        if (book.length > 0 && inventory.length >0) {
            storageNew(book, inventory)
        } else {
            alert("入库信息缺失")
        }
    });
    //新增用户
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

function historyNew(userID, storageId) {
    $.ajax({
        url: '/library/api/history/',
        type: 'POST',
        data: {"user_id": userID, "storage_id": storageId},
        //cache: false,
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
        let json = eval(response);
        let msg = json.info;
        if (msg == 'success') {
            alert("新增借阅成功")
        }
        location.href = '/library/backend'
    }

}
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

function storageNew(book, inventory) {
    $.ajax({
        url: '/library/api/storage',
        type: 'POST',
        data: {"book": book, "inventory": inventory},
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
        let json = eval(response);
        let msg = json.info;
        if (msg == 'success') {
            location.href = '/library/backend/storage'
        } else{
            alert(msg)
        }
    }
}

function userNew(email, name) {
    $.ajax({
        url: '/library/api/user/',
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
        let json = eval(response);
        let msg = json.info;
        if (msg == 'success') {
            location.href = '/library/backend/user'
        } else{
            alert(msg)
        }
    }
}