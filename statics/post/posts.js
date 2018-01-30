function deletePost() {
    var postID = $('.post-delete').attr('data-id');
    var postTitle = $('.post-title').text().substr(0, $('.post-title').text().length - 21);
    var isDelete = confirm('是否删除文章： ' + postTitle);
    if (isDelete === true) {
        $.ajax({
            url: $.URL_CONFIG.post.delete_page_url,
            type: 'post',
            data: {
                'post_id': postID,
                '_xsrf': $('input[name=_xsrf]').val()
            },
            success: function (response) {
                if (response.status) {
                    M.toast({
                        html: response.message,
                        displayLength: 1500,
                        classes: 'btn-success'
                    });
                    $('.post-link[data-id="' + postID + '"]').fadeOut(700, function () {
                        $(this).remove()
                    });
                    $('#post-details').fadeOut(700);
                } else {
                    M.toast({
                        html: response.message,
                        displayLength: 1500,
                        classes: 'btn-warning'
                    });
                }
            }
        });
    } else {
        return true;
    }
}

function showPostDetails(postID) {
    $.ajax({
        url: $.URL_CONFIG.post.info_api_url,
        type: 'post',
        data: {
            'post_id': postID,
            '_xsrf': $('input[name=_xsrf]').val()
        },
        success: function (response) {
            if (response.status) {
                $('.selected').removeClass('selected');
                $('.post-link[data-id="' + postID + '"]').addClass('selected');
                var viewHTML = '<a href="/post/' + postID + '" target="_blank" class="cyan-text"><i class="material-icons right">open_in_new</i></a>';
                var editHTML = '<a href="' + $.URL_CONFIG.post.edit_page_url + '?id=' + postID + '" class="primary-text" ><i class="material-icons right">edit</i></a>';
                var deleteBtn = '<a href="javascript:;" class="post-delete danger-text" data-id="' + postID + '" onclick="deletePost()"><i class="material-icons right">delete</i></a>';
                $('#post-details .post-title').html(response.result.post_title + viewHTML + deleteBtn + editHTML);

                if (window.postEditor) {
                    window.postEditor.remove();
                }
                $('#post-content').append('<div id="editor-wrapper"><textarea hidden></textarea></div>');
                $.EDITOR_CONFIG.markdown = response.result.post_content;
                $.EDITOR_CONFIG.tocm = true;
                window.postEditor = editormd.markdownToHTML('editor-wrapper', $.EDITOR_CONFIG);

                $('#post-browsers p').text(response.result.post_browser);
                if (!response.result.post_is_hidden) {
                    $('#post-hidden i').text('visibility');
                    $('#post-hidden p').text('所有人可见');
                } else {
                    $('#post-hidden i').text('visibility_off');
                    $('#post-hidden p').text('仅自己可见');
                }
                $('#post-timestamp p').text(new Date(parseInt(response.result.post_create_timestamp) * 1000).toLocaleString().replace(/:\d{1,2}$/, ' '));
                $('#post-details').fadeIn(500);
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
                classes: 'btn-warning'
            });
        }
    })
}

$(function () {
    window.postEditor = null;
    window.deleteUndo = false;
    $('.post-link').on('click', function () {
        if ($(this).hasClass('selected')) {
            return false;
        }
        var postID = $(this).attr('data-id');
        showPostDetails(postID);
    });
});