let subcategoryIndex = 0;
function bindSubSettingEvents() {
    // 選擇主類別
    const adminSelect = document.getElementById('admin_select');
    adminSelect.addEventListener('change', async (event)=> {
    
        if (event.target && event.target.id === 'admin_select') {
            // 處理選擇主類別的邏輯
            // console.log(adminSelect.value);
            let url = `/admin_app/selectType/?mainType=${adminSelect.value}`;
            let response = await fetch(url);
            let data = await response.json();

            // 打開表單
            var form = document.getElementById("settingForm");
            
            if (form.classList.contains("d-none")) {
                form.classList.remove("d-none");
            }

            // 處理icon下拉列表取得列表資料
            let icon_sourcedata = document.getElementById('admin_iconlist');
            let icon_elements = document.querySelectorAll(`Symbol[data-admin_icon]`);
            let iconDropdown = document.getElementById('admin_setting_iconDropdown');
            iconDropdown.innerHTML = ``;
            
            icon_elements.forEach(element => {
                let iconID = element.id;
            
                let icon_list = document.createElement('li');
                icon_list.innerHTML =
                 `
                    <a class="dropdown-item" href="#" onclick="selectIcon('#${iconID}')">
                        <svg class="bi" width="24" height="24" fill="currentColor">
                            <use xlink:href="#${iconID}"></use>
                        </svg>
                            ${iconID}
                    </a>
                `;  

                iconDropdown.appendChild(icon_list);
            })


            //處理表單狀態
            if (data && Object.keys(data).length > 0) {
                document.getElementById('admin_setting_action').value = adminSelect.value;
                document.getElementById('InputMainTypeName').value = adminSelect.value;
                
                removeIcon();
                removeAllSubcategory();

                if (data === null || data === undefined) {
                    console.log("取得資料為空");
                    return;
                }
                else if (data.length === 0) {
                    console.log("取得資料為空物件，目前沒設定子類別");
                    return;
                }
                else
                {
                    // 處理類別的ICON
                    if (data['button_icon'])
                    {
                        selectIcon(data['button_icon']);
                    }
                    
                    // 處理子類別
                    subcategoryIndex = 0;
                    for (let key in data['sub_detail']) {
                        //console.log(`${key}: ${data['sub_detail'][key]}`);
                        addSubcategory(key, data['sub_detail'][key], subcategoryIndex);
                        subcategoryIndex++;
                    }

                }
            }
            else{
                
                document.getElementById('admin_setting_action').value = adminSelect.value;

                removeIcon();
                removeAllSubcategory();

                console.log("取得資料失敗");
            }
        }
    });


    // 處理動態新增子類別
    document.getElementById('add-subcategory').addEventListener('click', function(event) {
        if (event.target && event.target.id === 'add-subcategory') {
            // 處理動態新增子類別的邏輯
            console.log("按鈕被點擊");
        }

        const subcategoryID = document.querySelector('#InputSubTypeID').value;
        const subcategoryName = document.querySelector('#InputSubTypeName').value;
        
        addSubcategory(subcategoryID, subcategoryName, subcategoryIndex);
        subcategoryIndex++;
    });

    //按下確認按鈕
    document.getElementById('confirm_edit_setting').addEventListener('click', async(event)=> {
        event.preventDefault();
        let confirm_editsetting_url = `/admin_app/confirm_editSetting/`;
        let editsetting_form = document.querySelector('#settingForm');
        let editsetting_FormData = new FormData(editsetting_form);
        const csrftoken = window.csrf_token;

        let confirm_editsetting_response = await fetch(confirm_editsetting_url,{
            method:'POST',
            body:editsetting_FormData,
            headers:{
              'X-CSRFToken': csrftoken
            }
        });

        let confirm_editsetting_data = await confirm_editsetting_response.text();
        let result = document.querySelector('#div_edit_setting_result')
        
        if (confirm_editsetting_data.success) {
            result.className = "alert alert-success mt-3"; // 成功變成綠色
          } 
          else {
            result.className = "alert alert-danger mt-3"; // 失敗變成紅色
          }
      
          result.innerHTML = confirm_editsetting_data;
    });
}


function addSubcategory(sub_ID, sub_name, idx) {
    const container = document.getElementById('subcategory-container');
    const newSubcategory = document.createElement('div');

    newSubcategory.setAttribute('class', 'subcategory-item');
    newSubcategory.setAttribute('id', `subcategory-${idx}`);
    
    newSubcategory.innerHTML = `
    <div class="row mt-2">
        <div class="col">
        <input type="text" name="subcategories[${idx}][id]" class="form-control" placeholder="子類別ID" value="${sub_ID}" readonly>
        </div>
        <div class="col">
        <input type="text" name="subcategories[${idx}][name]" class="form-control" placeholder="子類別名稱" value="${sub_name}" readonly>
        </div>
        <div class="col-auto">
        <button type="button" class="btn btn-danger" onclick="removeSubcategory(${idx})">刪除</button>
        </div>
    </div>
    `;
    
    container.appendChild(newSubcategory);

    // 設定子類別索引
    document.getElementById('subcategory_Idx').value = idx;
}

// 移除子類別
function removeSubcategory(index) {
    const subcategory = document.getElementById(`subcategory-${index}`);
    subcategory.remove();
}

// 移除所有子類別
function removeAllSubcategory() {
    const subcategoryContainer = document.getElementById('subcategory-container');
    while (subcategoryContainer.firstChild) {
        subcategoryContainer.removeChild(subcategoryContainer.firstChild);
    }
}

function selectIcon(iconId) {
    const iconContainer = document.getElementById('selected_MainType_Icon');
    iconContainer.innerHTML = `<svg class="bi" width="48" height="48" fill="currentColor"><use xlink:href="${iconId}"></use></svg>`;

    document.getElementById('selected_main_Icon').value = iconId;
}

function removeIcon() {
    const iconContainer = document.getElementById('selected_MainType_Icon');
    iconContainer.innerHTML = ``;
}