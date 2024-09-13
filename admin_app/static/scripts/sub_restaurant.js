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
                // console.log(rowdata);
                
                //直接把資料填入編輯資料的表單
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
    
    // 送出表單
    document.querySelector('#button_restaurant_Submit').addEventListener('click', async(event)=> {
        event.preventDefault();

        const restaurant_form = document.querySelector('#restaurant_form');
        const restaurant_FormData = new FormData(restaurant_form);
        const restaurant_url = `/admin_app/edit_restaurant/`;
        const csrftoken = window.csrf_token;

        const response = await fetch(restaurant_url,{
            method:'POST',
            body:restaurant_FormData,
            headers:{
              'X-CSRFToken': csrftoken
            }
        })

        const restaurant_data = await response.text();
    })
}