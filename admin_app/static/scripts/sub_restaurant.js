function bindSubSettingEvents() {
    const ColumnDefs = Object.freeze({
        ID: 0,          
        NAME: 1,  
        HASH: 2,      
        RATING: 3,      
        REVIEWS: 4,     
        ADDRESS: 5,     
        PHONE: 6,       
        AVG_SPEND: 7,   
        BUSSINESS_HOURS: 8,       
        SERVICES: 9,    
        LATITUDE: 10,    
        LONGITUDE: 11,  
        IMG_URL: 12,    
        GOOGLE_URL: 13, 
        OPTIONS: 14  
    });

    // 表格設定
    DataTableModule.init('#restaurant_table', {
        columnDefs: [
            { width: '50px', targets: ColumnDefs.ID },           // 第一列 (編號)
            { width: '200px', targets: ColumnDefs.NAME },        // 第二列 (餐廳名稱)
            { width: '250px', targets: ColumnDefs.HASH },        // 第三列 (HASH)
            { width: '50px', targets: ColumnDefs.RATING },       // 第四列 (評分)
            { width: '50px', targets: ColumnDefs.REVIEWS },      // 第五列 (評論數)
            { width: '150px', targets: ColumnDefs.ADDRESS },     // 第六列 (地址)
            { width: '100px', targets: ColumnDefs.PHONE },       // 第七列 (電話)
            { width: '50px', targets: ColumnDefs.AVG_SPEND },    // 第八列 (平均消費)
            { width: '150px', targets: ColumnDefs.BUSSINESS_HOURS },  // 第九列 (營業時間)
            { width: '150px', targets: ColumnDefs.SERVICES },    // 第十列 (提供服務)
            { width: '50px', targets: ColumnDefs.LATITUDE },     // 第十一列 (緯度)
            { width: '50px', targets: ColumnDefs.LONGITUDE },    // 第十二列 (經度)
            { width: '100px', targets: ColumnDefs.IMG_URL },     // 第十三列 (圖片網址)
            { width: '80px', targets: ColumnDefs.GOOGLE_URL },   // 第十四列 (google網址)
            { width: '50px', targets: ColumnDefs.OPTIONS }       // 第十五列 (選項)
        ],
        createdRow: function(row, data, dataIndex) {
            // 針對需要自動換行的欄位設置樣式
            $('td', row).eq(ColumnDefs.NAME).css('white-space', 'normal');
            $('td', row).eq(ColumnDefs.ADDRESS).css('white-space', 'normal');
            $('td', row).eq(ColumnDefs.HASH).css('white-space', 'normal');
            $('td', row).eq(ColumnDefs.BUSSINESS_HOURS).css('white-space', 'normal');
        }
    });

    // 針對表頭進行樣式調整
    $('#restaurant_table thead th').css({
        'white-space': 'nowrap',    // 避免標題自動換行
        'text-align': 'center',     // 讓標題文字居中
        'vertical-align': 'middle'  // 垂直居中，讓文字更整齊
    });

    // 驗證表單
    // 驗證-餐廳名稱
    checkrestaurantFormField('#InputRestaurantName', 'restaurant_name', validateRestaurantName);
    // 驗證-評分
    checkrestaurantFormField('#InputRestaurantRating', 'restaurant_rating', validateRestauranRating);
    // 驗證-營業時間
    checkrestaurantFormField('#InputRestaurantBusinessHours', 'restaurant_business_hours', validateRestaurantBusinessHours);
    // 驗證-緯度
    checkrestaurantFormField('#InputRestaurantLatitude', 'restaurant_latitude', validateRestaurantLatitude);
    // 驗證-經度
    checkrestaurantFormField('#InputRestaurantLongitude', 'restaurant_longitude', validateRestaurantLongitude);
    
    //按下修改
    document.querySelectorAll('.edit-btn').forEach(button =>{
        button.addEventListener('click', function(event) {
            // 拿到點到哪筆資料的修改按鈕
            let btn_restaurant_id = button.id;
            let restaurant_data_id = btn_restaurant_id.split('_')[2];
            
            //取得表格中的那筆資料
            let row = document.querySelector(`tr[data-id="${restaurant_data_id}"]`);
            
            //取得表格中的資料
            if(row){
                const cells = row.querySelectorAll('td');
                const rowdata = Array.from(cells).map(cell => cell.innerText);
                console.log(rowdata);
                
                //直接把資料填入編輯資料的表單
                InitRestaurantForm("edit");

                document.querySelector('#InputRestaurantID').value = rowdata[ColumnDefs.ID];
                document.querySelector('#InputRestaurantName').value = rowdata[ColumnDefs.NAME];
                document.querySelector('#InputRestaurantHash').value = rowdata[ColumnDefs.HASH];
                document.querySelector('#InputRestaurantRating').value = rowdata[ColumnDefs.RATING];
                document.querySelector('#InputRestaurantReviewCount').value = rowdata[ColumnDefs.REVIEWS];  
                document.querySelector('#InputRestaurantAddress').value = rowdata[ColumnDefs.ADDRESS];
                document.querySelector('#InputRestaurantPhone').value = rowdata[ColumnDefs.PHONE]; 
                document.querySelector('#InputRestaurantAverageSpending').value = rowdata[ColumnDefs.AVG_SPEND];
                document.querySelector('#InputRestaurantBusinessHours').value = rowdata[ColumnDefs.BUSSINESS_HOURS];
                document.querySelector('#InputRestaurantServices').value = rowdata[ColumnDefs.SERVICES];
                document.querySelector('#InputRestaurantLatitude').value = rowdata[ColumnDefs.LATITUDE];
                document.querySelector('#InputRestaurantLongitude').value = rowdata[ColumnDefs.LONGITUDE];

                const imgUrl = row.querySelector('td[data-url]').getAttribute('data-url');
                const googleUrl = row.querySelector('td[data-url] a').getAttribute('href');

                document.querySelector('#InputRestaurantImageUrl').value = imgUrl;
                document.querySelector('#InputRestaurantGoogleUrl').value = googleUrl;

            }
        })
    });
    
    // 送出餐廳資料的表單
    document.querySelector('#button_restaurant_Submit').addEventListener('click', async(event)=> {
        event.preventDefault();

        const restaurant_FormData = new FormData(restaurant_form);
        const restaurant_url = `/admin_app/edit_restaurant/`;
        const csrftoken = window.csrf_token;

        const options = {
            method:'POST',
            body:restaurant_FormData,
            headers:{
              'X-CSRFToken': csrftoken
            }
        }

        try{
            utilsModule.submitFormAndCloseModal('#restaurant_form', 'formModal', restaurant_url, 
            function() {
            }, 
            function() {
            },
            responseType = 'json', true, false)
            .then(response => {
                console.log('表單提交成功，返回資料:');
                
                if (response.data.action === 1) 
                {
                    alert('餐廳資料已經更新完成！');
                    utilsModule.closeModal('formModal', window.pagemanager.refreshPage());
                }
                else
                {
                    utilsModule.showAlert('div_alert_restaurant_info', 'error', response.data.message);
                }

            })
            .catch(error => {
                console.error('表單提交失敗，錯誤:', error);
            });
        }
        catch(error){
            console.error('Fetch error:', error);
        }

    })

    // 增加餐廳資料
    document.querySelector('#restaurant_add').addEventListener('click', async(event)=> {
        // event.preventDefault();
            // 初始化表單
            InitRestaurantForm("create");

    });

    // 刪除餐廳資料
    document.querySelectorAll('.del-btn').forEach(button =>{
        button.addEventListener('click', function(event) {
            // 拿到點到哪筆資料的刪除按鈕   
            let del_btn_restaurant_id = button.id;
            let del_restaurant_data_id = del_btn_restaurant_id.split('_')[2];

            const csrftoken = window.csrf_token;
    
            const options = {
                method:'POST',
                headers:{
                  'Content-Type': 'application/json',
                  'X-CSRFToken': csrftoken
                },
                body:JSON.stringify({
                    'restaurant_id': del_restaurant_data_id
                })
            }

            utilsModule.fetchWithLoading('/admin_app/del_restaurant/',  
                    options, 
                    'json')
                .then(response => {
                    if (response.data.action === 1)
                    {
                        alert('餐廳資料已經刪除完成！');
                        window.pagemanager.refreshPage();
                    }
                    else
                    {
                        alert(response.data.message);
                    }
                    
                })            
        });
    });


}

function InitRestaurantForm(action) {
    if (action == "create") {
        document.querySelector('#Div_InputRestaurantID').classList.add('d-none');
        document.querySelector('#InputRestaurantHash').value = "自動生成";
    }
    else if (action == "edit") {
        document.querySelector('#Div_InputRestaurantID').classList.remove('d-none');
        document.querySelector('#InputRestaurantHash').value = "";
    }

    // 設定表單動作
    document.querySelector('#restaurant_action').value = action;
    // 清空表單
    document.querySelector('#InputRestaurantID').value = "";
    document.querySelector('#InputRestaurantName').value = "";
    document.querySelector('#InputRestaurantRating').value = "";
    document.querySelector('#InputRestaurantReviewCount').value = ""; 
    document.querySelector('#InputRestaurantAddress').value = "";
    document.querySelector('#InputRestaurantPhone').value = "";
    document.querySelector('#InputRestaurantAverageSpending').value = "";
    document.querySelector('#InputRestaurantBusinessHours').value = "";
    document.querySelector('#InputRestaurantServices').value = "";
    document.querySelector('#InputRestaurantLatitude').value = "";
    document.querySelector('#InputRestaurantLongitude').value = "";
    document.querySelector('#InputRestaurantImageUrl').value = "";
    document.querySelector('#InputRestaurantGoogleUrl').value = "";

    // 隱藏警告訊息
    document.querySelector('#alert_restaurant_name').classList.add('d-none');
    document.querySelector('#alert_restaurant_rating').classList.add('d-none');
    document.querySelector('#alert_restaurant_business_hours').classList.add('d-none');
    document.querySelector('#alert_restaurant_latitude').classList.add('d-none');
    document.querySelector('#alert_restaurant_longitude').classList.add('d-none');
}

async function checkrestaurantFormField(id, name, validateFunction) {
    let inputField = document.querySelector(id);
    let alert_restaurant_name = document.querySelector(`#alert_${name}`);

    inputField.addEventListener('blur', async(event)=> {

        const isValid = validateFunction();

        if (!validateFunction()) {
            return;
        }

        let action = document.querySelector('#restaurant_action').value;

        let value = inputField.value;
        let url = `/admin_app/check_restaurantdata/?${name}=${value}&act=${action}`;

        try{
            let response = await utilsModule.fetchData(url,{ method: 'GET' }, 'json');

            if(response.status == 200){
                alert_restaurant_name.innerHTML = response.data.message;
                alert_restaurant_name.classList.remove('d-none');
                console.log('Valid data:', response.data);
            }
        }
        catch(error){
            console.error('Fetch error:', error);
        }

    });
}

function validateRestaurantName() {
        let name = document.querySelector('#InputRestaurantName');
        let alert_restaurant_name = document.querySelector('#alert_restaurant_name');
        
        if (name.value === '') {
            alert_restaurant_name.classList.remove('d-none');
            alert_restaurant_name.innerHTML = '請輸入餐廳名稱';
            return false;
        }
        else {
            alert_restaurant_name.classList.add('d-none');
            return true;
        }
}

function validateRestauranRating() {
    const rating = document.querySelector('#InputRestaurantRating');
    const alertMessage = document.querySelector('#alert_restaurant_rating');
    const value = parseFloat(rating.value);
    
    if (isNaN(value) || value <= 0 || value > 5) {
        alertMessage.classList.remove('d-none');
        alertMessage.innerHTML = '請輸入 1 到 5 之間的整數';
        return false;
    } else {
        alertMessage.classList.add('d-none');
        return true;
    }
}

function validateRestaurantBusinessHours() {
    const hours = document.querySelector('#InputRestaurantBusinessHours');
    const alertMessage = document.querySelector('#alert_restaurant_business_hours');
    if (hours.value === '') {
        alertMessage.classList.add('d-none');
        return true;
    }
    
    if (!utilsModule.isValidJSON(hours.value))
    {
        alertMessage.classList.remove('d-none');
        alertMessage.innerHTML = '請輸入正確的 JSON 格式';
        return false;
    }
    else
    {
        alertMessage.classList.add('d-none');
        return true;    
    }
}

function validateRestaurantLatitude() {
    const latitude = document.querySelector('#InputRestaurantLatitude');
    const alertMessage = document.querySelector('#alert_restaurant_latitude');
    const value = parseFloat(latitude.value);
    
    if (isNaN(value) || value < -90 || value > 90) {
        alertMessage.classList.remove('d-none');
        alertMessage.innerHTML = '請輸入 -90 到 90 之間的數字';
        return false;
    } else {
        alertMessage.classList.add('d-none');
        return true;
    }
}

function validateRestaurantLongitude() {
    const longitude = document.querySelector('#InputRestaurantLongitude');
    const alertMessage = document.querySelector('#alert_restaurant_longitude');
    const value = parseFloat(longitude.value);
    
    if (isNaN(value) || value < -180 || value > 180) {
        alertMessage.classList.remove('d-none');
        alertMessage.innerHTML = '請輸入 -180 到 180 之間的數字';
        return false;
    } else {
        alertMessage.classList.add('d-none');
        return true;
    }
}