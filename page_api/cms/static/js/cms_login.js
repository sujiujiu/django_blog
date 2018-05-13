
'use strict';

$(function() {
	$('.captcha-img').click(function() {
		//ajax擅长处理纯文本和json对象
		//对于流媒体不擅长,比较消耗资源
		//只要img的src改变了,就会重新加载图片
		var old_src = $(this).attr('src');
		var src = old_src + '?xx=' + Math.random();
		$(this).attr('src',src);
	});
});