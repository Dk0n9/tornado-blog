function showArticleDetails(articleID) {
    $.ajax({
        url: $.URL_CONFIG.article.info_api_url,
        type: 'post',
        data: {
            'article_id': articleID,
            '_xsrf': $('input[name=_xsrf]').val()
        },
        success: function (response) {
                if (response.status) {
                    $('.selected').removeClass('selected');
                    $('.article-link[data-id="' + articleID + '"]').addClass('selected');
                    var viewHTML = '<a href="/p?id=' + articleID + '" ><i class="material-icons right">open_in_new</i></a>';
                    var editHTML = '<a href="' + $.URL_CONFIG.article.edit_page_url + '?id=' + articleID + '" ><i class="material-icons right">edit</i></a>';
                    $('#article-details .article-title').html(response.result.article_title + viewHTML + editHTML);

                    if (window.articleEditor) {
                        window.articleEditor.editor.remove();
                    }
                    $('#article-content').append('<div id="editor-wrapper"><textarea style="display: none;"></textarea></div>');
                    window.articleEditor = editormd('editor-wrapper', {
                        width: '100%',
                        height: '400px',
                        markdown: response.result.article_content,
                        path: '/statics/editor/lib/',
                        watch : false,
                        delay: 1000,
                        onload : function() {
                            this.previewing();
                        }
                    });

                    $('#article-browsers p').text(response.result.article_browser);
                    if (!response.result.article_is_hidden) {
                        $('#article-hidden i').text('visibility');
                        $('#article-hidden p').text('所有人可见');
                    } else {
                        $('#article-hidden i').text('visibility_off');
                        $('#article-hidden p').text('仅自己可见');
                    }
                    $('#article-timestamp p').text(new Date(parseInt(response.result.article_create_timestamp) * 1000).toLocaleString().replace(/:\d{1,2}$/,' '));
                    $('#article-details').fadeIn(500);
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
    window.articleEditor = null;
    $('.article-link').on('click', function () {
        if ($(this).hasClass('selected')) {
            return false;
        }
        var articleID = $(this).attr('data-id');
        showArticleDetails(articleID);
    })
});