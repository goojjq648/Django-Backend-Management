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
            let add_member_form_data = new FormData(document.querySelector('#admin_member_form'));
            let response = await fetch(url, {
                method: 'POST',
                body: add_member_form_data,
                headers: {
                    'X-CSRFToken': window.csrf_token
                }
            });

            let data = await response.json();
            let result_container = document.querySelector('#div_alert_create_user')  
            let result = document.querySelector('#alert_create_user')  

            if (data.status) {
                alert(data.message);
                let myModal = document.getElementById('admin_member_formModal');
                let modal = bootstrap.Modal.getInstance(myModal);

                modal.hide();

                myModalElement.addEventListener('hidden.bs.modal', function () {
                    // 在 Modal 完全關閉後執行頁面刷新
                    window.pagemanager.refreshPage();
                });
            } 
            else {
                result_container.className = "alert alert-danger d-flex align-items-center"; // 失敗變成紅色
                result.innerHTML = data.message;
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