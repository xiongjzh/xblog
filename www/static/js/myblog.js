// function showError(err) {
//     var alertbox = $('div.uk-alertbox-danger');
//     if (err) {
//         alertbox.text(err.message || err.error || err).removeClass('uk-hidden').show();
//         try {
//             if (alertbox.offset().top < ($(window).scrollTop() - 41)) {
//                 $('html,body').animate({scrollTop: alertbox.offset().top - 41});
//             }
//         }
//         catch (e) {}
//     }
//     else {
//         alertbox.addClass('uk-hidden').hide().text('');
//     }
// }
function s(t){
    console.log(t);
} 
function hide_alertbox(){
    var alertbox = $('div.uk-alert');
    alertbox.addClass('uk-hidden').hide().text('');
} 
function showError(err,type="",duration=0){
    var alertbox = $('div.uk-alert');
    alertbox.removeClass('uk-alert-danger').removeClass('uk-alert-warning').removeClass('uk-alert-success');
    if(type)
        alertbox.addClass('uk-alert-'+type);
    if(err){
        alertbox.text(err.message || err.error || err).removeClass('uk-hidden').show(300);
        if(duration){
            t=setTimeout("hide_alertbox()",duration);  
        }
    }else{
        alertbox.addClass('uk-hidden').hide().text('');
    }
}

function postApi(url,data='',success_fn=function(){},err_fn=function(){}){
    return 
    $.ajax({
        cache: false,
        type: "POST",
        url:url,
        data:data,
        async: false,
        error: err_fn,
        success: success_fn
    });
}
function _ajax(method, url, data, callback) {
    $.ajax({
        type: method,
        url: url,
        data: data,
        dataType: 'json'
    }).done(function(r) {
        if (r && r.error) {
            return callback && callback(r);
        }
        return callback && callback(null, r);
    }).fail(function(jqXHR, textStatus) {
        return callback && callback({error: 'HTTP ' + jqXHR.status, message: 'Network error (HTTP ' + jqXHR.status + ')'});
    });
}

function getApi(url, data, callback) {
    if (arguments.length === 2) {
        callback = data;
        data = {};
    }
    _ajax('GET', url, data, callback);
}

function postApi(url, data, callback) {
    if (arguments.length === 2) {
        callback = data;
        data = {};
    }
    _ajax('POST', url, data, callback);
}