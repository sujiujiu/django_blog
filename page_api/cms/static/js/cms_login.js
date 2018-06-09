
// 'use strict';

// $(function() {
// 	$('.captcha-img').click(function() {
// 		//ajax擅长处理纯文本和json对象
// 		//对于流媒体不擅长,比较消耗资源
// 		//只要img的src改变了,就会重新加载图片
// 		var old_src = $(this).attr('src');
// 		var src = old_src + '?xx=' + Math.random();
// 		$(this).attr('src',src);
// 	});
// });

$(function () {
    $('#login_submit').click(function (event) {
        event.preventDefault();

        var email = $('input[name=email]').val();
        var password = $('input[name=password]').val();

        myajax.post({
            'url':'/cms_login/',
            'data':{
                'email': email,
                'password': password
            },
            'success': function (data) {
                var code = data['code'];
                if(code == 200){
                    // 跳转到首页
                    window.location = '/';
                }else{
                    var message = data['message'];
                    // alert(message);
                    var errorTag = $('.error-info');
                    errorTag.text(message);
                }
            }
        })
    });
});