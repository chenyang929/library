$(document).ready(function () {
    book_select(1, 2);
    if ($("#myhistory").length>0) {
        history('GET',0);
    }
    $("#select").change(function () {
        book_select(1, $(this).val())
    });
    $("#next").click(function () {
        book_select($(this).val(), 2)
    });
    $("#previous").click(function () {
        book_select($(this).val(), 2)
    });

});

function book_select(page, status) {
    let link;
    if (status==1) {
      link = "/library/api/book/status=1/page=" + page
    }else if (status==0) {
      link = "/library/api/book/status=0/page=" + page
    }else {
      link = "/library/api/book/" + 'page=' + page
    }
    $.ajax({
        url: link,
        type: 'GET',
        cache: false,
        dataType: 'json',
        beforeSend: loadFunction,
        error: errorFunction,
        success: succFunction
    });
    function loadFunction() {
        $("#books").html("加载中...");
    }
    function errorFunction() {
        alert("请求失败");
    }
    function succFunction(response) {
        let json = eval(response);
        let results = json.results;
        if (results!=null) {
            let counts = json.counts;
            let next_page = json.next_page;
            let previous_page = json.previous_page;
            let tt = '';
            $.each(results, function (index) {
                let id = results[index].id;
                let book = results[index].book;
                let inventory = results[index].inventory;
                let remain = results[index].remain;
                let str = '<button class="in" value="' + id + '"' + '>'+ '在库' + '</button>';
                if (remain==0) {
                  str = '出库'
                }
                tt += '<tr class="row1">'+
                      '<th class="book">'+book+'</th>'+
                      '<td class="inventory">'+inventory+'</td>'+
                      '<td class="remain">'+remain+'</td>'+
                      '<td class="status">'+str+'</td>'+
                      '</tr>'
            });
            $("#results").html(tt);
            $("#this-page").text("第"+page+"页 ");
            if (previous_page == null) {
              $("#previous").hide()
            } else {
              $("#previous").show().val(previous_page)
            }
            if (next_page == null) {
              $("#next").hide()
            } else {
              $("#next").show().val(next_page)
            }
            $("#count").text(" "+counts+"条结果");
            afterLoad();
        } else {
            $("#results").html('');
            $("#this-page").hide();
            $("#previous").hide();
            $("#next").hide();
            $("#count").text("0条结果");
        }
    }
}
function afterLoad() {
    $(function () {
        $("button").css({
            "background-color": "#4CAF50",
            "font-size": "15px",
            "border-radius": "2px",
            "color": "white",
            "border": "0",
        });
        $("#next").css({
            "background-color": "#008CBA",
            "font-size": "15px",
            "border-radius": "2px",
            "color": "white",
            "border": "0",
        });
        $("#previous").css({
            "background-color": "#008CBA",
            "font-size": "15px",
            "border-radius": "2px",
            "color": "white",
            "border": "0",
        });
        $(".in").bind(
            "click",
            function () {
                 if(confirm("确定借阅?")){
                     history('POST', $(this).val())
                }
            }
        )
    });
}

function history(type, id) {
  let link;
  if (type=="POST") {
    link = '/library/api/history/'+id+'/'
  } else {
    link = '/library/api/history/'
  }
    $.ajax({
        url: link,
        type: type,
        cache: false,
        dataType: 'json',
        xhrFields: {
             withCredentials: true
        },
        crossDomain: true,
        beforeSend: loadFunction,
        error: errorFunction,
        success: succFunction
    });
    function loadFunction(xhr) {
        xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
    }
    function errorFunction() {
        alert("请求失败");
    }
    function succFunction(response){
      let json = eval(response);
      if (type=='POST') {
          let message = json.message;
          if (message=='anonymous') {
              if(confirm("请先登录")){
                     location.href = '/login/'
                }
          } else {
              alert(json.message);
              book_select(1, $("#select").val());
              history('GET',0);
          }
      } else {
        let results = json.history;
        let tt = '';
        if (results==null) {
          tt = '<span><pre>暂无借阅历史</pre></span>'
        } else {
          $.each(results, function (index) {
            let id = results[index].id;
            let book = results[index].book;
            let borrow_date = results[index].borrow_date;
            let status = results[index].status;
            let str = '借阅中';
            let action = '';
            if (status==0) {
              str = '已归还';
            } else if (status==1) {
              str = '借阅中';
              action = '<button class="back" value="' + id + '"' + '>'+ '归还' + '</button>';
            } else if (status==2) {
              str = '借阅审核中';
            } else if(status==3) {
              str = '归还审核中';
            } else if(status==4) {
              str = '借阅驳回';
            }
            tt += '<tr class="row2">'+
                  '<td class="history_date">'+borrow_date+'</td>'+
                  '<th class="history_book">'+book+'</th>'+
                  '<td class="history_status">'+str+'</td>'+
                  '<td class="history_action">'+action+'</td>'+
                  '</tr>'
        });
        }
        $("#history").html(tt);
      }
      afterHistoryLoad();
    }
}
function afterHistoryLoad() {
    $(function () {
        $(".back").bind(
            "click",
            function () {
                if(confirm("确认归还该书")){
                     book_back($(this).val())
                }
            }
        )
    })
}
function book_back(id) {
    $.ajax({
        url: '/library/api/back/'+id+'/',
        type: 'POST',
        cache: false,
        dataType: 'json',
        xhrFields: {
             withCredentials: true
        },
        crossDomain: true,
        beforeSend: loadFunction,
        error: errorFunction,
        success: succFunction
    });
    function loadFunction(xhr) {
        xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
    }
    function errorFunction() {
        alert("操作失败");
    }
    function succFunction(response) {
      let json = eval(response);
      alert(json.message);
      history('GET',0);
    }
}