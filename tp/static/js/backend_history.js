$(document).ready(function () {
    //翻页
    $(".bt-page").click(function () {
        goPage($(this).val());
    });

    //选择状态和分页大小
    let select = $("#select");
    let per = $("#per");
    select.change(function () {
        selectHistory(select.val(), per.val());
    });
    per.change(function () {
        selectHistory(select.val(), per.val());
    });

    //搜索
    $("#history-search").bind('keypress', function (event) {
        let search_var = $(this).val();
        if (search_var.length!=0 && event.keyCode == 13 ) {
            let choice = $('#choice-search').val();
            if (choice==0) {
                searchUser(search_var, per.val());
            } else {
                searchBook(search_var, per.val());
            }
            $(this).val("")
        }
     });

    //编辑
    $(".bt-modify-history").click(function () {
        alert($(this).text())
    });

    //新增借阅
    $("#history_submit").click(function () {
        let userId = $("#changelist-check select.user").val();
        let storageId = $("#changelist-check select.book").val();
        historyNew(userId, storageId);
    });
});

function goPage(url) {
    $.get(url, historySuccess)
}

function selectHistory(status, per) {
    let url = '/library/api/history';
    $.get(url, {status: status, per: per}, historySuccess)
}

function searchBook(book, per) {
    let url = '/library/api/history';
    $.get(url, {book: book, per: per}, historySuccess);
}

function searchUser(user, per) {
    let url = '/library/api/history';
    $.get(url, {user: user, per: per}, historySuccess);
}


function historySuccess(response) {
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
            let {id, book, user, borrow_date, back_date, status, delay} = results[index];
            let action = '<button class="bt-modify-history">' + '编辑' + '</button>';
            let str = '已归还';
            if (status==0) {
                str = '借阅不通过'
            } else if (status==1) {
                str = '借阅审核中'
            } else if (status==2) {
                str = '借阅中'
            } else if (status==3) {
                str = '归还不通过'
            } else if (status==4) {
                str = '归还审核中'
            }
            let d = '否';
            if (delay==1) {
                d = '是'
            }
            row += '<tr class="row1" id="' + id + '">' +
                '<th class="book">' + book + '</th>' +
                '<td class="user">' + user + '</td>' +
                '<td class="borrow_date">' + borrow_date + '</td>' +
                '<td class="back_date">' + back_date + '</td>' +
                '<td class="status">' + str + '</td>' +
                '<td class="delay">' + d + '</td>' +
                '<td class="action">' + action + '</td>' +
                '</tr>'
        });
    } else {
        thisPage = '';
        totalPage = '';
    }
    $("#results").html(row);
    $('#paginator').html(thisPage + previousPage + nextPage + totalPage + count_t);
    historyAfterLoad()
}

function historyAfterLoad() {
    $('.bt-page').bind(
        "click",
        function () {
            goPage($(this).val())
    });
    $('.bt-modify-history').bind(
        "click",
        function () {
            alert($(this).text())
        }
    )
}

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
        location.href = '/library/backend/history'
    }

}
