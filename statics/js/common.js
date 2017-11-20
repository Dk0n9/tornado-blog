$(function () {
    $('.button-collapse').sideNav();  // 初始化导航栏
    $('nav li a.waves-effect').each(function () {
        if (location.pathname == $(this).attr('href')) {
            $(this).parent().addClass('active');
            return true;
        }
    });
    $.URL_CONFIG = {
        post: {}
    };
    $.EDITOR_CONFIG = {
        width: '100%',
        placeholder: 'Enjoy writting...',
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
        codeFold : true,
        delay: 1000,  // 当数据量过大是开启延迟显示
        flowChart: true,  // 开启流程图功能
        sequenceDiagram: true,  // 开启序列图功能
        emoji: false,  // 关闭 emoji功能
        path: '/statics/editor/lib/'
    };
});