function getInfo() {
    var info = {
        postID: $('#author').attr('data-id') ? $('#author').attr('data-id') : '0',
        postTitle: $('#title').val(),
        postAuthor: $('#author').val(),
        postSummary: $('#summary').val(),
        postContent: $('#content').val(),
        postIsDraft: '0',
        postIsHidden: $('#hidden').is(':checked') ? '1' : '0',
        tagName: '',
        postCreateTime: $('#publish_date').val() + ' ' + $('#publish_time').val(),
        _xsrf: $('input[name=_xsrf]').val()
    };
    $('.chips .chip').each(function () {
        var str = $(this).text();
        str = str.substring(0, str.length - 5);
        info.tagName += str + ',';
    });
    info.tagName = info.tagName.substring(0, info.tagName.length - 1);
    return info;
}

function getChips(postID) {
    var chipData = [];
    var autoCompleteData = {};
    if (postID) {
        $.ajax({
            url: $.URL_CONFIG.post.tags_api_url,
            type: 'post',
            async: false,
            data: {
                'postID': postID,
                '_xsrf': $('input[name=_xsrf]').val()
            },
            success: function (response) {
                if (response.status) {
                    chipData = response.result;
                }
            }
        })
    }
    $.ajax({
        url: $.URL_CONFIG.post.tags_api_url,
        type: 'post',
        async: false,
        data: {
            '_xsrf': $('input[name=_xsrf]').val()
        },
        success: function (response) {
            if (response.status) {
                autoCompleteData = response.result;
            }
        }
    });
    return {
        'data': chipData,
        'autoCompleteData': autoCompleteData
    }
}

$(function () {
    $.EDITOR_CONFIG.height = 640;
    $.EDITOR_CONFIG.syncScrolling = 'single';
    var mdEditor = editormd('editor-wrapper', $.EDITOR_CONFIG);

    if ($('html').width() < 992) {
        mdEditor.settings.watch = false;  // 屏幕宽度小于一般桌面计算机尺寸时，默认关闭预览，可再次点击watch图标开启；
    }

    var chipData = getChips($('#author').attr('data-id'));
    $('.chips').chips({  // 初始化文章标签模块
        //data: chipData['data'],
        // autocompleteOptions: {
        //     data: chipData['autoCompleteData'],
        //     limit: Infinity,
        //     minLength: 1
        // },
        placeholder: '输入文章标签'
    });

    $('.datepicker').datepicker({
        format: 'yyyy/mm/dd',
        firstDay: 1  // Set Monday as the first day of week
    });

    $('.timepicker').timepicker({
        default: 'now', // default time, 'now' or '13:14' e.g.
        autoclose: false,
        ampmclickable: true,
        twelvehour: false,
        vibrate: true,
        twelveHour: false
    });

    $('.publish-now').on('click', function () {  // [现在发布]按钮点击事件
        var info = getInfo();
        $.ajax({
            url: $.URL_CONFIG.post.write_api_url,
            type: 'post',
            data: info,
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
            },
            error: function (response) {
                M.toast({
                    html: '未知错误，请与管理员联系',
                    displayLength: 1500,
                    classes: 'btn-danger'
                });
            }
        });
    });

    $('.update-now').on('click', function () {  // [现在更新]按钮点击事件
        var info = getInfo();
        $.ajax({
            url: $.URL_CONFIG.post.update_api_url,
            type: 'post',
            data: info,
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
            },
            error: function (response) {
                M.toast({
                    html: '未知错误，请与管理员联系',
                    displayLength: 1500,
                    classes: 'btn-danger'
                });
            }
        });
    });

    $('.save-draft').on('click', function () {  // [存为草稿]按钮点击事件
        var info = getInfo();
        info.postIsDraft = '1';
        var tempURL = '';
        if (info.postID === '0') {
            tempURL = $.URL_CONFIG.post.write_api_url;
        } else {
            tempURL = $.URL_CONFIG.post.update_api_url;
        }
        $.ajax({
            url: tempURL,
            type: 'post',
            data: info,
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
            },
            error: function (response) {
                M.toast({
                    html: '未知错误，请与管理员联系',
                    displayLength: 1500,
                    classes: 'btn-danger'
                });
            }
        });
    });
});