function bindSubSettingEvents() {
    DataTableModule.init('#restaurant_table', {
        columnDefs: [
            { width: '5%', targets: 0 },   // 第一列 (編號)
            { width: '15%', targets: 1 },  // 第二列 (餐廳名稱)
            { width: '5%', targets: 2 },   // 第三列 (評分)
            { width: '10%', targets: 3 },   // 第四列 (評論數)
            { width: '20%', targets: 4 },  // 第五列 (地址)
            { width: '10%', targets: 5 },  // 第六列 (平均消費)
            { width: '15%', targets: 6 },  // 第七列 (營業時間)
            { width: '5%', targets: 7 },   // 第八列 (緯度)
            { width: '5%', targets: 8 },   // 第九列 (經度)
            { width: '10%', targets: 9 },  // 第十列 (圖片網址)
            { width: '15%', targets: 10 }  // 第十一列 (選項)
        ]       
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

                document.querySelector('#InputRestaurantID').value = rowdata[0];
                document.querySelector('#InputRestaurantName').value = rowdata[1];
                document.querySelector('#InputRestaurantRating').value = rowdata[2];
                document.querySelector('#InputRestaurantReviewCount').value = rowdata[3];  
                document.querySelector('#InputRestaurantAddress').value = rowdata[4]; 
                document.querySelector('#InputRestaurantAverageSpending').value = rowdata[5];
                document.querySelector('#InputRestaurantBusinessHours').value = rowdata[6];
                document.querySelector('#InputRestaurantLatitude').value = rowdata[7];
                document.querySelector('#InputRestaurantLongitude').value = rowdata[8];
                document.querySelector('#InputRestaurantImageUrl').value = rowdata[9];

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
                // console.log('模態框已關閉，頁面正在刷新');
            }, 
            function() {
                // console.log('');
            },
            responseType = 'text')
            .then(response => {
                console.log('表單提交成功，返回資料:');

                window.pagemanager.refreshPage();
                alert('餐廳資料已經更新完成！');
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

}

function InitRestaurantForm(action) {
    if (action == "create") {
        document.querySelector('#Div_InputRestaurantID').classList.add('d-none');
    }
    else if (action == "edit") {
        document.querySelector('#Div_InputRestaurantID').classList.remove('d-none');
    }

    // 設定表單動作
    document.querySelector('#restaurant_action').value = action;
    // 清空表單
    document.querySelector('#InputRestaurantID').value = "";
    document.querySelector('#InputRestaurantName').value = "";
    document.querySelector('#InputRestaurantRating').value = "";
    document.querySelector('#InputRestaurantReviewCount').value = ""; 
    document.querySelector('#InputRestaurantAddress').value = "";
    document.querySelector('#InputRestaurantAverageSpending').value = "";
    document.querySelector('#InputRestaurantBusinessHours').value = "";
    document.querySelector('#InputRestaurantLatitude').value = "";
    document.querySelector('#InputRestaurantLongitude').value = "";
    document.querySelector('#InputRestaurantImageUrl').value = "";

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

        let value = inputField.value;
        let url = `/admin_app/check_restaurantdata/?${name}=${value}`;

        try{
            let response = await utilsModule.fetchData(url,{ method: 'GET' }, 'json');

            if(response.status == 200){
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
        return false;
    } else {
        alertMessage.classList.add('d-none');
        return true;
    }
}