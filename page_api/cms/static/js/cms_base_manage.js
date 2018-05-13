
'use strict';

$(function() {
	var url = window.location.href;
	var ulTag = $('#sub-nav');
	var index = 0;
	if(url.indexOf('category_manage') > 0){
		index = 1;
	}else{
		index = 0;
	}
	ulTag.children().eq(index).addClass('active').siblings().removeClass('active');
});