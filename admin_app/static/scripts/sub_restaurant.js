function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function bindSubSettingEvents() {
    // 表格的初始化及設置
    $(document).ready(function() {
        $('#restaurant_table').DataTable({
            dom: 'Blfrtip',
            autoWidth: false,  // 禁用自動寬度調整
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
            ],
            language: {
                url: 'https://cdn.datatables.net/plug-ins/2.1.5/i18n/zh-HANT.json',
            },
            // 預設每頁顯示 5 筆資料
            pageLength : 5,
            // 使用者可以選擇每頁顯示 5、10、25、50 或 100 筆
            lengthMenu : [[5, 10, 25, 50, 100], [5, 10, 25, 50, 100]],
            buttons: [
                'copy', 'csv', 'excel'
            ]
            
        });
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
        const csrftoken = getCookie('csrftoken');

        const response = await fetch(restaurant_url,{
            method:'POST',
            body:restaurant_FormData,
            headers:{
              'X-CSRFToken': csrftoken
            }
        })

        const restaurant_data = await response.text();
        console.log(restaurant_data);
    })
}