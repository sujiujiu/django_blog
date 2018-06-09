
//获取cookie的方法

'use strict';

// 初始化七牛的事件
$(function() {
	// 初始化七牛的代码必须放在选择图片行为之前
	myqiniu.setUp({
		'browse_button': 'avatar-img',
		'success':function(up,file,info) {
			var avatar = $('#avatar-img'); 
			// var avatar = domain + file.name; //设置图片的完成URL路径
			// 把图片的URL设置进img标签
			$('#avatar-img').attr('src',avatar)
		},
		'error':function(up,err,errTip) {
			console.log(err);
		}
	});
});

// 提交按钮执行事件
$('.submit-btn').click(function(event) {
	event.preventDefault();
	var username = $('.username-input').val();
	var avatar = null;
	// 说明有图片上传了
	if(uploader.files.length > 0){
		// src属性代表的就是上传的头像URL
		avatar = $('#avatar-img').attr('src');
	}
	var data = {'username':username};
	if(avatar){
		data['avatar'] = avatar;
	}
	$.ajax({
		'url': '/cms_settings/',
		'method': 'post',
		'data':data,
		'success': function(data) {
			if(data['code'] == 200){
				var alert = $('.alert-success');
				alert.html('更新成功');
				alert.show();
			}
		},
		'error': function(error) {
			console.log(error);
		},
		'beforeSend':function(xhr,settings) {
			var csrftoken = getCookie('csrftoken');
			//2.在header当中设置csrf_token的值
			xhr.setRequestHeader('X-CSRFToken',csrftoken);
		}
	});
	myajax.post({
		'url': '/cms_profile/',
		'data':data,
		'success': function(data) {
			if(data['code'] == 200){
				var alert = $('.alert-success');
				alert.html('更新成功');
				alert.show();
			}
		},
		'error': function(error) {
			console.log(error);
		},
	});
});

