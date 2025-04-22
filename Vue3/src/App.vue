<template>
    <div v-if="isWait" id="wait">
      <WLoad/>
    </div>
    <div v-else id="start">
      <div id="top">
        <div class="nav-links">
          <RouterLink to="/chat" active-class="active" class="nav-item">
            <svg t="1742367432691" class="icon" viewBox="0 0 1025 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2490" width="24" height="24"><path d="M867.2672 561.792c-81.216-66.496-162.048-133.376-243.072-200.128C586.9472 331.008 549.6992 300.352 512.3872 269.568c-3.264 2.368-6.016 4.288-8.64 6.4C387.2032 372.096 270.5312 468.16 154.2432 564.608 149.9552 568.192 146.9472 575.936 146.8832 581.76c-0.448 97.344-0.384 194.752-0.256 292.096 0 30.208 15.936 45.824 46.464 45.824 74.944 0.064 149.824 0 224.768 0 4.032 0 8.064-0.448 13.184-0.768 0-81.344 0-161.6 0-242.432 54.336 0 107.52 0 161.856 0 0 80.576 0 160.896 0 243.264 6.144 0 10.24 0 14.4 0 74.112 0 148.16 0 222.272 0 32.768 0 47.936-15.232 47.936-48.32 0.064-95.68-0.128-191.36 0.192-286.976C877.7632 574.592 874.8832 568.128 867.2672 561.792z" p-id="2491"></path><path d="M1009.7312 495.808c-38.08-31.68-75.776-63.808-114.56-94.592-13.184-10.432-18.24-21.12-18.048-38.208 1.024-76.608 0.512-153.28 0.448-229.888 0-18.624-5.888-26.176-21.504-26.304-39.808-0.32-79.616-0.32-119.424 0-14.016 0.128-20.8 7.04-21.312 21.312-0.512 12.672-0.192 25.408-0.192 38.08 0 27.008 0 54.016 0 84.032-6.4-5.12-9.984-7.936-13.504-10.88-44.16-36.928-88.32-73.856-132.544-110.784C530.2432 96.256 493.9552 96.192 455.0432 128.576 374.0192 195.968 293.0592 263.488 212.0352 330.944 146.3712 385.664 80.7072 440.448 14.9792 495.168-4.0288 511.04-4.6688 519.04 11.5232 538.24c9.28 11.008 18.432 22.08 27.712 33.088 13.888 16.448 23.04 17.28 39.552 3.456 108.864-90.816 217.728-181.76 326.656-272.576C440.7712 272.704 476.2272 243.2 512.0032 213.376c35.712 29.76 70.848 59.008 105.92 88.256 109.184 91.136 218.432 182.272 327.616 273.408 16.32 13.632 25.408 12.672 39.424-3.968 9.536-11.328 19.008-22.72 28.544-34.048C1028.4192 519.296 1027.6512 510.72 1009.7312 495.808z" p-id="2492"></path></svg>
            <span class="ng_title">主页</span>
          </RouterLink>

          <RouterLink to="/setting" active-class="active" class="nav-item">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path><circle cx="12" cy="12" r="3"></circle></svg>
            <span class="ng_title">设置</span>
          </RouterLink>
        </div>

        <div id="CHbut">
          <div class="avatar-dropdown">
            <div @click="toggleDropdown"  class="avatar-button">
              <div class="avatar-with-status">
                <svg v-if="userStore.isLoggedIn" id="character" t="1742980798240" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="6625" width="32" height="32"><path d="M513.536 628.6336c101.6832 0 280.8832 38.7072 310.8864 193.7408 77.5168-77.5168 124.928-185.9584 124.928-305.0496 0-241.152-194.6624-435.8144-435.8144-435.8144S77.7216 277.0944 77.7216 517.2224c0 119.0912 47.4112 227.6352 124.928 306.0736 30.0032-154.9312 209.2032-194.6624 310.8864-194.6624z m0-439.7056c112.3328 0 204.3904 91.0336 204.3904 204.3904 0 112.3328-91.0336 204.3904-204.3904 204.3904a203.776 203.776 0 0 1-204.3904-204.3904c0.1024-112.4352 92.0576-204.3904 204.3904-204.3904z m0 0" fill="#1296DB" p-id="6626"></path><path d="M515.4816 1006.8992c-65.8432 0-129.8432-12.9024-189.952-38.4-58.1632-24.576-110.2848-59.8016-155.136-104.5504A485.56032 485.56032 0 0 1 65.8432 708.8128c-25.6-60.2112-38.5024-124.1088-38.5024-189.952 0-65.8432 12.9024-129.8432 38.4-189.952 24.576-58.1632 59.8016-110.2848 104.5504-155.136 44.8512-44.8512 96.9728-79.9744 155.136-104.5504C385.6384 43.6224 449.536 30.72 512.0032 30.72c65.8432 0 129.8432 12.9024 189.952 38.4 58.1632 24.576 110.2848 59.8016 155.136 104.5504 44.8512 44.8512 79.9744 96.9728 104.5504 155.136C990.6176 389.0176 1003.52 452.9152 1003.52 518.8608c0 65.8432-12.9024 129.8432-38.4 189.952-24.576 58.1632-59.8016 110.2848-104.5504 155.136a485.56032 485.56032 0 0 1-155.136 104.5504 484.39296 484.39296 0 0 1-189.952 38.4z m0-936.8576c-60.6208 0-119.3984 11.8784-174.6944 35.2256a447.76448 447.76448 0 0 0-142.6432 96.1536A444.42624 444.42624 0 0 0 101.9904 344.064a446.70976 446.70976 0 0 0-35.2256 174.6944c0 60.6208 11.8784 119.3984 35.2256 174.6944 22.6304 53.4528 54.9888 101.4784 96.1536 142.6432 41.1648 41.2672 89.1904 73.6256 142.6432 96.1536 55.296 23.3472 114.0736 35.2256 174.6944 35.2256 60.6208 0 119.3984-11.8784 174.6944-35.2256 53.4528-22.6304 101.4784-54.9888 142.6432-96.1536 41.2672-41.1648 73.6256-89.1904 96.1536-142.6432 23.3472-55.296 35.2256-114.0736 35.2256-174.6944 0-60.6208-11.8784-119.3984-35.2256-174.6944a447.76448 447.76448 0 0 0-96.1536-142.6432 444.42624 444.42624 0 0 0-142.6432-96.1536 447.44704 447.44704 0 0 0-174.6944-35.2256z m0 0" fill="#1296DB" p-id="6627"></path></svg>
                <svg v-else t="1742373012738" id="character" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3776" width="32" height="32"><path d="M512 0a512 512 0 1 0 512 512A512 512 0 0 0 512 0zM213.333 832A298.667 298.667 0 0 1 512 533.333a170.667 170.667 0 1 1 170.667-170.666A170.667 170.667 0 0 1 512 533.333 298.667 298.667 0 0 1 810.667 832z" fill="#8A8A8A" p-id="3777"></path></svg>
                <!-- 状态指示点 -->
                <div v-if="userStore.isLoggedIn && (userStore.userinfo.userauth == 1 || userStore.userinfo.userauth == 2)" class="status-dot admin-dot"></div>
                <div v-else-if="userStore.isLoggedIn" class="status-dot logged-dot"></div>
                <div v-else class="status-dot"></div>
              </div>
            </div>
            <div v-if="isDropdownOpen" class="dropdown-menu">
              <div v-if="userStore.isLoggedIn" class="usermenu">
                <RouterLink to="/userinfo" class="dropdown-item">
                  <svg class="menu-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                  <span>个人</span>
                </RouterLink>
                <hr class="bnbn">
                <RouterLink v-if="userStore.userinfo.userauth == 1 || userStore.userinfo.userauth == 2" to="/admin" class="dropdown-item">
                  <svg class="menu-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="3" y1="9" x2="21" y2="9"></line>
                    <line x1="9" y1="21" x2="9" y2="9"></line>
                  </svg>
                  <span>管理</span>
                </RouterLink>
                <hr v-if="userStore.userinfo.userauth == 1 || userStore.userinfo.userauth == 2" class="bnbn">
                <RouterLink to="/chat" @click="logout" class="dropdown-item">
                  <svg class="menu-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                    <polyline points="16 17 21 12 16 7"></polyline>
                    <line x1="21" y1="12" x2="9" y2="12"></line>
                  </svg>
                  <span>退出</span>
                </RouterLink>
              </div>
              <RouterLink to="/login" v-else @click="login" class="dropdown-item">
                <svg class="menu-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
                  <polyline points="10 17 15 12 10 7"></polyline>
                  <line x1="15" y1="12" x2="3" y2="12"></line>
                </svg>
                <span>登录</span>
              </RouterLink>
            </div>
          </div>
          <CHbut></CHbut>
        </div>
      </div>
    <div class="page_style" :id="contentClass">
      <RouterView/>
    </div>
    </div>
</template>

<script setup lang="ts">
import WLoad from  "./components/waitLoad.vue"
import CHbut from "./components/changebutton.vue"
import {onMounted, ref,computed, onUnmounted} from "vue";
import {RouterLink,RouterView,useRoute,useRouter} from "vue-router";
import "./css/App.css"
import {useUserConfig} from "@/store/dataconfig.ts"
import {useSystemConfig} from "@/store/dataconfig.ts"
import axios from "axios";
const isDropdownOpen = ref(false);
//用户配置
const userStore = useUserConfig()
const systemStore = useSystemConfig()
//路由处理
const route = useRoute();//返回当前路由对象，包含当前路由的信息（如 route.path、route.params 等）
const router = useRouter();//返回路由器实例，包含路由器的方法和属性（如 router.push、router.replace 等）
const contentClass = computed(() =>{
  if (route.path === '/' ||  route.path === '/chat') { 
    return 'chat_style'; // 聊天页面样式
  }
  else if (route.path === '/login') {
    return 'login_style'; // 登录页面样式
  }
  else if (route.path === '/setting') {
    return 'setting_style'; // 设置页面样式
  }
  else if (route.path === '/userinfo') {
    return 'userinfo_style'; // 用户信息页面样式
  }
  return ''; // 默认无额外样式
});

// 应用初始化配置
let isWait = ref(true);
onMounted(async () => {
  try {
    const token = localStorage.getItem('JWTtoken');
    if (token) {
      const response = await axios.get(`${systemStore.baseurl}/admin/config`, {
      });
      systemStore.title = response.data.title;
      systemStore.emailregister = response.data.email_register;
      document.title = systemStore.title;
    }
  } catch (error) {
    console.error('获取网站配置失败:', error);
  }
  // 读取首次访问标记
  const storedValue = localStorage.getItem('frist_');
  
  // 恢复保存的路由
  const lastRoute = sessionStorage.getItem("lastRoute")
  if (lastRoute && window.location.pathname === '/') {
    router.push(lastRoute)
  }
  
  // 添加全局点击事件监听，关闭下拉菜单
  document.addEventListener('click', closeDropdown);
  
  // 首次访问应用时显示加载动画
  if (!Number(storedValue)) {
    setTimeout(() =>{isWait.value = false}, 1000);
    localStorage.setItem('frist_', "1");
  } else {
    isWait.value = false;
  }
});

// 在组件卸载时移除事件监听
onUnmounted(() => {
  document.removeEventListener('click', closeDropdown);
})

// 切换下拉菜单
const toggleDropdown = (event: MouseEvent) =>{
  event.stopPropagation();
  isDropdownOpen.value = !isDropdownOpen.value;
};

// 点击其他地方关闭下拉菜单
const closeDropdown = () =>{
  isDropdownOpen.value = false;
};

// 登录函数
const login = () =>{
  // TODO: 实现登录逻辑
  isDropdownOpen.value = false;
};
// 退出登录
function logout(){
  // 清除用户状态
  userStore.setLoginStatus(false);
  // 移除token
  localStorage.removeItem("JWTtoken");
  // 跳转到登录页
  router.push("/login");
  // 关闭下拉菜单
  isDropdownOpen.value = false;
}
</script>

<style>
/* 初始样式 */
html, body {
  margin: 0;
  padding: 0;
  width: 100vw;
  height: 100vh;
}

:root {
  --background-color: #FAFAFA;
  --text-color: #000;
  --text-ground: #FFFFFF;
  --background-sidebar:#666666;
  --linear-gradient:linear-gradient(45deg, #9f9f9f, #d9d9d9dc);
}

:root[data-theme="dark"] {
  --background-color: #333;
  --text-color: #eee;
  --text-ground: #212121;
  --background-sidebar:#696969;
  --linear-gradient:linear-gradient(135deg, #3a3a3a, #202020);
}

body {
  background-color: var(--background-color);
  color: var(--text-color);
}

/* 页面布局 */
.page_style{
  height: calc(100vh - 3.5rem);
  width: 100vw;
  overflow:hidden;
}
.usermenu{
  display: flex;
  flex-direction: column;
  white-space: nowrap;
}
.ng_title{
  white-space: nowrap; /* 不换行 */
  overflow: hidden; /* 隐藏超出的内容 */
  text-overflow: ellipsis; /* 显示省略号 */
  font-size: 1em;
  margin-bottom: 0px;
  margin-top: 5px;
}
.bnbn{
  margin: 0;
  padding: 0;
  height: 2px;
  border: 0;
  border-top: 3px solid #d0d0FF;
}

.dropdown-item{
  width: 100%;
  padding: 10px 16px;
  color: #333;
  font-size: 14px;
  text-decoration: none;
  display: block;
  text-align: center;
  transition: background 0.2s;
}

.dropdown-item:hover {
  background-color: rgba(18, 150, 219, 0.08);
  color: #1296DB;
}

.bnbn {
  margin: 0;
  padding: 0;
  height: 1px;
  border: 0;
  background-color: #eaeaea;
}

.usermenu {
  width: 60px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  min-width: 100px;
  background-color: #ffffff;
  border-radius: 6px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  z-index: 100;
}

/* 头像状态样式 */
.avatar-with-status {
  position: relative;
  display: inline-block;
}

.status-dot {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #8A8A8A; /* 默认灰色点 */
  border: 2px solid var(--text-ground);
}

.logged-dot {
  background-color: #4CAF50; /* 绿色点表示已登录 */
}

.admin-dot {
  background-color: #0073ff; /* 金色点表示管理员 */
}

/* 增强头像样式 */
.avatar-button {
  cursor: pointer;
  border-radius: 50%;
  padding: 0.2rem;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-button:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.avatar-dropdown {
  position: relative;
}

#character {
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

#wait {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
#start {
  display: flex;
  height: 100vh;
  flex-direction: column;
  
}
#top {
  display: flex;
  align-items: center;
  width: 100vw;
  height: 3.5rem;
  background: var(--text-ground);
  justify-content: space-between;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  user-select: none;
  position: sticky;
  top: 0;
  z-index: 100; /* 确保顶部栏显示在其他内容之上 */
}
#CHbut{
  display: flex;
  align-items: center;
  height: 100%;
  gap: 0.6rem;
  margin-right: 1rem;
  margin-top: 0.1rem;
}

#login_style {
  display: flex;
  flex:1;
  justify-content: center;
  align-items: center;
  overflow:hidden;
}
#chat_style {
  display: flex;
  width: 100vw;
  overflow:hidden;
}
#setting_style {
   display: flex;
  overflow:hidden;
}
#userinfo_style {
  display: flex;
  justify-content: center;
  overflow:hidden;
}

/* 输入框强制白色 - 最高优先级 */
:root .ant-design-x-sender,
:root .ant-design-x-vue-sender {
  background: #ffffff !important;
  background-color: #ffffff !important;
  color: #333333 !important;
}

:root .ant-design-x-sender *,
:root .ant-design-x-vue-sender * {
  background-color: #ffffff !important;
}

:root .ant-design-x-sender-textarea,
:root .ant-design-x-vue-sender-textarea {
  background: #ffffff !important;
  color: #333333 !important;
}

/* 下拉菜单样式 */
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: var(--text-ground);
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  z-index: 100;
  animation: fadeIn 0.2s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.dropdown-item {
  padding: 10px 23px;
  color: var(--text-color);
  font-size: 14px;
  text-decoration: none;
  display: flex;
  align-items: center;
  transition: all 0.2s;
}

.dropdown-item:hover {
  background-color: rgba(18, 150, 219, 0.05);
  color: #1296DB;
}

.dropdown-item .menu-icon {
  margin-right: 8px;
  color: #666;
}

.dropdown-item:hover .menu-icon {
  color: #1296DB;
}

.bnbn {
  margin: 0;
  padding: 0;
  height: 1px;
  border: 0;
  background-color: #f0f0f0;
}

.usermenu {
  width: 100%;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
