import { createApp } from "vue"
import App from "./App.vue"
import chat_router from "@/router/content.ts"
import { createPinia } from "pinia"
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

const app = createApp(App)
const pinia = createPinia()

// 修改：添加Pinia持久化插件
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(chat_router)
app.mount("#app")
