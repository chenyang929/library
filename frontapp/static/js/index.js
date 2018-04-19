$(document).ready(function () {
    $("#select").change(function () {
        storageList($(this).val(), 1);
    });
    $(".button1").click(function () {
        storageList($("#select").val(), $(this).val());
    });
    $(".button2").click(function () {
        if(confirm("确认借阅该书1")){
            historyList('POST', $(this).val())
        }
    });
    $(".button3").click(function () {
        if(confirm("确认归还该书1")){
            backBook($(this).val())
        }
    });
});

function storageList(remain, page) {
    $.ajax({
        url: '/library/storage' + '?remain=' + remain + '&page=' + page,
        type: 'GET',
        cache: false,
        dataType: 'json',
        error: errorFunction,
        success: successFunction
    });

    function errorFunction() {
        alert("请求失败");
    }

    function successFunction(response) {
        let json = eval(response);
        let results = json.results;
        if (results != null) {
            let next_page = json.next_page;
            let previous_page = json.previous_page;
            let row = '';
            $.each(results, function (index) {
                let {id, book, inventory, remain} = results[index];
                let action = '<button class="button2" value="' + id + '"' + '>' + '借阅' + '</button>';
                let str = '在库';
                if (remain == 0) {
                    str = '出库';
                    action = ''
                }
                row += '<tr class="row1">' +
                    '<th class="book">' + book + '</th>' +
                    '<td class="inventory">' + inventory + '</td>' +
                    '<td class="remain">' + remain + '</td>' +
                    '<td class="status">' + str + '</td>' +
                    '<td class="action">' + action + '</td>' +
                    '</tr>'
            });
            $("#results").html(row);
            let thisPage = '<span class="this-page">' + '第' + page + '页</span> ';
            let previousPage = '<button class="button1" value="' + previous_page +'"' + '>' + '上一页</button> ';
            let nextPage = '<button class="button1" value="' + next_page + '"' + '>' + '下一页</button> ';
            let count = '<span class="count">' + json.counts + '条结果</span>';
            if (previous_page == null) {
                previousPage = ''
            }
            if (next_page == null) {
                nextPage = ''
            }
            $('#paginator').html(thisPage + previousPage + nextPage + count);
            storageListAfterLoad()

        }
    }
}

function storageListAfterLoad() {
    $('.button1').bind(
        "click",
        function () {
            storageList($("select").val(), $(this).val())
    });
    $('.button2').bind(
        "click",
        function () {
            if(confirm("确认借阅该书2")){
            historyList('POST', $(this).val())
        }
    });
}

function historyList(type, storageId) {
    $.ajax({
        url: '/library/history/',
        data: {"storage_id": storageId},
        type: type,
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
        if (type == 'POST') {
            let s = $(".this-page").text();
            let m = s.match(/[0-9]+/);
            if (m == null) {
                m = '1'
            }
            storageList($("#select").val(), m);
            historyList('GET', 1)
        } else if (type == 'GET') {
            let json = eval(response);
            let results = json.history;
            let row = '';
            if (results != null) {
                $.each(results, function (index) {
                    let {id, book, borrow_date, status} = results[index];
                    let str = '借阅中';
                    let action = '<button class="button3" value="' + id + '">' + '归还</button>';
                    switch (status) {
                        case 0:
                            str = '借阅不通过';
                            action = '';
                            break;
                        case 1:
                            str = '借阅审批中';
                            action = '';
                            break;
                        case 3:
                            str = '归还不通过';
                            break;
                        case 4:
                            str = '归还审批中';
                            action = '';
                            break;
                        case 5:
                            str = '已归还';
                            action = '';
                            break;
                    }
                    row += '<tr class="row2">' +
                        '<th class="history_date">' + borrow_date + '</th>' +
                        '<td class="history_book">' + book + '</td>' +
                        '<td class="history_status">' + str + '</td>' +
                        '<td class="history_action">' + action + '</td>' +
                        '</tr>'
                });
                $("#history").html(row);
            }
        }
        if (type == 'GET') {
            historyListAfterLoad();
        }
    }
}

function historyListAfterLoad() {
    $('.button3').bind(
        "click",
        function () {
            if(confirm("确认归还该书2")){
            backBook($(this).val())
        }
    });
}

function backBook(historyId) {
    $.ajax({
        url: '/library/history/' + historyId,
        type: 'POST',
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
        historyList('GET', 1);
    }
}


