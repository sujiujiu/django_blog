
// 'use strict';

// 原
// $(document).ready(function() {
// 	var c_url = window.location.href;
// 	var c_index = 0;
// 	if(c_url.indexOf('add_article') > 0){
// 		c_index = 1;
// 	}else if(c_url.indexOf('settings') > 0){
// 		c_index = -1;
// 	}else{
// 		c_index = 0;
// 	}
// 	var ulTag = $('.menu-ul');
// 	if(c_index >= 0){
// 		ulTag.children().eq(c_index).addClass('active').siblings().removeClass('active');
// 	}else{
// 		ulTag.children().removeClass('active');
// 	}
// });



$(function () {
    $('.nav-sidebar>li>a').click(function (event) {
        var that = $(this);
        if(that.children('a').attr('href') == '#'){
            event.preventDefault();
        }
        if(that.parent().hasClass('unfold')){
            that.parent().removeClass('unfold');
        }else{
            that.parent().addClass('unfold').siblings().removeClass('unfold');
        }
        console.log('coming....');
    });

    $('.nav-sidebar a').mouseleave(function () {
        $(this).css('text-decoration','none');
    });
});



$(function () {
    var url = window.location.href;
    if(url.indexOf('profile') >= 0){
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(0).addClass('active').siblings().removeClass('active');
    } else if(url.indexOf('cms_reset_pwd') >= 0){
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(1).addClass('active').siblings().removeClass('active');
    } else if(url.indexOf('cms_reset_email') >= 0){
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(2).addClass('active').siblings().removeClass('active');
    } else if(url.indexOf('cms_article_list') >= 0){
        var articleManageLi = $('.articles-manage');
        postManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('cms_category_list') >= 0){
        var categoryManageLi = $('.categorys-manage');
        boardManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('cms_tags') >= 0){
        var tagManageLi = $('.tags-manage');
        tagManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('comments') >= 0) {
        var commentsManageLi = $('.comments-manage');
        commentsManageLi.addClass('unfold').siblings().removeClass('unfold');
    }
});