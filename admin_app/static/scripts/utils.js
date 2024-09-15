var utilsModule = (function() {
/**
 * 驗證一個欄位是否包含有效的 JSON 格式。
 *
 * @param {string} inputValue - 欄位的值（字符串）。
 * @returns {boolean} - 如果是有效的 JSON 格式則返回 true，否則返回 false。
 */
function isValidJSON(inputValue) {
    try {
        JSON.parse(inputValue); 
        return true;  // 如果解析成功，則返回 true
    } catch (e) {
        return false;  // 如果解析失敗，則返回 false
    }
}

/**
 * 關閉模態框。
 *
 * @param {string} modalID - 模態框的 ID。
 * @param {function} [closeCallback] - 模態框關閉時要執行的回呼函數。
 */
function closeModal(modalID, closeCallback) {
    let modalElement = document.getElementById(modalID);
    let modalInstance = bootstrap.Modal.getInstance(modalElement);
    modalInstance.hide();

    modalElement.addEventListener('hidden.bs.modal', function () {
        if (typeof closeCallback === 'function') {
            closeCallback();
        }
    }); 
}

/**
 * 顯示alert。
 *
 * @param {string} id - alert 的 ID。
 * @param {string} status - alert 的狀態，可以是 'success', 'error', 或 'warning'。
 * @param {string} message - alert 的訊息。
 */

function showAlert(id, status, message) {
    const resultContainer = document.querySelector(`#${id}`);
    if (!resultContainer) {
        console.error(`未找到 ID 為 ${id} 的元素`);
        return;
    }
    
    const result = document.createElement('div');
    // 定義不同狀態對應的樣式和圖標
    let alertClass, icon, display;

    switch (status) {
        case 'success':
            alertClass = 'alert-success';
            icon = '<svg class="bi flex-shrink-0 me-2" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>';
            display = '成功';
            break;
        case 'error':
            alertClass = 'alert-danger';
            icon = '<svg class="bi flex-shrink-0 me-2" role="img" aria-label="Error:"><use xlink:href="#exclamation-triangle-fill"/></svg>';
            display = '失敗';
            break;
        case 'warning':
            alertClass = 'alert-warning';
            icon = '<svg class="bi flex-shrink-0 me-2" role="img" aria-label="Warning:"><use xlink:href="#exclamation-fill"/></svg>';
            display = '警告';
            break;
        default:
            alertClass = 'alert-info';
            icon = '<svg class="bi flex-shrink-0 me-2" role="img" aria-label="Info:"><use xlink:href="#info-fill"/></svg>';
            display = '信息';
    }

    // 更新警報內容
    result.className = `alert ${alertClass} d-flex align-items-center`;
    result.innerHTML = `${icon}<strong>${display}:</strong> ${message}`;

    // 將生成的警報添加到指定的容器中
    resultContainer.innerHTML = ''; // 清空之前的內容
    resultContainer.appendChild(result);
    
    // 顯示警報框
    resultContainer.classList.remove('d-none');
    
    // 自動隱藏警報框（可選）
    setTimeout(() => {
        resultContainer.classList.add('d-none');
    }, 5000); // 5 秒後隱藏
}


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
 * @param {boolean} [showLoading=true] - 是否顯示 loading 畫面，預設為 true。
 * @param {boolean} [iscloseModal=true] - 是否關閉模態框，預設為 true。
 * @returns {Promise<{data: any, status: number}>} - 返回包含資料和 HTTP 狀態碼的 Promise。
 * 
 * @example
 * submitFormAndCloseModal('#admin_member_form', 'admin_member_formModal', '/admin_app/create_admin_member/', function() {
 *     window.pagemanager.refreshPage();
 * }, null, 'json', true, true);
 */
    async function submitFormAndCloseModal(formSelector, modalId, url, successCallback, failedCallback, responseType = 'json', showLoading = true, iscloseModal = true) {
        // 顯示 loading 狀態
        const loading = document.getElementById('loading-overlay');
        try {
            let form = document.querySelector(formSelector);
            let formData = new FormData(form);

            if (showLoading && loading) {
                loading.style.display = 'block';
            }
            
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

            if (showLoading && loading) {
                loading.style.display = 'none';  // 請求完成後隱藏 loading
            }

            if (response.status) {
                // 獲取並關閉 Modal
                if (iscloseModal) {      
                    console.log(`關閉 ${modalId} 模態框`);              
                    closeModal(modalId, successCallback);
                }
            } else {
                // 處理失敗情況
                if (typeof failedCallback === 'function') {
                    failedCallback();
                }
            }

            // 返回資料和狀態
            return { data, status: response.status };

        } catch (error) {
            if (showLoading && loading) {
                loading.style.display = 'none';  // 請求失敗後隱藏 loading
            }

            console.error('Error:', error);
            throw error;  // 拋出異常
        }
    }


    return {
        isValidJSON: isValidJSON,               // 驗證是否為 JSON
        fetchWithLoading: fetchWithLoading,     // 顯示 loading 畫面並執行 fetch
        fetchData: fetchData,                   // 執行 fetch
        submitFormAndCloseModal: submitFormAndCloseModal,    // 提交表單並關閉模態框
        closeModal: closeModal,
        showAlert: showAlert
    };
})();