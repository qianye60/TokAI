<template>
    <div class="admin-container">        
        <div class="admin-sidebar">
            <div class="admin-title">管理中心</div>
            <div class="admin-item-box" 
                :class="{ active: $route.path.includes('/admin/user') }"
                @click="navigateTo('/admin/user')">
                <svg class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="22" height="22"><path d="M763.2 827.21c-8-92.7-47.18-178.62-110.31-241.92-34.58-34.68-74.77-60.94-118.15-77.81a178.42 178.42 0 0 0 72.59-143.63c0-98.46-80.1-178.57-178.57-178.57s-178.57 80.1-178.57 178.57a178.29 178.29 0 0 0 65.72 138.28c-49 16.39-94.43 44.57-132.89 83.16C119.95 648.58 80.8 734.5 72.81 827.13a60.32 60.32 0 0 0 15.4 46 56.13 56.13 0 0 0 41.22 18.42h577.14a56 56 0 0 0 40.91-18.15 60.8 60.8 0 0 0 15.73-46z m-334.44-585a121.65 121.65 0 1 1-121.65 121.64A121.79 121.79 0 0 1 428.76 242.2z m277 592.43H130.14a3.43 3.43 0 0 1-0.64-2.53C143.76 667 267.75 542.42 417.91 542.42S692.16 666.88 706.48 832a3.92 3.92 0 0 1-0.68 2.63z" p-id="3160"></path><path d="M946.55 739.47A342.55 342.55 0 0 0 728 452.44a182.8 182.8 0 0 0 59.17-153.25c-7.83-80-68.84-146.06-148.44-160.75a182.67 182.67 0 0 0-97.33 8.85l20.15 53.23a124 124 0 0 1 66.93-6.1c53.85 9.93 96.77 56.33 102.05 110.34a125.86 125.86 0 0 1-72.09 126.31l-0.26 0.12a33 33 0 0 0 7.43 62c120 25.49 212.06 128.36 224.16 250.51H786.6v56.91h103.87a56.64 56.64 0 0 0 41.89-18.59 55.56 55.56 0 0 0 14.19-42.55z" p-id="3161"></path></svg>
                <span class="admin-sidebar-item">用户管理</span>
            </div>
            <div class="admin-item-box" 
                :class="{ active: $route.path.includes('/admin/api') }"
                @click="navigateTo('/admin/api')">
                <svg class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="22" height="22"><path d="M0 0h1024v1024H0z" fill="#FFFFFF" fill-opacity=".01" p-id="4345"></path><path d="M456.832 417.856c14.976 14.976 16.512 38.4 4.48 55.04l-4.48 5.248-55.168 55.168 88.96 88.96 55.232-55.104a42.688 42.688 0 0 1 64.832 55.04l-4.48 5.312-55.232 55.104 12.544 12.544c14.976 14.976 16.448 38.4 4.48 55.04l-4.48 5.312-64 64c-59.968 59.904-174.4 83.264-261.568 27.008L158.08 926.144a42.688 42.688 0 0 1-64.832-55.04l4.48-5.248 79.68-79.744c-56.32-87.168-32.896-201.664 27.008-261.632l64-64c16.64-16.64 43.712-16.64 60.352 0l12.48 12.48 55.168-55.104c16.64-16.64 43.712-16.64 60.352 0zM298.688 551.04l-33.856 33.792c-37.952 37.952-50.88 123.456 0 174.336 50.88 50.88 136.384 37.952 174.336 0l33.792-33.856L298.688 551.04z m627.456-453.184c15.04 14.976 16.512 38.4 4.48 55.04l-4.48 5.248-79.616 79.808c56.32 87.168 32.896 201.6-27.008 261.568l-64 64a42.688 42.688 0 0 1-60.352 0L460.48 328.832a42.688 42.688 0 0 1 0-60.352l64-64c59.968-59.904 174.464-83.264 261.632-27.008L865.92 97.92c16.64-16.64 43.648-16.64 60.288 0z m-167.04 167.04c-50.816-50.944-136.32-38.016-174.272 0l-33.792 33.792 174.272 174.272 33.856-33.792c36.032-36.032 49.536-115.008 7.168-166.4z" fill="#5C6577" p-id="4346"></path></svg>
                <span class="admin-sidebar-item">API管理</span>
            </div>
            <div class="admin-item-box" 
                :class="{ active: $route.path.includes('/admin/email') }"
                @click="navigateTo('/admin/email')">
                <svg t="1745058717928" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2338" width="22" height="22"><path d="M893.842 217.557H130.159c-16.261 0-29.443 13.182-29.443 29.443v530c0 16.261 13.182 29.443 29.443 29.443h763.683c16.261 0 29.443-13.183 29.443-29.443V247c0-16.261-13.182-29.443-29.443-29.443z m-85.584 58.886L512 507.651 215.742 276.443h592.516zM159.602 747.557v-440.23l334.283 260.885A29.4 29.4 0 0 0 512 574.443a29.4 29.4 0 0 0 18.115-6.231l334.283-260.884v440.229H159.602z" fill="" p-id="2339"></path></svg>
                <span class="admin-sidebar-item">邮件配置</span>
            </div>
            <div class="admin-item-box" 
                :class="{ active: $route.path.includes('/admin/config') }"
                @click="navigateTo('/admin/config')">
                <svg t="1745058770784" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3346" width="22" height="22"><path d="M469.333333 60.693333a85.333333 85.333333 0 0 1 85.333334 0l326.826666 188.714667a85.333333 85.333333 0 0 1 42.666667 73.898667v377.386666a85.333333 85.333333 0 0 1-42.666667 73.898667L554.666667 963.306667a85.333333 85.333333 0 0 1-85.333334 0L142.506667 774.592a85.333333 85.333333 0 0 1-42.666667-73.898667v-377.386666a85.333333 85.333333 0 0 1 42.666667-73.898667z m42.666667 73.898667L185.173333 323.306667v377.386666L512 889.408l326.826667-188.714667v-377.386666L512 134.592zM512 341.333333a170.666667 170.666667 0 1 1 0 341.333334 170.666667 170.666667 0 0 1 0-341.333334z m0 85.333334a85.333333 85.333333 0 1 0 0 170.666666 85.333333 85.333333 0 0 0 0-170.666666z" fill="#222429" p-id="3347"></path></svg>
                <span class="admin-sidebar-item">系统设置</span>
            </div>
        </div>
        <div class="admin-content">
            <RouterView/>
        </div>
    </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView, useRouter } from "vue-router"
import { useSystemConfig } from "@/store/dataconfig"

const router = useRouter()
const systemConfig = useSystemConfig()

// 导航函数，使整个菜单项可点击
const navigateTo = (path: string) => {
  router.push(path)
}

// 页面加载时默认导航
router.push("/admin/user")
</script>

<style scoped>
.admin-container {
    display: flex;
    width: 100%;
    height: calc(100vh - 3.5rem);
    gap: 1rem;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}

.admin-sidebar {
    margin-left: 5px;
    width: 230px;
    height: 100%;
    display: flex;
    flex-direction: column;
    background-color: var(--background-color);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    gap: 0.7rem;
    position: relative;
    z-index: 1;
    border-radius: 20px;
}

.admin-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-color, #333);
    text-align: center;
    padding: 1.2rem 0;
    border-bottom: 1px solid #eee;
    user-select: none;
}

.admin-item-box {
    padding: 0.9rem 1.2rem;
    margin: 0 0.6rem;
    display: flex;
    align-items: center;
    cursor: pointer;
    border-radius: 12px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.admin-item-box:hover {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
    transform: translateX(5px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.admin-item-box.active {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

.admin-sidebar-item {
    text-decoration: none;
    color: var(--text-color, #555);
    font-size: 1rem;
    margin-left: 0.8rem;
    white-space: nowrap;
}

.admin-content {
    flex: 1;
    width: 82%;
    height: 100%;
    padding: 2rem;
    background-color: var(--background-color);
    border-radius: 24px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    overflow-y: auto;
}

/* 改进移动端适配 */
@media (max-width: 768px) {
    .admin-container {
        flex-direction: column;
        height: auto;
        min-height: calc(100vh - 3.5rem);
    }
    
    .admin-sidebar {
        width: 100%;
        margin: 0;
        flex-direction: row;
        overflow-x: hidden;
        height: auto;
        border-radius: 15px;
        box-shadow: 1px 0px 2px 2px rgba(0, 0, 0, 0.15);
        display: flex;
        justify-content: center; 
        align-items: center;
        gap:1px;
        padding: 0.5rem;
    }
    
    .admin-title {
        display: none;
    }
    
    .admin-item-box {
        width: auto;
        flex-shrink: 0;
        margin: 0 0.5rem;
        padding: 0.6rem;
        border-radius: 8px;
    }
    
    .admin-item-box.active {
        border-left: none;
        border-bottom: 3px solid #83b9ff;
    }
    
    .admin-content {
        width: 90%;
        display: flex;
        justify-content: start;
        margin-top: 0.5rem;
        overflow-x: hidden;
        overflow-y: auto;
    }
}

/* 特小屏幕适配 */
@media (max-width: 480px) {
    .admin-sidebar-item {
        display: none;
    }
    
    .admin-item-box {
        justify-content: center;
        padding: 0.5rem;
    }
    
    .admin-content {
        padding: 0.8rem;
    }
}
</style>