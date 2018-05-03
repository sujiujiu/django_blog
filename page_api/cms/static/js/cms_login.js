/*
* @Author: xiaotuo
* @Date:   2016-10-31 21:54:48
* @Last Modified by:   xiaotuo
* @Last Modified time: 2016-10-31 22:10:10
*/

'use strict';

$(function() {
	$('.captcha-img').click(function() {
		var old_src = $(this).attr('src');
		var src = old_src + '?xx=' + Math.random();
		$(this).attr('src',src);
	});
});