function getInfo() {
    var info = {
        article_id: $('#author').attr('data-id') ? $('#author').attr('data-id') : '0',
        article_title: $('#title').val(),
        article_author: $('#author').val(),
        article_summary: $('#summary').val(),
        article_content: $('#content').val(),
        article_is_draft: '0',
        article_is_hidden: $('#hidden').is(':checked') ? '1' : '0',
        tag_name: '',
        article_create_time: $('#publish').val(),
        _xsrf: $('input[name=_xsrf]').val()
    };
    $('.chips .chip').each(function () {
        var str = $(this).text();
        str = str.substring(0, str.length - 5);
        info.tag_name += str + ',';
    });
    info.tag_name = info.tag_name.substring(0, info.tag_name.length - 1);
    return info;
}

$(function () {
    var mdEditor = editormd('editor-wrapper', {
        width: '100%',
        height: 640,
        syncScrolling: 'single',
        toolbarIcons: function () {
            return [
                "undo", "redo", "|",
                "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                "list-ul", "list-ol", "hr", "|",
                "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime", "pagebreak", "|",
                "goto-line", "watch", "preview", "fullscreen", "clear", "search", "|",
                "help"
            ]
        },
        placeholder: 'Enjoy writting...',
        path: '/statics/editor/lib/',
        delay: 1000,  // 当数据量过大是开启延迟显示
        flowChart: true,  // 开启流程图功能
        emoji: false
    });

    if ($('html').width() < 992) {
        mdEditor.settings.watch = false;  // 屏幕宽度小于一般桌面计算机尺寸时，默认关闭预览，可再次点击watch图标开启；
    }

    $('.chips').material_chip({  // 初始化文章标签模块
        autocompleteOptions: {
            data: {
                'Fuck': null,
                'Microsoft': null,
                'Google': null
            },
            limit: Infinity,
            minLength: 1
        },
        placeholder: '输入文章标签'
    });

    $('.dropdown-button').dropdown({  // 初始化下拉列表
        inDuration: 300,
        outDuration: 225,
        constrain_width: false, // Does not change width of dropdown to that of the activator
        hover: false, // Activate on hover
        gutter: 0, // Spacing from edge
        belowOrigin: true // Displays dropdown below the button
    });

    $('.timepicker').pickatime({
        default: 'now', // default time, 'now' or '13:14' e.g.
        donetext: '保存',
        cleartext: '清除',
        canceltext: '取消',
        autoclose: false,
        ampmclickable: true,
        twelvehour: false,
        vibrate: true
    });

    $('.publish-now').on('click', function () {  // [现在发布]按钮点击事件
        var info = getInfo();
        $.ajax({
            url: $.URL_CONFIG.article.write_api_url,
            type: 'post',
            data: info,
            success: function (response) {
                if (response.status) {
                    Materialize.toast(response.message, 1700, 'btn-primary', function () {
                        window.location = response.result;
                    });
                } else {
                    Materialize.toast(response.message, 1500, 'btn-danger');
                }
            },
            error: function (response) {
                Materialize.toast('未知错误，请与管理员联系', 1500, 'btn-danger');
            }
        });
    });

    $('.update-now').on('click', function () {  // [现在更新]按钮点击事件
        var info = getInfo();
        $.ajax({
            url: $.URL_CONFIG.article.update_api_url,
            type: 'post',
            data: info,
            success: function (response) {
                if (response.status) {
                    Materialize.toast(response.message, 1700, 'btn-primary', function () {
                        window.location = response.result
                    });
                } else {
                    Materialize.toast(response.message, 1500, 'btn-danger');
                }
            },
            error: function (response) {
                Materialize.toast('未知错误，请与管理员联系', 1500, 'btn-danger');
            }
        });
    });

    $('.save-draft').on('click', function () {  // [存为草稿]按钮点击事件
        var info = getInfo();
        info.article_is_draft = '1';
        var tempURL = '';
        if (info.article_id === '0') {
            tempURL = $.URL_CONFIG.article.write_api_url;
        } else {
            tempURL = $.URL_CONFIG.article.update_api_url;
        }
        $.ajax({
            url: tempURL,
            type: 'post',
            data: info,
            success: function (response) {
                if (response.status) {
                    Materialize.toast(response.message, 1700, 'btn-primary', function () {
                        window.location = response.result
                    });
                } else {
                    Materialize.toast(response.message, 1500, 'btn-danger');
                }
            },
            error: function (response) {
                Materialize.toast('未知错误，请与管理员联系', 1500, 'btn-danger');
            }
        });
    });
});