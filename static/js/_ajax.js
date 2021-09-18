function login() {
    var username = $.trim(document.getElementById('user-login').value);
    var pwd = $.trim(document.getElementById('user-password').value);
    var stayloggedin = document.getElementById('remember').checked;
    $.ajax({
        url : "/auth",
        type : "post",
        data : {
            username: username,
            password : pwd,
            remember : stayloggedin
        }
    }).done(function(data) {
        var data = JSON.parse(JSON.stringify(data));
        if (data) {
            if (data["status"] == "success") {
                window.location.replace("/");
            }
            else if (data["status"] == "error") {
                alert(data["error_text"]);
            }

        }
    });
}


function like() {
    $.ajax({
        url : "like",
        type : "post",
    }).done(function(data) {
        var data = JSON.parse(JSON.stringify(data));
        if (data) {
            if (data["status"] == "success") {
                window.location.replace("/");
            }
            else if (data["status"] == "error") {
                alert(data["error_text"]);
            }

        }
    });
}


$('.modal-login-btn').click(login);