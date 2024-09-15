function bindSubSettingEvents() {
    //按下新增後台會員
    document.querySelector('#admin_member_add').addEventListener('click', function() {
        // 初始化表單
        Init_CreateMember_form();
    });

    //按下確認新增
    document.querySelector('#button_create_user').addEventListener('click', async(event)=> {
            event.preventDefault();
            let url = '/admin_app/create_admin_member/';

            let result_container = document.querySelector('#div_alert_create_user')  
            let result = document.querySelector('#alert_create_user')  

            try{
                utilsModule.submitFormAndCloseModal('#admin_member_form', 'admin_member_formModal', url, 
                function() {
                    // console.log('模態框已關閉，頁面正在刷新');
                }, 
                function() {
                    // console.log('失敗');
                },
                responseType = 'json',true, false)
                .then(response => {
                    // console.log('表單提交成功，返回資料:');
                    if (response.data.action === true) 
                    {
                        alert(response.data.message);
                        utilsModule.closeModal('admin_member_formModal', window.pagemanager.refreshPage());
                    }
                    else{
                        // result_container.className = "alert alert-danger d-flex align-items-center"; // 失敗變成紅色
                        // result.innerHTML = response.data.message;
                        utilsModule.showAlert('div_alert_create_user_info', 'error', response.data.message);
                    }
                })
                .catch(error => {
                    console.error('表單提交失敗，錯誤:', error);
                });
            }
            catch(error){
                console.error('Fetch error:', error);
            }           

        });
}

function Init_CreateMember_form(){
    // 初始化表單
    document.querySelector('#InputAdmin_memberName').value = '';
    document.querySelector('#InputAdmin_memberEmail').value = '';
    document.querySelector('#InputAdminPassword').value = '';
    document.querySelector('#InputAdminPassword_confirm').value = '';
}

function Edit_CreateMember_form(){
    let name = document.querySelector('#InputAdmin_memberName');
    let email = document.querySelector('#InputAdmin_memberEmail');
    let password = document.querySelector('#InputAdminPassword');
    let confirm_password = document.querySelector('#InputAdminPassword_confirm');
}