<template>
  <div class="userinfo-container">
    <div class="user-card">
      <div class="card-header">
        <div class="avatar" @click="isLoggedIn && !isEditing && openAvatarUpload()">
          <img v-if="avatar" :src="avatar" alt="头像" />
          <span v-else>{{ userconfig.isLoggedIn ? userconfig.userinfo.username.charAt(0).toUpperCase() : '?' }}</span>
          <div v-if="isLoggedIn && !isEditing" class="avatar-edit">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
          </div>
          <input type="file" ref="avatarInput" style="display:none" accept="image/*" @change="handleAvatarChange" />
        </div>
        <h2>用户信息</h2>
        <div v-if="isLoggedIn && !isEditing" class="edit-btn" @click="startEdit">编辑资料</div>
      </div>
      
      <div v-if="isLoggedIn">
        <div v-if="!isEditing" class="info-list">
          <div class="info-row"><span>用户ID</span><span>{{ userconfig.userinfo.userID }}</span></div>
          <div class="info-row"><span>用户名</span><span>{{ userconfig.userinfo.username }}</span></div>
          <div class="info-row"><span>邮箱</span><span>{{ userconfig.userinfo.email }}</span></div>
          <div class="info-row"><span>余额</span><span class="money">¥{{ userconfig.userinfo.money }}</span></div>
          
          <div v-if="userconfig.userinfo.userauth === 2" class="badge superadmin">超级管理员</div>
          <div v-if="userconfig.userinfo.userauth === 1" class="badge admin">管理员</div>
          <div class="badge status"><span class="dot"></span>已登录</div>
        </div>
        
        <form v-else class="edit-form" @submit.prevent="saveChanges">
          <div class="field">
            <label>用户名</label>
            <input v-model="form.username" placeholder="输入新用户名" />
          </div>
          <div class="field">
            <label>当前密码</label>
            <input type="password" v-model="form.currentPwd" placeholder="输入当前密码" />
          </div>
          <div class="field">
            <label>新密码</label>
            <input type="password" v-model="form.newPwd" placeholder="输入新密码" />
          </div>
          <div class="field">
            <label>确认密码</label>
            <input type="password" v-model="form.confirmPwd" placeholder="再次输入新密码" />
          </div>
          <div class="btns">
            <button type="button" class="cancel" @click="isEditing = false">取消</button>
            <button type="submit" class="save">保存</button>
          </div>
        </form>
      </div>
      
      <div v-else class="login-tip">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#a0aec0" stroke-width="2"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path><polyline points="10 17 15 12 10 7"></polyline><line x1="15" y1="12" x2="3" y2="12"></line></svg>
        <p>请先登录查看个人信息</p>
      </div>
    </div>
    
    <div v-if="msg.show" :class="['msg', msg.type]">{{ msg.text }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useUserConfig, useSystemConfig } from "@/store/dataconfig.ts"
import axios from "axios"
import { message } from 'ant-design-vue'

const userconfig = useUserConfig()
const systemConfig = useSystemConfig()
const baseurl = computed(() => systemConfig.baseurl)
const isLoggedIn = computed(() => userconfig.isLoggedIn)
const avatar = ref('')
const loading = ref(false)
const avatarInput = ref<HTMLInputElement | null>(null)
const isEditing = ref(false)

// 表单数据
const form = reactive({
  username: userconfig.userinfo.username,
  currentPwd: '',
  newPwd: '',
  confirmPwd: ''
})

// 消息提示
const msg = reactive({show: false, text: '', type: 'success'})


// 函数处理
const startEdit = () => {
  form.username = userconfig.userinfo.username
  form.currentPwd = form.newPwd = form.confirmPwd = ''
  isEditing.value = true
}

const openAvatarUpload = () => avatarInput.value?.click()

const handleAvatarChange = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => { if (e.target?.result) avatar.value = e.target.result as string }
    reader.readAsDataURL(file)
  }
}

const showMsg = (text: string, type = 'success') => {
  Object.assign(msg, { text, type, show: true })
  setTimeout(() => msg.show = false, 3000)
}

const saveChanges = async () => {
  if (form.newPwd && form.newPwd !== form.confirmPwd) {
    showMsg('两次输入的密码不一致', 'error')
    return
  }
  
  try {
    const token = localStorage.getItem('JWTtoken')
    if (!token) {
      showMsg('用户未登录，请先登录', 'error')
      return
    }

    const userData = {
      username: form.username,
      current_password: form.currentPwd || null,
      new_password: form.newPwd || null
    }

    const response = await axios.post(`${baseurl.value}/user/update`, userData, {
      headers: { 
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (response.data && response.data.code === 0) {
      userconfig.userinfo.username = form.username
      isEditing.value = false
      showMsg('用户信息更新成功')
    } else {
      const errorMsg = response.data?.msg || '更新失败，请重试'
      showMsg(errorMsg, 'error')
    }
  } catch (error: any) {
    const errorMsg = error.response?.data?.msg || '更新失败，请重试'
    showMsg(errorMsg, 'error')
  }
}

// 获取用户信息
const fetchUserInfo = async () => {
  if (!userconfig.isLoggedIn) return
  
  loading.value = true
  try {
    const token = localStorage.getItem('JWTtoken')
    if (!token) return
    
    const response = await axios.get(`${baseurl.value}/user/info`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    if (response.data) {
      // 更新用户信息到Pinia存储
      userconfig.userinfo = response.data
      console.log('用户信息已更新:', response.data)
    }
  } catch (error: any) {
    console.error('获取用户信息失败:', error)
    message.error(error.response?.data?.msg || '获取用户信息失败')
  } finally {
    loading.value = false
  }
}

// 页面加载时自动获取用户信息
onMounted(() => {
  fetchUserInfo()
})
</script>

<style scoped>
.userinfo-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  padding: 2rem;
  background-color: var(--background-color, #f5f7fa);
  position: relative;
}
@media (max-width: 768px) {
  .user-card {
    transform: scale(0.8);
    transform-origin: center;
  }
}
.user-card {
  background-color: var(--text-ground, white);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
  min-width: 380px;
  transition: transform .3s, box-shadow .3s;
}

.user-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
  position: relative;
}

.avatar {
  width: 80px;
  height: 80px;
  margin-bottom: 1rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #edff47, #00fff2);
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-size: 32px;
  font-weight: bold;
  box-shadow: 0 5px 15px rgba(107,142,251,0.4);
  overflow: hidden;
  cursor: pointer;
  position: relative;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-edit {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 30%;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity .2s;
}

.avatar:hover .avatar-edit { opacity: 1; }

.edit-btn {
  margin-top: 10px;
  cursor: pointer;
  font-size: 0.9rem;
  color: #6e8efb;
  text-decoration: underline;
}

.edit-btn:hover { color: #a777e3; }

h2 {
  margin: 0;
  color: var(--text-color, #2c3e50);
  font-size: 1.8rem;
  font-weight: 600;
}

.info-list { position: relative; }

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.info-row:last-child { border-bottom: none; }

.info-row span:first-child {
  color: var(--text-color-light, #7f8c8d);
  font-weight: 500;
}

.info-row span:last-child {
  color: var(--text-color, #2c3e50);
  font-weight: 600;
}

.money { color: #00a389; }

.badge {
  position: absolute;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  color: white;
  top: -20px;
}

.status {
  right: 0;
  background-color: #10b981;
  display: flex;
  align-items: center;
}

.superadmin {
  left: 0;
  background-color: #f59e0b;
  font-weight: bold;
}
.admin {
  left: 0;
  background-color: #00aaff;
  font-weight: bold;
}
.dot {
  width: 8px;
  height: 8px;
  background-color: white;
  border-radius: 50%;
  margin-right: 6px;
  display: inline-block;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

.login-tip {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #7f8c8d;
  padding: 1.5rem;
}

/* 表单样式 */
.edit-form { padding: 1rem 0; }
.field { margin-bottom: 1.2rem; }

.field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #7f8c8d;
}

.field input {
  width: 95%;
  padding: 0.8rem;
  border: 1px solid rgba(0,0,0,0.1);
  border-radius: 8px;
  background-color: #f5f7fa;
  font-size: 1rem;
}

.field input:focus {
  outline: none;
  border-color: #6e8efb;
  box-shadow: 0 0 0 3px rgba(110,142,251,0.2);
}

.btns {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 1.5rem;
}

button {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
}

.cancel {
  background-color: #e2e8f0;
  color: #4a5568;
}
.cancel:hover { background-color: #cbd5e0; }

.save {
  background-color: #6e8efb;
  color: white;
}
.save:hover { background-color: #5a78e6; }

/* 消息提示 */
.msg {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 12px 20px;
  border-radius: 8px;
  color: white;
  font-weight: 500;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 1000;
  animation: slideIn .3s forwards;
}

.success { background-color: #10b981; }
.error { background-color: #ef4444; }

@keyframes slideIn {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
</style>