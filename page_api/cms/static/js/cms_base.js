
'use strict';
$(document).ready(function() {
	//1. 获取当前的URL
	var c_url = window.location.href;
	//2. 判断当前的URL是哪个,然后具体再给指定的li添加active类
	var c_index = 0;
	if(c_url.indexOf('addarticle') > 0){
		c_index = 1;
	}else if(c_url.indexOf('settings') > 0){
		c_index = -1;
	}else{
		c_index = 0;
	}
	var ulTag = $('.menu-ul');
	if(c_index >= 0){
		ulTag.children().eq(c_index).addClass('active').siblings().removeClass('active');
	}else{
		ulTag.children().removeClass('active');
	}
});