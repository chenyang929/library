$(document).ready(function () {
    //翻页
    $(".bt-page").click(function () {
        goPage($(this).val());
    });

    //选择分页大小
    let per = $("#per");
    per.change(function () {
        selectUser(per.val());
    });

    //搜索用户
    $("#user-search").bind('keypress', function (event) {
        let search_var = $(this).val();
        if (search_var.length!=0 && event.keyCode == 13 ) {
            searchUser(search_var, per.val());
            $(this).val("")
        }
     });

    //编辑用户
    $(".bt-modify-user").click(function () {
        modifyClick($(this))
    });
    $(".modify_submit").click(function () {
        submitClick($(this))
    });

    //新增用户
    $("#user_submit").click(function () {
        let email = $("#email_in").val();
        let name = $("#name_in").val();
        if (email.length>0 && name.length>0) {
            userNew(email, name)
        } else {
            alert("用户信息不完整")
        }
    });
});

function modifyClick(ele) {
    let userId = ele.closest("tr").attr("id");
    let email = ele.closest("tr").find("td.email").text();
    let name = ele.closest("tr").find("th.first_name").text();
    $(".modify_submit").attr("si", userId);
    $("#email_md").val(email);
    $("#name_md").val(name);
}

function submitClick(ele) {
    let email = $("#email_md").val();
    let name = $("#name_md").val();
    if (email.length>0 && name.length>0) {
        let type = ele.attr("name");
        if (type==0) {
            userModify(ele.attr("si"), email, name, 0)
        } else {
            userModify(ele.attr("si"), email, name, 1)
        }

    } else {
        alert('用户修改信息不完整')
    }
}

function goPage(url) {
    $.get(url, userSuccess)
}

function selectUser(per) {
    let url = '/library/api/user';
    $.get(url, {per: per}, userSuccess)
}

function searchUser(name, per) {
    let url = '/library/api/user';
    $.get(url, {name: name, per: per}, userSuccess);
}

function userSuccess(response) {
    let json = eval(response);
    let count = json.count;
    let total_page = json.total_page;
    let page = json.page;
    let next_page = json.next_page;
    let previous_page = json.previous_page;
    let results = json.results;
    let thisPage = '<span class="this-page">' + '第' + page + '页</span> ';
    let previousPage = '<button class="bt-page" value="' + previous_page +'"' + '>' + '上一页</button> ';
    let nextPage = '<button class="bt-page" value="' + next_page + '"' + '>' + '下一页</button> ';
    let totalPage = '<span class="total_page"> 共 ' + total_page + ' 页 </span>';
    let count_t = '<span class="count">' + count + '条结果</span>';
    if (previous_page == null) {
            previousPage = ''
        }
        if (next_page == null) {
            nextPage = ''
        }
    let row = '';
    if (results.length > 0) {
        $.each(results, function (index) {
            let {id, first_name, email} = results[index];
            let action = '<button class="bt-modify-user">' + '编辑' + '</button>';
            row += '<tr class="row1" id="' + id + '">' +
                '<th class="first_name">' + first_name + '</th>' +
                '<td class="email">' + email + '</td>' +
                '<td class="action">' + action + '</td>' +
                '</tr>'
        });
    } else {
        thisPage = '';
        totalPage = '';
    }
    $("#results").html(row);
    $('#paginator').html(thisPage + previousPage + nextPage + totalPage + count_t);
    userAfterLoad()
}

function userAfterLoad() {
    $('.bt-page').bind(
        "click",
        function () {
            goPage($(this).val())
    });
    $('.bt-modify-user').bind(
        "click",
        function () {
            modifyClick($(this))
        }
    )
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

function userModify(userId, email, name, pw) {
    $.ajax({
        url: '/library/api/user/' + userId,
        type: 'POST',
        data: {"user_name": email, "first_name": name, "pw": pw},
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