
// 添加标签的按钮的执行事件
$(function () {
    $('#add-tag-btn').click(function (event) {
        event.preventDefault();
        myalert.alertOneInput({
            'text': '请输入标签名称',
            'placeholder': '标签名称',
            'confirmCallback': function (inputValue) {
                // 发送ajax请求给后台
                myajax.post({
                    'url': '/cms_add_tag/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            myalert.alertSuccessToast('恭喜！标签添加成功！');
                            setTimeout(function () {
                                window.location.reload();
                            },500);
                        }else{
                            myalert.alertInfoToast(data['message']);
                        }
                    }
                });
            }
        });
    });
});

// 编辑标签按钮的执行事件
$(function () {
    $('.edit-tag-btn').click(function (event) {
        event.preventDefault();
        var tag_id = $(this).attr('data-tag-id');

        myalert.alertOneInput({
            'text': '请输入标签名称',
            'placeholder': '标签名称',
            'confirmCallback': function (inputValue) {
                // 把数据发送到后台
                myajax.post({
                    'url': '/edit_tag/',
                    'data': {
                        'name': inputValue,
                        'tag_id': tag_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            myalert.alertSuccessToast('恭喜！标签修改成功！');
                            setTimeout(function () {
                                window.location.reload();
                            },500);
                        }else{
                            myalert.alertInfoToast(data['message']);
                        }
                    }
                });
            }
        })
    });
});

// 删除标签按钮的执行事件
$(function () {
    $('.delete-tag-btn').click(function (event) {
        event.preventDefault();
        var tag_id = $(this).attr('data-tag-id');

        myalert.alertConfirm({
            'msg': '您确定要删除本标签吗？',
            'confirmCallback': function () {
                // 把数据发送到后台
                xtajax.post({
                    'url': '/delete_tag/',
                    'data': {
                        'tag_id': tag_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            myalert.alertSuccessToast('恭喜！标签删除成功！');
                            setTimeout(function () {
                                window.location.reload();
                            },500);
                        }else{
                            myalert.alertInfoToast(data['message']);
                        }
                    }
                });
            }
        });
    });
});


