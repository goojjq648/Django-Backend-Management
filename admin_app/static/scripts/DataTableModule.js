var DataTableModule = (function() {
    // 私有變數或函數
    
    //初始化 DataTable
    function initTable(tableId, options) {
        if ($.fn.DataTable.isDataTable(tableId)) {
            $(tableId).DataTable().destroy();  // 如果表格已經存在，先銷毀
        }

        // 默認的設置，可以被傳入的 options 覆蓋
        var defaultOptions = {
            dom: 'Blfrtip',
            autoWidth: false,
            scrollX: true,     // 啟用水平捲動
            fixedColumns: true,  // 固定列寬
            columnDefs: [
            ],
            language: {
                url: 'https://cdn.datatables.net/plug-ins/2.1.5/i18n/zh-HANT.json',
            },
            pageLength: 5,
            lengthMenu: [[5, 10, 25, 50, 100], [5, 10, 25, 50, 100]],
            buttons: ['copy', 'csv', 'excel']
        };

        // 使用 $.extend 合併自定義選項和默認選項
        var settings = $.extend(true, {}, defaultOptions, options);

        // 初始化 DataTable
        $(document).ready(function() {
            $(tableId).DataTable(settings);
        });
    }

    // 返回公開的方法
    return {
        init: initTable
    };
})();