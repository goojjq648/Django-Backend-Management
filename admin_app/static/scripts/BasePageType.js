// 基本頁面
export class BasePage {
    constructor(pageID) {
        this.pageID = pageID;
        this.active = false;
    }

    // 可以覆寫的方法
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
        console.log(`hhhh頁面 ${this.pageID} 隱藏中...`);
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

    // loadSubPage
    async loadSubPage(subPageID) {
      if (this.sub_page_list) {
        await this.sub_page_list[subPageID].loadPage();
        
        // 隱藏 Offcanvas
        this.hideOffCanvas();
      }
    }

    hidePage() {
      console.log(`頁面 ${this.pageID} 隱藏中...`);
      super.hidePage();

      if (this.sub_page_list) {
        for (const subKey in this.sub_page_list) {
          if (this.sub_page_list[subKey].active === true)
          {
            this.sub_page_list[subKey].hidePage();
          }
        }
      }
    }

    hideOffCanvas() {
      if (this.sub_page_list) {
        console.log(`${this.pageID} 隱藏 Offcanvas`);
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
    }
  
    // 重寫頁面載入邏輯，並動態載入對應的 JS
    async loadPage() {
      console.log(`子頁面 ${this.pageID} 載入中...`);
      await super.loadPage();

      this.loadScript(`/static/scripts/${this.pageID}.js`, function() {
        bindSubSettingEvents();
      });
      // this.loadScript();
    }
  
    // 動態載入 JS 檔案
    // loadScript() {
    //   const scriptUrl = `/static/scripts/${this.pageID}.js`;
    //   const script = document.createElement('script');

    //   script.type = 'text/javascript';
    //   script.src = `${scriptUrl}?v=${new Date().getTime()}`;
    //   document.head.appendChild(script);
    //   console.log(`${this.pageID} 腳本已載入`);
    //   bindSubSettingEvents();
    // }

    loadScript(url, callback) {
      let script = document.createElement('script');
      script.type = 'text/javascript';
      
      // 當腳本載入完成時，執行回調函數
      script.onload = function() {
          if (callback) {
              callback();
          }
      };
      
      script.src = url + '?v=' + new Date().getTime();
      document.head.appendChild(script);
    }
}