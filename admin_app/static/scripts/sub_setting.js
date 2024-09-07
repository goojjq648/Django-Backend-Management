let subcategoryIndex = 0;
function bindSubSettingEvents() {
    // 選擇主類別
    const adminSelect = document.getElementById('admin_select');
    adminSelect.addEventListener('change', async (event)=> {
    if (event.target && event.target.id === 'admin_select') {
        // 處理選擇主類別的邏輯
            console.log(adminSelect.value);
            let url = `/admin_app/selectType/?mainType=${adminSelect.value}`;
            let response = await fetch(url);
            let data = await response.text();

            document.getElementById('sub_setting').innerHTML = data;
        }
    });


    // 處理動態新增子類別
    document.getElementById('add-subcategory').addEventListener('click', function(event) {
        if (event.target && event.target.id === 'add-subcategory') {
            // 處理動態新增子類別的邏輯
            console.log("按鈕被點擊");
        }
        const container = document.getElementById('subcategory-container');

        const subcategoryID = document.querySelector('#InputSubTypeID').value;
        const subcategoryName = document.querySelector('#InputSubTypeName').value;

        const newSubcategory = document.createElement('div');
        newSubcategory.setAttribute('class', 'subcategory-item');
        newSubcategory.setAttribute('id', `subcategory-${subcategoryIndex}`);
        
        newSubcategory.innerHTML = `
        <div class="row mt-2">
            <div class="col">
            <input type="text" name="subcategories[${subcategoryIndex}][id]" class="form-control" placeholder="子類別ID" value="${subcategoryID}" readonly>
            </div>
            <div class="col">
            <input type="text" name="subcategories[${subcategoryIndex}][name]" class="form-control" placeholder="子類別名稱" value="${subcategoryName}" readonly>
            </div>
            <div class="col-auto">
            <button type="button" class="btn btn-danger" onclick="removeSubcategory(${subcategoryIndex})">刪除</button>
            </div>
        </div>
        `;
        
        container.appendChild(newSubcategory);
        subcategoryIndex++;
    });
}

function removeSubcategory(index) {
    const subcategory = document.getElementById(`subcategory-${index}`);
    subcategory.remove();
}