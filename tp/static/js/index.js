$(document).ready(function () {
    //选择图书状态和分页大小
    let select = $("#select");
    let per = $("#per");
    select.change(function () {
        selectStorage(select.val(), per.val())
    });
    per.change(function () {
        selectStorage(select.val(), per.val());
    });

    //搜索图书
    $("#book-search").bind('keypress', function (event) {
        let search_var = $(this).val();
        if (search_var.length!=0 && event.keyCode == 13 ) {
            searchStorage(search_var, per.val());
            $(this).val("")
        }
     });

    //借阅图书
    $(".bt-storage").click(function () {
        btStorageClick($(this))
    });

    //翻页
    $(".bt-page").click(function () {
        goPage($(this).val());
    });

    //归还图书
    $(".bt-history").click(function () {
        let book = $(this).closest("tr").find("th.history_book").text();
        let historyId = $(this).val();
        if (confirm(book + "? 归还")){
            historyDetailPost(historyId, $(this));
        }
    })
});

function btStorageClick(ele) {
    let book = ele.closest("tr").find("th.book").text();
    let storageId = ele.closest("tr").attr("id");
    if(confirm(book + "？借阅")){
        historyListPost(storageId)
    }
}

function selectStorage(remain, per) {
    let url = '/library/api/storage';
    $.get(url, {remain: remain, per: per}, storageSuccess)
}

function searchStorage(book, per) {
    let url = '/library/api/storage';
    $.get(url, {book: book, per: per}, storageSuccess);
}

function goPage(url) {
    $.get(url, storageSuccess)
}

function storageSuccess(response) {
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
            let {id, book, inventory, remain} = results[index];
            let action = '<button class="bt-storage" title="点击借阅">' + '借阅' + '</button>';
            let str = '在库';
            if (remain == 0) {
                str = '出库';
                action = ''
            }
            row += '<tr class="row1" id="' + id + '">' +
                '<th class="book">' + book + '</th>' +
                '<td class="inventory">' + inventory + '</td>' +
                '<td class="remain">' + remain + '</td>' +
                '<td class="status">' + str + '</td>' +
                '<td class="action">' + action + '</td>' +
                '</tr>'
        });
    } else {
        thisPage = '';
        totalPage = '';
    }
    $("#results").html(row);
    $('#paginator').html(thisPage + previousPage + nextPage + totalPage + count_t);
    storageAfterLoad()
}

function storageAfterLoad() {
    $('.bt-page').bind(
        "click",
        function () {
            goPage($(this).val())
    });
    $('.bt-storage').bind(
        "click",
        function () {
            btStorageClick($(this))
        }
    )
}

function historyListPost(storageId) {
    $.ajax({
        url: '/library/api/history/',
        data: {"storage_id": storageId},
        type: 'POST',
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
            $("#" + storageId + " td.status").text("出库");
            $("#" + storageId + " td.remain").text("0");
            $("#" + storageId + " td.action").text("");
            let book = json["results"][0]["book"];
            let borrow_date = json["results"][0]["borrow_date"];
            historyShow(book, borrow_date);
        } else {
            alert(msg)
        }
    }
}

function historyShow(book, borrow_date) {
    let row = '<tr class="row2">' +
              '<th class="history_book">' + book + '</th>' +
              '<td class="history_borrow_date">' + borrow_date + '</td>' +
              '<td class="history_back_date"></td>' +
              '<td class="history_status">' + '借阅审核中' + '</td>' +
              '<td class="history_action"></td></tr>';
    $("#history").prepend(row);
}

function historyDetailPost(historyId, ele) {
    $.ajax({
        url: '/library/api/history/' + historyId,
        type: 'POST',
        data: {"status": 4},
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
            let status = ele.closest("tr").find("td.history_status").text();
            if (status == '借阅中' || status == '归还不通过') {
                ele.closest("tr").find("td.history_status").text("归还审核中");
                ele.closest("tr").find("td.history_action").text("")
            }
        } else {
            alert(msg)
        }
    }
}

