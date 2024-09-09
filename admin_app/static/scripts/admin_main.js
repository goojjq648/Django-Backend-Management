import { BasePage,MainPage,SubPage } from './BasePageType.js';
import { PageManager } from './PageManager.js';


const page_manager = new PageManager();

async function LoadAdminSetting() {
    const getpagedataurl = `/admin_app/get_admin_setting/`;
    const response = await fetch(getpagedataurl);
    const data = await response.json();
    return data;
}

async function init() {
  // 要求設定資料
  const admin_setting = await LoadAdminSetting();

  for (const mainKey in admin_setting) {
    let mainPage = mainKey;
    let sublist = admin_setting[mainKey]['sub_detail'];

    // 註冊主頁面
    if (sublist){
      page_manager.registerPage(new MainPage(mainPage, sublist));
    }
    else
    {
      page_manager.registerPage(new MainPage(mainPage, null));
    }
  }

  // 初始頁面
  page_manager.switchPage('Home');
}

init();

var currentType = null;

// 主類型按鈕切換
document.querySelectorAll('.sidebar .nav-link').forEach(link => {
  link.addEventListener('click', (event)=>{
      event.preventDefault();
      const pageID = link.textContent.trim();
      page_manager.switchPage(pageID);
      currentType = pageID;

      // 移除所有按鈕的 active 類別
      document.querySelectorAll('.sidebar .nav-link').forEach(link => {
        link.classList.remove('active');
      });

      // 設定當前按鈕的 active 類別
      link.classList.add('active');
  });
})


// 子類型按鈕切換
document.querySelectorAll('.offcanvas .nav-link').forEach(link => {
  link.addEventListener('click', (event) => {
      event.preventDefault();
      const pageID = link.getAttribute('data-page');
      page_manager.switchPage(currentType, pageID);
  });
})