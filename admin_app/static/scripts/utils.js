var utilsModule = (function() {
/**
 * 執行一個帶有 loading 圖示的異步 fetch 請求。
 * 在請求開始時顯示 loading，完成或發生錯誤時隱藏 loading 圖示。
 * 
 * @param {string} url - 要發送請求的 URL。
 * @param {Object} [options={}] - 可選的 fetch 請求選項，如 method、headers 和 body。
 * @param {string} [responseType='text'] - 指定返回的資料類型，'json' 解析為 JSON，'text' 解析為文字。
 * @returns {Promise<{data: string|Object, status: number}>} - 返回一個包含解析後的資料和 HTTP 狀態碼的 Promise。
 * @throws {Error} - 當發生錯誤時拋出異常。
 * 
 * @example
 * fetchWithLoading('/api/data', { method: 'POST', body: JSON.stringify(data) }, 'json')
 *     .then(response => {
 *         console.log(response.data);
 *     })
 *     .catch(error => {
 *         console.error('Error:', error);
 *     });
 */
    async function fetchWithLoading(url, options = {}, responseType = 'text') {
        const loading = document.getElementById('loading-overlay');
        loading.style.display = 'block'; // 顯示 loading 狀態

        try {
            const response = await fetch(url, options);

            let data;
            if (responseType === 'json') {
                data = await response.json();  // 如果指定為 JSON，則解析為 JSON
            } else {
                data = await response.text();  // 預設解析為文字
            }

            loading.style.display = 'none'; // 請求完成後隱藏 loading 狀態

            return { data, status: response.status }; // 返回資料和狀態

        } catch (error) {
            loading.style.display = 'none'; // 請求失敗後也隱藏 loading
            console.error('Fetch error:', error);
            throw error; // 可以根據需要處理錯誤
        }
    }
/**
 * 發送異步請求並根據請求類型解析回應。
 *
 * @param {string} url - 要發送請求的目標 URL。
 * @param {Object} [options={}] - 請求的選項配置（如 method, headers, body 等）。
 * @param {string} [responseType='text'] - 回應的類型，'json' 或 'text'，預設為 'text'。
 * @returns {Promise<{data: any, status: number}>} - 返回包含資料和 HTTP 狀態碼的 Promise。
 * @throws {Error} - 當請求失敗時，會拋出異常。
 * 
 * @example
 * fetchData('/api/data', { method: 'GET' }, 'json')
 *    .then(response => console.log(response.data))
 *    .catch(error => console.error('Error:', error));
 */
    async function fetchData(url, options = {}, responseType = 'text') {
        try {
            const response = await fetch(url, options);

            let data;
            if (responseType === 'json') {
                data = await response.json();  // 如果指定為 JSON，則解析為 JSON
            } else {
                data = await response.text();  // 預設解析為文字
            }

            return { data, status: response.status }; // 返回資料和狀態

        } catch (error) {
            console.error('Fetch error:', error);
            throw error; // 可以根據需要處理錯誤
        }
    }

/**
 * 提交表單並在成功後關閉模態框，支持自定義回應類型並返回資料。
 *
 * @param {string} formSelector - 表單的 CSS 選擇器，用於選取要提交的表單。
 * @param {string} modalId - 模態框的 ID，將在提交成功後關閉此模態框。
 * @param {string} url - 表單提交的目標 URL。
 * @param {function} [successCallback] - 在模態框完全關閉後執行的回調函數，可選。
 * @param {function} [failedCallback] - 在getData失敗後執行的回調函數，可選。
 * @param {string} [responseType='json'] - 回應的類型，'json' 或 'text'，預設為 'json'。
 * @returns {Promise<{data: any, status: number}>} - 返回包含資料和 HTTP 狀態碼的 Promise。
 * 
 * @example
 * submitFormAndCloseModal('#admin_member_form', 'admin_member_formModal', '/admin_app/create_admin_member/', function() {
 *     window.pagemanager.refreshPage();
 * }, 'json');
 */
    async function submitFormAndCloseModal(formSelector, modalId, url, successCallback, failedCallback, responseType = 'json') {
        try {
            let form = document.querySelector(formSelector);
            let formData = new FormData(form);
            
            let response = await fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': window.csrf_token
                }
            });

            let data;
            if (responseType === 'json') {
                data = await response.json();  // 如果指定為 JSON，則解析為 JSON
            } else {
                data = await response.text();  // 預設解析為文字
            }

            if (response.status) {
                // 獲取並關閉 Modal
                let modalElement = document.getElementById(modalId);
                let modalInstance = bootstrap.Modal.getInstance(modalElement);
                modalInstance.hide();
                
                // 完全關閉後執行頁面刷新或其他操作
                modalElement.addEventListener('hidden.bs.modal', function () {
                    if (typeof successCallback === 'function') {
                        successCallback();
                    }
                });
            } else {
                // 處理失敗情況
                if (typeof failedCallback === 'function') {
                    failedCallback();
                }
            }

            // 返回資料和狀態
            return { data, status: response.status };

        } catch (error) {
            console.error('Error:', error);
            throw error;  // 拋出異常
        }
    }


    return {
        fetchWithLoading: fetchWithLoading,
        fetchData: fetchData,
        submitFormAndCloseModal: submitFormAndCloseModal
    };
})();