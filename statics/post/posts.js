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
                    var viewHTML = '<a href="/post/' + postID + '" target="_blank"><i class="material-icons right">open_in_new</i></a>';
                    var editHTML = '<a href="' + $.URL_CONFIG.post.edit_page_url + '?id=' + postID + '" ><i class="material-icons right">edit</i></a>';
                    $('#post-details .post-title').html(response.result.post_title + viewHTML + editHTML);

                    if (window.postEditor) {
                        console.log(window.postEditor);
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
                    $('#post-timestamp p').text(new Date(parseInt(response.result.post_create_timestamp) * 1000).toLocaleString().replace(/:\d{1,2}$/,' '));
                    $('#post-details').fadeIn(500);
                } else {
                    Materialize.toast(response.message, 1500, 'btn-danger');
                }
            },
        error: function (response) {
            Materialize.toast('未知错误，请与管理员联系', 1500, 'btn-danger');
        }
    })
}

$(function () {
    window.postEditor = null;
    $('.post-link').on('click', function () {
        if ($(this).hasClass('selected')) {
            return false;
        }
        var postID = $(this).attr('data-id');
        showPostDetails(postID);
    })
});