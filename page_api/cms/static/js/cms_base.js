
'use strict';

$(document).ready(function() {
	var c_url = window.location.href;
	var c_index = 0;
	if(c_url.indexOf('add_article') > 0){
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