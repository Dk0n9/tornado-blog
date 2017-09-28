function login(url) {
    let username = $('#user_prefix').val();
    let password = $('#pass_prefix').val();
    let _token = $('input[name=_xsrf]').val();
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
