$(document).ready(function () {
    $("#pw_submit").click(function () {
        let pw = $("#pw").val();
        let pw1 = $("#pw1").val();
        if (pw.length>0 && pw == pw1) {
            //alert(pw);
            pwChange($("#pw_submit").val(), pw)
        } else {
            alert("两次密码不一致")
        }
    });
});

function pwChange(userId, pw) {
    $.ajax({
        url: '/library/api/user/' + userId,
        type: 'POST',
        data: {"pw": pw},
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
        alert("请重新登录");
        $.removeCookie('csrftoken');
        location.href = '/library/'
    }
}