import { createWebHistory, createRouter } from 'vue-router'
import Chat from "@/pages/chat.vue"
import Login from "@/pages/login.vue"
import Setting from "@/pages/setting.vue"
import UserInfo from "@/pages/userinfo.vue"
import ModCF from "@/pages/setting/mod_config.vue"
import Admin from "@/pages/admin.vue"
import User from "@/pages/admin/user.vue"
import API from "@/pages/admin/api.vue"
import Email from "@/pages/admin/email.vue"
import Config from "@/pages/admin/config.vue"
import { useUserConfig,useSystemConfig  } from '@/store/dataconfig.ts'
import { message } from 'ant-design-vue'
import axios from 'axios'

// 路由配置，meta.requiresAuth 标记是否需要登录
const chat_router = createRouter({
    history:createWebHistory(),
    routes: [
        {
            name:'home',
            path:"/",
            component:Chat,
            meta: { requiresAuth: true }
        },
        {
            name:'chat_',
            path: "/chat",
            component:Chat,
            meta: { requiresAuth: true }
        },
        {
            name:'userinfo_',
            path: "/userinfo",
            component: UserInfo,
            meta: { requiresAuth: true }
        },
        {
            name:'setting_',
            path: "/setting",
            component: Setting,
            meta: { requiresAuth: true },
            children: [
                {
                    name:"modconfig_",
                    path: 'modconfig',
                    component: ModCF,
                    meta: { requiresAuth: true },
                },
              ],
        },
        {
            name:'login_',
            path:"/login",
            component: Login,
            meta: { requiresAuth: false }
        },
        {
            name:'admin_',
            path:"/admin",
            component: Admin,
            meta: { requiresAuth: true },
            children:[
                {
                    name:"user_",
                    path:"user",
                    component: User,
                    meta:{
                        requiresAuth:true,
                        adminAuth:true
                    }
                },
                {
                    name:"api_",
                    path:"api",
                    component: API,
                    meta:{
                        requiresAuth:true,
                        adminAuth:true
                    }
                },
                {
                    name:"email_",
                    path:"email",
                    component: Email,
                    meta:{
                        requiresAuth:true,
                        adminAuth:true
                    }
                },
                {
                    name:"config_",
                    path:"config",
                    component: Config,
                    meta:{
                        requiresAuth:true,
                        adminAuth:true
                    }
                },
            ]
        }
    ]
})

/**
 * 检查用户登录状态
 * 发送token到后端验证，并更新store中的登录状态
 * @returns {Promise<boolean>} 是否已登录
 */
const checkLoginStatus = async () => {
    // 在函数内部获取store实例，避免Pinia初始化问题
    const systemStore = useSystemConfig()
    const userConfig = useUserConfig()
    
    try {
        const token = localStorage.getItem("JWTtoken")
        if (!token) {
            userConfig.isLoggedIn = false
            return false
        }
        
        const res_token = await axios.post(
            systemStore.baseurl + "/user/verify", 
            {},  // 空对象作为请求体
            {
                timeout: 1000,
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        )
        
        return res_token.data
    } catch (error) {
        console.error("Token验证失败:", error)
        userConfig.isLoggedIn = false
        return false
    }
}

/**
 * 全局路由守卫
 * 拦截需要登录的页面，检查用户登录状态
 */
chat_router.beforeEach(async (to, from) => {
    const userConfig = useUserConfig()

    // 如果访问登录页，直接放行
    if (to.name === 'login_') {
        return true
    }

    // 检查是否需要登录
    if (to.meta.requiresAuth) {
        const userauth = await checkLoginStatus()

        if (!userauth.islogin) {
            // 未登录，保存目标路由并跳转到登录页
            sessionStorage.setItem("lastRoute", to.fullPath)
            message.warning('请先登录!')
            return { name: 'login_' }
        }

        // 更新本地登录状态
        userConfig.setLoginStatus(true)

        // 检查管理员权限
        if (to.meta.adminAuth && !userauth.userauth) {
            message.warning('您没有管理员权限!')
            return { name: 'home' }
        }
    }
})

export default chat_router