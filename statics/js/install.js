$(function () {
    $('#reset-btn').bind('click', function () {
        $('#setup-container input').each(function () {
            $(this).val('');
            $(this).removeClass('valid');
            $(this).next().removeClass('active');
        });
    });

    $('#setup-btn').bind('click', function () {
        $('#setup-container input').each(function () {
            if (!$(this).val()) {
                alert($(this).next().text() + '不能为空');
                $(this).focus();
                return false;
            }
        });
        var _token = $('input[name=_xsrf]').val();
        var title = $('#title').val();
        var user = $('#user').val();
        var passwd = $('#passwd').val();
        var confirm = $('#confirm').val();
        $.ajax({
            url: '/install',
            type: 'post',
            data: {
                title: title,
                user: user,
                passwd: passwd,
                _xsrf: _token
            },
            success: function (response) {
                if (response.status) {
                    M.toast({
                        html: response.message,
                        displayLength: 1500,
                        classes: 'btn-success'
                    });
                } else {
                    M.toast({
                        html: response.message,
                        displayLength: 1500,
                        classes: 'btn-warning'
                    });
                }
            }
        });
    });
});