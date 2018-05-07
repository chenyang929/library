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
        modifyClick($(this));
    });
    $("#modify_submit").click(function () {
        submitClick($(this))
    });

    //新增借阅
    $.datetimepicker.setLocale('zh');
    $("#datetimepicker1").datetimepicker({
        timepicker: false,
        format: 'Y-m-d',
    });

    $("#history_submit").click(function () {
        let userId = $("#changelist-check select.user").val();
        let storageId = $("#changelist-check select.book").val();
        let borrowDate = $("#datetimepicker1").val();
        if (borrowDate.length>0) {
            historyNew(userId, storageId, borrowDate);
        } else {
            alert('请选择日期')
        }

    });

});

function modifyClick(ele) {
    let historyId = ele.closest("tr").attr("id");
    let book = ele.closest("tr").find("th.book").text();
    let user = ele.closest("tr").find("td.user").text();
    let status = ele.closest("tr").attr("st");
    let borrow_date = ele.closest("tr").find("td.borrow_date").text();
    let delay = ele.closest("tr").attr("dy");
    $("#modify_submit").attr("si", historyId);
    $("#book_md").val(book);
    $("#user_md").val(user);
    $("#status_md").val(status);
    $("#borrow_md").val(borrow_date);
    $("#delay_md").val(delay);
    $(".modify-div").slideDown();
}

function submitClick(ele) {
    let book = $("#book_md").val();
    let user = $("#user_md").val();
    let status = $("#status_md").val();
    let borrow_date = $("#borrow_md").val();
    let delay = $("#delay_md").val();
    if (book.length>0 && user.length>0 && borrow_date.length>0) {
        historyModify(ele.attr("si"), status, delay);
        $("#book_md").val("");
        $("#user_md").val("");
        $("#borrow_md").val("");
        $("#status_md").val("2");
        $(".modify-div").slideUp();
    } else {
        alert('借阅修改信息不完整')
    }
}

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
            let action = '';
            let str = '已归还';
            if (status==0) {
                str = '借阅不通过'
            } else if (status==1) {
                str = '借阅审核中'
            } else if (status==2) {
                str = '借阅中';
                action = '<button class="bt-modify-history">' + '编辑' + '</button>'
            } else if (status==3) {
                str = '归还不通过'
            } else if (status==4) {
                str = '归还审核中'
            }
            let d = '否';
            if (delay==1) {
                d = '是'
            }
            row += '<tr class="row1" id="' + id + '" st="' + status + '" dy="' + delay + '">' +
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
            modifyClick($(this))
        }
    )
}

function historyNew(userID, storageId, borrowDate) {
    $.ajax({
        url: '/library/api/history/',
        type: 'POST',
        data: {"user_id": userID, "storage_id": storageId, "borrow_date": borrowDate},
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

function historyModify(historyId, status, delay) {
    $.ajax({
        url: '/library/api/history/' + historyId,
        type: 'POST',
        data: {"status": status, "delay": delay},
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
            //location.href = '/library/backend/history'
            let status = json["results"][0]['status'];
            let delay = json["results"][0]['delay'];
            let backDate = json["results"][0]['back_date'];
            $("tr#"+ historyId).find("td.back_date").text(backDate);
            if (status==5) {
                $("tr#"+ historyId).find("td.status").text("已归还");
                $("tr#"+ historyId).find("td.action").html("");
            }
            if (delay==0) {
                $("tr#"+ historyId).find("td.delay").text("否");
            } else {
                $("tr#"+ historyId).find("td.delay").text("是");
            }
        } else{
            alert(msg)
        }
    }
}