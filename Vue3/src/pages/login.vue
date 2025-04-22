<template>
  <div class="page-container">
    <div class="auth-container" :class="{ 'hover-effect': isHovered }" @mouseenter="isHovered = true" @mouseleave="isHovered = false">
      <!-- 标签切换 -->
      <div class="auth-tabs">
        <div class="tab-btn" :class="{ active: activeTab === 'login' }" @click="activeTab = 'login'">
          登录
        </div>
        <div class="tab-btn" :class="{ active: activeTab === 'register' }" @click="activeTab = 'register'">
          注册
        </div>
      </div>

      <!-- 表单内容容器 - 固定高度确保切换时不会改变容器大小 -->
      <div class="form-content-wrapper">
        <!-- 登录表单 -->
        <div v-if="activeTab === 'login'" class="auth-form-container">
          <h2 class="form-title">欢迎回来</h2>
          <form class="auth-form" @submit.prevent="login">
            <div class="form-group">
              <label for="login-username">用户名</label>
              <div class="input-with-icon">
                <span class="input-icon">@</span>
                <input
                  id="login-username"
                  v-model="dataUserName"
                  class="form-input"
                  type="text"
                  placeholder="请输入用户名"
                  autocomplete="username"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="login-password">密码</label>
              <div class="input-with-icon">
                <span class="input-icon">🔒</span>
                <input
                  id="login-password"
                  v-model="dataPassword"
                  class="form-input"
                  :type="showLoginPassword ? 'text' : 'password'"
                  placeholder="请输入密码"
                  autocomplete="current-password"
                />
                <span
                  class="toggle-password-btn"
                  @click="showLoginPassword = !showLoginPassword"
                >
                  显示
                </span>
              </div>
            </div>

            <button type="submit" class="submit-btn">登录</button>

            <div class="form-footer">
              <a href="#" class="forgot-password">忘记密码?</a>
            </div>
          </form>
        </div>

        <!-- 注册表单 -->
        <div v-if="activeTab === 'register'" class="auth-form-container">
          <h2 class="form-title">创建账号</h2>
          <form class="auth-form" @submit.prevent="register">
            <div class="form-group">
              <label for="register-username">用户名</label>
              <div class="input-with-icon">
                <span class="input-icon">@</span>
                <input
                  id="register-username"
                  v-model="dataUserName"
                  class="form-input"
                  type="text"
                  placeholder="请输入用户名"
                  autocomplete="username"
                />
              </div>
            </div>

            <div class="form-group" v-if="systemConfig.emailregister">
              <label for="register-email">邮箱</label>
              <div class="email-input-container">
                <div class="input-with-icon email-input-wrapper">
                  <span class="input-icon">✉️</span>
                  <input
                    id="register-email"
                    v-model="dataEmail"
                    class="form-input"
                    type="email"
                    placeholder="请输入邮箱"
                    autocomplete="email"
                  />
                </div>
                <button
                  type="button"
                  class="verification-btn"
                  :disabled="!isValidEmail || verificationSent"
                  @click="sendVerificationCode"
                >
                  {{ verificationSent ? `${countdown}s` : '获取验证码' }}
                </button>
              </div>
            </div>

            <div class="form-group" v-if="systemConfig.emailregister">
              <label for="verification-code">验证码</label>
              <div class="input-with-icon">
                <span class="input-icon">🔢</span>
                <input
                  id="verification-code"
                  v-model="verificationCode"
                  class="form-input"
                  type="text"
                  placeholder="请输入验证码"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="register-password">密码</label>
              <div class="input-with-icon">
                <span class="input-icon">🔒</span>
                <input
                  id="register-password"
                  v-model="dataPassword"
                  class="form-input"
                  :type="showRegisterPassword ? 'text' : 'password'"
                  placeholder="请输入密码"
                  autocomplete="new-password"
                />
                <span
                  class="toggle-password-btn"
                  @click="showRegisterPassword = !showRegisterPassword"
                >
                  显示
                </span>
              </div>
            </div>

            <div class="form-group">
              <label for="confirm-password">确认密码</label>
              <div class="input-with-icon">
                <span class="input-icon">🔒</span>
                <input
                  id="confirm-password"
                  v-model="confirmPassword"
                  class="form-input"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  placeholder="请再次输入密码"
                  autocomplete="new-password"
                />
                <span
                  class="toggle-password-btn"
                  @click="showConfirmPassword = !showConfirmPassword"
                >
                  显示
                </span>
              </div>
            </div>

            <button type="submit" class="submit-btn">注册</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import "@/App.vue"
import { ref, computed, watch } from "vue";
import axios from "axios";
import { useSystemConfig } from "@/store/dataconfig.ts"
import { useUserConfig } from "@/store/dataconfig.ts"
import { useConversationStore } from "@/store/dataconfig.ts"
import { useRouter } from "vue-router";
import { message } from "ant-design-vue";
import { onMounted } from "vue";

// 表单数据
let dataUserName = ref(''); // 用户名
let dataPassword = ref(''); // 密码
let dataEmail = ref(''); // 邮箱
let verificationCode = ref(''); // 验证码
let confirmPassword = ref(''); // 确认密码

// 密码显示控制
let showLoginPassword = ref(false);
let showRegisterPassword = ref(false);
let showConfirmPassword = ref(false);

// 使用正确的状态管理
const userStore = useUserConfig();
// 对话管理
const conversationStore = useConversationStore();

// 当前激活的标签页（登录/注册）
const activeTab = ref('login');

// 悬停效果控制
const isHovered = ref(false);

// 验证码发送状态
const verificationSent = ref(false);
const countdown = ref(60);

const messageAPI = message;

// 邮箱验证
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const isValidEmail = computed(() => {
  return emailRegex.test(dataEmail.value);
});

const systemConfig = useSystemConfig();
const userConfig = useUserConfig();
const router = useRouter();



onMounted(async ()=>{
  const response = await axios.get(systemConfig.baseurl + '/admin/config')
  systemConfig.emailregister = response.data.email_register;
})
// 获取验证码
async function sendVerificationCode() {
  if (!isValidEmail.value) return;
  // 发送验证码
  const response = await axios.post(systemConfig.baseurl + '/email/send_email', {"email": dataEmail.value });
  messageAPI.success('验证码发送成功');
  verificationSent.value = true;
  countdown.value = 60;

  // 倒计时
  const timer = setInterval(() => {
    countdown.value--;
    if (countdown.value <= 0) {
      clearInterval(timer);
      verificationSent.value = false;
    }
  }, 1000);

  // 这里只是UI改动，实际发送验证码的逻辑保持不变
  console.log('获取验证码', dataEmail.value);
}

// 注册函数
async function register() {
  if (systemConfig.emailregister && confirmPassword.value == dataPassword.value){
    const response = await axios.post(systemConfig.baseurl + "/user/register",{
      "username":dataUserName.value,
      "email":dataEmail.value,
      "code":verificationCode.value,
      "password":confirmPassword.value
    })
    //注册成功
    if(response.data == true) {
      messageAPI.success("注册成功！")
      activeTab.value = "login"
    }
    //验证码错误
    else if (response.data == false)messageAPI.error("注册失败:验证码错误！")
    //注册失败
    else if (response.data['error'] == 1) messageAPI.error("用户名已存在！")
    else if (response.data['error'] == 2) messageAPI.error("邮箱已存在！")
    else if (response.data['error'] == 3) messageAPI.error("验证码超时！")
    else if (response.data['error'] == 4) messageAPI.error("未提交验证码！")
    else messageAPI.error(`注册失败:${response.data['error']}`)
  }
  else if (!systemConfig.emailregister) {
    const response = await axios.post(systemConfig.baseurl + "/user/register",{
      "username":dataUserName.value,
      "email":"",
      "code":"",
      "password":confirmPassword.value
    })
    //注册成功
    if(response.data == true) {
      messageAPI.success("注册成功！")
      activeTab.value = "login"
    }
    //验证码错误
    else if (response.data == false)messageAPI.error("注册失败:验证码错误！")
    //注册失败
    else if (response.data['error'] == 1) messageAPI.error("用户名已存在！")
    else if (response.data['error'] == 2) messageAPI.error("邮箱已存在！")
    else if (response.data['error'] == 3) messageAPI.error("验证码超时！")
    else if (response.data['error'] == 4) messageAPI.error("未提交验证码！")
    else messageAPI.error(`注册失败:${response.data['error']}`)
  }
  // 保持原有逻辑不变
}

// 登录函数
async function login() {
  const formData = new FormData();
  formData.append('username', dataUserName.value);
  formData.append('password', dataPassword.value);
  try {
    const response = await axios.post(systemConfig.baseurl + '/user/token', formData);
    if (response.data["error"] == "None"){
      messageAPI.error("没有该用户！")
      return false
    }
    else{
      const token = response.data.token.access_token; //还需要接收用户消息，聊天记录
      localStorage.setItem('JWTtoken', token);
      messageAPI.success("登陆成功！")
      const UserConfig = response.data.user
      //信息同步
      userStore.userinfo.userID = UserConfig.userinfo.id;
      userStore.userinfo.username = UserConfig.userinfo.username;
      userStore.userinfo.email = UserConfig.userinfo.email;
      userStore.userinfo.money = UserConfig.userinfo.money;
      userStore.userinfo.userauth = UserConfig.userinfo.userauth;

      //聊天同步
      conversationStore.conversations = UserConfig.chats
      userStore.setLoginStatus(true);
      
       // 如果有对话记录，选择第一个对话，否则创建新对话
      if (UserConfig.chats && UserConfig.chats.length > 0) {
        conversationStore.selectConversation(UserConfig.chats[0].id);
      } else {
        await conversationStore.createNewConversation();
      }
    }
    
    
    // 使用正确的状态管理
    router.push('/');
  } catch (error: any) {
    messageAPI.error(`登录失败:密码错误！`);
  }
}

// 监听标签切换，重置表单
watch(activeTab, () => {
  dataUserName.value = '';
  dataPassword.value = '';
  dataEmail.value = '';
  verificationCode.value = '';
  confirmPassword.value = '';
  showLoginPassword.value = false;
  showRegisterPassword.value = false;
  showConfirmPassword.value = false;
});
</script>

<style scoped>
/* 页面容器 */
.page-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: var(--background-color);
  padding: 20px;
}

/* 认证容器 */
.auth-container {
  width: 400px; /* 固定宽度 */
  background-color: #121212;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
}

/* 悬停效果 */
.auth-container.hover-effect {
  box-shadow: 0 0 20px 10px rgba(0, 255, 200, 0.3);
}

.auth-container.hover-effect::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, #00e5cc, #2979ff);
  border-radius: 14px;
  z-index: -1;
  animation: borderAnimation 3s linear infinite;
}

@keyframes borderAnimation {
  0% {
    filter: hue-rotate(0deg);
  }
  100% {
    filter: hue-rotate(360deg);
  }
}
@media (max-width: 768px) {
  .page-container {
    width: 80%;
  }
}

/* 标签切换样式 */
.auth-tabs {
  display: flex;
  background-color: #121212;
  border-bottom: 1px solid #333;
}

.tab-btn {
  flex: 1;
  padding: 15px 0;
  text-align: center;
  font-size: 16px;
  color: #999;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tab-btn.active {
  color: #fff;
  position: relative;
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 25%;
  width: 50%;
  height: 3px;
  background: linear-gradient(90deg, #00e5cc, #2979ff);
  border-radius: 3px 3px 0 0;
}

/* 表单内容包装器 - 确保两个表单占用相同的空间 */
.form-content-wrapper {
  position: relative;
  min-height: 400px; /* 设置一个最小高度，确保登录表单有足够空间 */
}

/* 表单容器 */
.auth-form-container {
  padding: 24px;
  width: 100%;
  box-sizing: border-box;
}

.form-title {
  margin: 0 0 24px;
  font-size: 20px;
  font-weight: normal;
  color: #fff;
  text-align: center;
}

/* 表单样式 */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  color: #ccc;
}

.input-with-icon {
  position: relative;
  width: 100%;
}

.input-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #777;
  font-size: 16px;
}

.form-input {
  width: 100%;
  height: 44px;
  padding: 0 12px 0 36px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  color: #fff;
  background-color: #222;
  box-sizing: border-box;
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  background-color: #2a2a2a;
  box-shadow: 0 0 0 2px rgba(0, 229, 204, 0.2);
}

.form-input::placeholder {
  color: #777;
}

/* 邮箱输入框和验证码按钮容器 */
.email-input-container {
  display: flex;
  gap: 8px;
}

.email-input-wrapper {
  flex: 1;
}

.verification-btn {
  min-width: 100px;
  height: 44px;
  background: linear-gradient(90deg, #00e5cc, #2979ff);
  color: #121212;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.3s ease;
}

.verification-btn:hover:not(:disabled) {
  background: linear-gradient(90deg, #00ccb4, #2563eb);
  transform: translateY(-2px);
}

.verification-btn:disabled {
  background: #333;
  color: #777;
  cursor: not-allowed;
}

/* 密码输入框和显示/隐藏按钮容器 */
.toggle-password-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 14px;
  color: #777;
  cursor: pointer;
  user-select: none;
}

.toggle-password-btn:hover {
  color: #00e5cc;
}

/* 提交按钮 */
.submit-btn {
  width: 100%;
  height: 44px;
  margin-top: 10px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  background: linear-gradient(90deg, #00e5cc, #2979ff);
  color: #121212;
}

.submit-btn:hover {
  background: linear-gradient(90deg, #00ccb4, #2563eb);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 229, 204, 0.3);
}

/* 表单底部 */
.form-footer {
  margin-top: 20px;
  text-align: center;
}

.forgot-password {
  font-size: 14px;
  color: #00e5cc;
  text-decoration: none;
  transition: all 0.2s ease;
}

.forgot-password:hover {
  color: #2979ff;
  text-decoration: underline;
}
</style>