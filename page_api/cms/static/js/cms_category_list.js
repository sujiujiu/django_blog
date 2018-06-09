
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
                    'url': '/add_board/',
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
        var board_id = $(this).attr('data-category-id');

        myalert.alertOneInput({
            'text': '请输入板块名称',
            'placeholder': '板块名称',
            'confirmCallback': function (inputValue) {
                // 把数据发送到后台
                myajax.post({
                    'url': '/edit_board/',
                    'data': {
                        'name': inputValue,
                        'board_id': board_id
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
        var board_id = $(this).attr('data-category-id');

        myalert.alertConfirm({
            'msg': '您确定要删除本板块吗？',
            'confirmCallback': function () {
                // 把数据发送到后台
                myajax.post({
                    'url': '/delete_board/',
                    'data': {
                        'board_id': board_id
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


