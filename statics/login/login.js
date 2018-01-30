function login(url) {
    var username = $('#user_prefix').val();
    var password = $('#pass_prefix').val();
    var _token = $('input[name=_xsrf]').val();
    $.ajax({
        url: url,
        type: 'post',
        data: {
            user_name: username,
            user_pwd: password,
            _xsrf: _token
        },
        success: function (response) {
            if (response.status) {
                M.toast({
                    html: response.message,
                    displayLength: 1500,
                    classes: 'btn-success',
                    completeCallback: function () {
                        window.location = response.result;
                    }
                });
            } else {
                M.toast({
                    html: response.message,
                    displayLength: 1500,
                    classes: 'btn-warning'
                });
            }
        }
    })
}

$(document).ready(function () {
    $(".button-collapse").sidenav();
});
