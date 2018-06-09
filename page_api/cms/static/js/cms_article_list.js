

'use strict';
// 删除文章的执行函数
$(function() {
	$('.delete-article-btn').click(function(event) {
		// 阻止a标签的默认行为
		event.preventDefault();
		var result = confirm('您确定要删除这篇文章吗?');
		if(result){
			var article_id = $(this).attr('data-article-id');
			// var trTag = $(this).parent().parent();
			// var article_id = trTag.attr('data-article-id');
			myajax.post({
				'url': '/cms_delete_article/',
				'data': {
					'article_id': article_id
				},
				'success':function(result) {
					if(result['code'] == 200){
						myalert.alertSuccessToast(msg);
	                    setTimeout(function () {
	                        window.location.reload();
	                    },500);
						// trTag.hide(1000,function() {
						// 	trTag.remove();
						// });
					}else{
						myalert.alertInfoToast(result['message']);
					}
				},
				'error':function(error) {
					// alert(error);
					myalert.alertInfoToast(error);
				}
			});
		}else{
			//nothing
		}
	});
});

//置顶文章的执行函数
$(function () {
    $('.top-article-btn').click(function (event) {
        event.preventDefault();
        var article_id = $(this).attr('data-article-id');
        var is_top = parseInt($(this).attr('data-is-top'));
        myajax.post({
            'url': '/cms_top_article/',
            'data': {
                'article_id': article_id,
                'is_top': !is_top
            },
            'success': function (data) {
                if(data['code'] == 200){
                    var msg = '';
                    if(is_top){
                        msg = '取消加精成功！';
                    }else{
                        msg = '加精成功！';
                    }
                    myalert.alertSuccessToast(msg);
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }else{
                    myalert.alertInfoToast(data['message']);
                }
            },
            'error':function(error) {
				alert(error);
			}
        })
    });
});


// 排序的事件
$(function () {
    $('#sort-select').change(function (event) {
       var value = $(this).val();
       var newHref = myparam.setParam(window.location.href,'sort',value);
       window.location = newHref;
   });
});

// 分类选择的事件
$(function() {
	$('#category-select').change(function() {
		// var categoryId = $(this).val();
		// window.location = '/cms/article_manage/1/' + categoryId + '/';
		var value = $(this).val();
		var newHref = myparam.setParam(window.location.href,'category',value);
        var newHref = myparam.setParam(newHref,'page',1);
        window.location = newHref;
	});
});