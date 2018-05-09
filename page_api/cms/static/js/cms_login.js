
'use strict';

$(function() {
	$('.captcha-img').click(function() {
		var old_src = $(this).attr('src');
		var src = old_src + '?xx=' + Math.random();
		$(this).attr('src',src);
	});
});