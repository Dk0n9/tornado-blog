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
                Materialize.toast(response.message, 1700, '', function () {
                    window.location = response.result;
                });
            } else {
                Materialize.toast(response.message, 1500, 'error');
            }
        }
    })
}

$(document).ready(function () {
    $(".button-collapse").sideNav();
});
