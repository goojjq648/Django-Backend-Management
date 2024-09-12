import { BasePage,MainPage,SubPage } from './BasePageType.js';

// PageManager 負責管理所有頁面物件
export class PageManager {
    constructor() {
      this.pages = {};
      this.currentPage = null;
    }
  
    // 註冊頁面物件
    registerPage(page) {
      this.pages[page.pageID] = page;
      console.log(`頁面 ${page.pageID} 已註冊`);
    }
  
    // 切換並載入頁面
    async switchPage(pageID, subPageID = null) {  
      //檢查這個頁面是否有子類型
      if (this.pages[pageID] instanceof MainPage && 
          this.pages[pageID].sub_page_list !== null &&
          subPageID === null) {
            return
      }
      
      if (this.currentPage) {
        this.currentPage.hidePage();
      }
      
      //切換頁面
      this.currentPage = this.pages[pageID];
      
      if (subPageID !== null) {
        await this.currentPage.loadSubPage(subPageID);
      }
      else {
        await this.currentPage.loadPage();
      }
    }

    async refreshPage() {
      let current_activePage = this.currentPage.getActivePage()
      if (current_activePage !== null) {
        await current_activePage.loadPage();
      }
    }
}