$(document).ready(function () {
    //翻页
    $(".bt-page").click(function () {
        goPage($(this).val());
    });

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

    //编辑图书
    $(".bt-modify-storage").click(function () {
        alert($(this).text())
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
});

function goPage(url) {
    $.get(url, storageSuccess)
}

function selectStorage(remain, per) {
    let url = '/library/api/storage';
    $.get(url, {remain: remain, per: per}, storageSuccess)
}

function searchStorage(book, per) {
    let url = '/library/api/storage';
    $.get(url, {book: book, per: per}, storageSuccess);
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
            let action = '<button class="bt-modify-storage">' + '编辑' + '</button>';
            let str = '在库';
            if (remain == 0) {
                str = '出库';
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
    $('.bt-modify-storage').bind(
        "click",
        function () {
            alert($(this).text())
        }
    )
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