
$(function () {
   $('#captcha-btn').click(function (event) {
       event.preventDefault();

       var email = $('input[name=email]').val();

       myajax.get({
           'url': '/mail_captcha/',
           'data': {
               'email': email
           },
           'success': function (data) {
               if(data['code'] == 200){
                   myalert.alertSuccessToast('恭喜！邮箱发送成功！');
               }else{
                   myalert.alertInfoToast(data['message']);
               }
           }
       })
   });
});

$(function () {
   $('#submit').click(function (event) {
       event.preventDefault();

       var emailInput = $('input[name=email]');
       var captchaInput = $('input[name=captcha]');

       var email = emailInput.val();
       var captcha = captchaInput.val();

       myajax.post({
           'url': '/resetmail/',
           'data':{
               'email': email,
               'captcha': captcha
           },
           'success': function (data) {
               if(data['code'] == 200){
                   emailInput.val('');
                   captchaInput.val('');
                   myalert.alertSuccessToast('恭喜！邮箱修改成功！');
               }else{
                   myalert.alertInfoToast(data['message']);
               }
           }
       })
   });
});
