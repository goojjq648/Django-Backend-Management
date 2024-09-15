// 基本頁面
export class BasePage {
    constructor(pageID) {
        this.pageID = pageID;
        this.active = false;
    }

    async loadPage() {
        const data = await this.fetchPageData();
        this.displayPage(data);
    }

    async fetchPageData() {
        const getpagedataurl = `/admin_app/getpagedata/?page_id=${this.pageID}`;
        const response = await fetch(getpagedataurl);
        const data = await response.text();
        document.getElementById(this.pageID).innerHTML = data;
        return data;
    }

    displayPage(data){
      const pageElement = document.getElementById(this.pageID);
        
      if (pageElement) {
        pageElement.innerHTML = data;
        pageElement.classList.add('active');
        this.active = true;
      }
    }

    hidePage() {
      if (this.active) {
        const pageElement = document.getElementById(this.pageID);
        if (pageElement) {
          pageElement.classList.remove('active');
          this.active = false;
        }
      }
    }
}

export class MainPage extends BasePage {
    constructor(pageID, SubPageList) {
      super(pageID);
      this.sub_page_list = null;

      // 設定子頁面
      if (SubPageList) {
        this.sub_page_list = {};
        for (const subKey in SubPageList) {
          this.sub_page_list[subKey] = new SubPage(subKey);
        }
      }
    }

    getActivePage() {
      // 如果有子頁面
      if (this.sub_page_list) { 
        for (const subKey in this.sub_page_list) {
          if (this.sub_page_list[subKey].active === true) {
            return this.sub_page_list[subKey];
          }
        }
      }

      // 如果沒有子頁面
      if (this.active === true) {
        return this;
      }
      else{
        return null;
      }
    } 

    // loadSubPage
    async loadSubPage(subPageID) {
      if (this.sub_page_list) {
        await this.sub_page_list[subPageID].loadPage();
        
        // 隱藏 Offcanvas
        this.hideOffCanvas();
      }
    }

    hidePage() {
      super.hidePage();

      if (this.sub_page_list) {
        for (const subKey in this.sub_page_list) {
          if (this.sub_page_list[subKey].active === true)
          {
            this.sub_page_list[subKey].hidePage();
            this.sub_page_list[subKey].unbindScript()
          }
        }
      }
    }

    hideOffCanvas() {
      if (this.sub_page_list) {
        let offcanvasElement = document.getElementById(this.pageID);
        let offcanvasInstance = bootstrap.Offcanvas.getInstance(offcanvasElement);
        offcanvasInstance.hide();
      }
    }
  
    bindEvents() {
      console.log(`主頁面 ${this.pageID} 的事件綁定`);
    }
}

  // 定義 SubPage 類別繼承自 BasePage，處理子類型邏輯
export class SubPage extends BasePage {
    constructor(pageID) {
      super(pageID);
      this.bindScript = null;
    }
  
    // 重寫頁面載入邏輯，並動態載入對應的 JS
    async loadPage() {
      await super.loadPage();
      console.log(`子頁面 ${this.pageID} 載入Script中...`);
      const _self = this;
      
      (function() {
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
        
        console.log("腳本載入中...");
        _self.checkAndLoadScript(_self.pageID, getCookie('csrftoken'), function() {
          _self.loadScript(`/static/scripts/${_self.pageID}.js`, function() {
            bindSubSettingEvents();
            window.csrf_token = getCookie('csrftoken');
            // console.log(`csrf_token ${window.csrf_token}`);  
          });
        });
      })();

    }

    checkAndLoadScript(page_id, csrftoken, callback) {
      let data = {
        'page_id': page_id,
      };

      fetch(`/admin_app/loadscript/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data) // 將資料轉換為 JSON 格式
      })
      .then(response => {
        if (response.status === 200) {
          callback();
          console.log('腳本載入成功');
        }
        else {
          console.log(`${page_id} Script load failed with status:`, response.status);
        }
      })
      .catch(error => {
        console.error(error);
      });
    }

    loadScript(url, callback) {
      if (this.bindScript) {
        console.log(`腳本 ${url} 已經被載入過了，不再載入...`);
        this.unbindScript(url);
      }

      let script = document.createElement('script');
      script.type = 'text/javascript';
      // script.type = 'module';
      
      // 當腳本載入完成時，執行回調函數
      script.onload = function() {
          if (callback) {
              callback();
          }
      };
      
      script.src = url + '?v=' + new Date().getTime();
      // script.src = url;
      this.bindScript = script;
      document.body.appendChild(script);
    }

    unbindScript(url) {
      if (this.bindScript === null) {
        return;
      }

      let existingScript = Array.from(document.querySelectorAll('script'))
      .find(script => {
        let scriptSrc = new URL(script.src, window.location.href).pathname;
        return this.bindScript.src === script.src; // 比較相對路徑是否相同
      });
      
      if (existingScript) {
        console.log('腳本已經載入，直接返回');
        existingScript.parentNode.removeChild(existingScript);
        this.bindScript = null;
      }
    }
}