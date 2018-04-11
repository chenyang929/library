function register()
{
let xmlhttp;
if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp=new XMLHttpRequest();
  }
else
  {// code for IE6, IE5
  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
xmlhttp.onreadystatechange=function()
  {
  if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
        let result = xmlhttp.responseText;
        let result_json = JSON.parse(result);
        if (result_json['message'] == 'failed') {
            alert("用户名或密码错误");
        } else {
            alert('ok');
            window.location.href = "/library/";
        }
    }
  };
let username = document.getElementById('id_username').value;
let password = document.getElementById('id_password').value;
xmlhttp.open("POST","/login/api/login/",true);
xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
xmlhttp.send("username="+username+"&"+"password="+password);
}