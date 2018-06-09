// 移除评论
$(function () {
    $('.remove-btn').click(function (event) {
        event.preventDefault();

        var comment_id = $(this).attr('data-comment-id')
        myalert.alertConfirm({
            'msg': '你确定要移除这条评论吗？',
            'confirmCallback': function () {
                // 发送ajax
                myajax.post({
                    'url': '/cms_remove_comment/',
                    'data': {
                        'id': comment_id
                    },
                    'success': function (data) {
                        if(data['code'] != 200){
                            myalert.alertInfoToast(data['message']);
                        }else{
                            myalert.alertSuccessToast('移除成功！');
                            setTimeout(function () {
                                window.location.reload();
                            },1000);
                        }
                    }
                });
            }
        });
    });
});