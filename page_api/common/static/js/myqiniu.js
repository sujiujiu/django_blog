
'use strict';

var myqiniu = {
	'setUp': function(args) {
		var domain = 'http://ono11bq0h.bkt.clouddn.com/';
		var params = {
			// browse_button:args['browse_btn'],
			runtimes: 'html5,flash,html4', //上传模式，依次退化
			max_file_size: '500mb', //文件最大允许的尺寸
			dragdrop: false, //是否开启拖拽上传
			chunk_size: '4mb', //分块上传时，每片的大小
			uptoken_url: '/cms/get_token/', //ajax请求token的url
			domain: domain, //图片下载时候的域名
			get_new_uptoken: false, //是否每次上传文件都要从业务服务器获取token
			auto_start: true, //如果设置了true,只要选择了图片,就会自动上传
			log_level: 5, //log级别
			init: {
				'FileUploaded': function(up,file,info) {
					if(args['success']){
						var success = args['success'];
						file.name = domain + file.name;
						success(up,file,info);
					}
				},
				'Error': function(up,err,errTip) {
					if(args['error']){
						var error = args['error'];
						error(up,err,errTip);
					}
				},
				// 'UploadProgress': function (up,file) {
    //                 if(args['progress']){
    //                     args['progress'](up,file);
    //                 }
    //             },
    //             'FilesAdded': function (up,files) {
    //                 if(args['fileadded']){
    //                     args['fileadded'](up,files);
    //                 }
    //             },
    //             'UploadComplete': function () {
    //                 if(args['complete']){
    //                     args['complete']();
    //                 }
    //             }
			},
		};

		// 把args中的参数放到params中去
		for(var key in args){
			params[key] = args[key];
		}
		var uploader = Qiniu.uploader(params);
		return uploader;
	}
};