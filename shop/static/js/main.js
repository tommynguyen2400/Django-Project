$(document).ready(function(){
    $('.table-form input,textarea,select').each(function(){
        $(this).addClass('form-control');
    });

    $('.table-form input[type=file]').each(function(){
        $(this).removeClass('form-control');
        $(this).addClass('form-control-file');
    });
});