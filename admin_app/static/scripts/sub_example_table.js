function bindSubSettingEvents() {
    // 填上指定的table id
    DataTableModule.init('#examples_table_id', {
        // 每格的寬度設定
        columnDefs: [
            { width: '5%', targets: 0 },    // 範例1
            { width: '5%', targets: 1 },    // 範例2
            { width: '15%', targets: 2 },   // 範例3
        ],
        // 設定每頁最大顯示筆數
        pageLength: 5,
        // 設定顯示幾筆選項 (EX 5 10 25 50 100)
        lengthMenu: [[5, 10, 25, 50, 1000], [5, 10, 25, 50, 1000]],       
    });
}