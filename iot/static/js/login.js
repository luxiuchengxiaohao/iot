// var ajax1;
// var is_loading = false;
// function get_html(url){
//     ajax1 = $.ajax(url, {
//         dataType: 'json',
//         type: 'get',
//         error: function (xhr, type, errorThrown) {
//             setTimeout(function(){
//                 is_loading = false;
//                 get_html(url);
//             },1000);
//         },
//         success: function (result, status, xhr) {
//             is_loading = false;
//             return result
//         }
//     });
//
// }
// var regist_html = get_html('http://127.0.0.1:8000/regist/');
// $('#regist').html(regist_html);
// var change_password_html = get_html('http://127.0.0.1:8000/change_pw/');
// $('#change_password').html(change_password_html);