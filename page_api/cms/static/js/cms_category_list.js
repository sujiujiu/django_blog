
// 添加板块的按钮的执行事件
$(function () {
    $('#add-category-btn').click(function (event) {
        event.preventDefault();
        myalert.alertOneInput({
            'text': '请输入板块名称',
            'placeholder': '板块名称',
            'confirmCallback': function (inputValue) {
                // 发送ajax请求给后台
                myajax.post({
                    'url': '/cms_add_category/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            myalert.alertSuccessToast('恭喜！板块添加成功！');
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

// 编辑板块按钮的执行事件
$(function () {
    $('.edit-category-btn').click(function (event) {
        event.preventDefault();
        var category_id = $(this).attr('data-category-id');

        myalert.alertOneInput({
            'text': '请输入板块名称',
            'placeholder': '板块名称',
            'confirmCallback': function (inputValue) {
                // 把数据发送到后台
                myajax.post({
                    'url': '/cms_edit_category/',
                    'data': {
                        'name': inputValue,
                        'category_id': category_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            myalert.alertSuccessToast('恭喜！板块修改成功！');
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

// 删除板块按钮的执行事件
$(function () {
    $('.delete-category-btn').click(function (event) {
        event.preventDefault();
        var category_id = $(this).attr('data-category-id');

        myalert.alertConfirm({
            'msg': '您确定要删除本板块吗？',
            'confirmCallback': function () {
                // 把数据发送到后台
                myajax.post({
                    'url': '/cms_remove_category/',
                    'data': {
                        'category_id': category_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            myalert.alertSuccessToast('恭喜！板块删除成功！');
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


