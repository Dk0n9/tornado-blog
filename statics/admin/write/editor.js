window.converter = new showdown.Converter();

function compile(){
    let text = $('#editor').val();
    $('#preview').html(window.converter.makeHtml(text));
}
