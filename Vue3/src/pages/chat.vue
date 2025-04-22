<template>
  <div class="chat-container">
    <!-- 左侧聊天管理组件 -->
    <Lside class="lside" ref="lsideRef"/>
    
    <!-- 主聊天区域，包含输入框 -->
    <div class="Chat">
      <!-- 气泡区域 -->
      <div class="chat-area" ref="chatAreaRef">
        <!-- 每一个气泡 -->
        <div v-for="(chatMessage) in chatStore.currentMessages" :key="chatMessage.id" class="chat-box">
          <Transition>
            <Bubble
              ref="content"
              :autoScroll="true"
              :loading="false"
              v-bind:placement="chatMessage.isuser ? 'end' : 'start'"
              @mouseenter="hoveredMessageIndex = chatMessage.id"
              @mouseleave="hoveredMessageIndex = null"
              :styles="{
                content: {
                  backgroundColor: systemStore.theme?'rgba(0, 0, 0, 0.60)':'rgba(255, 255, 255, 0.80)',
                  borderRadius: '12px',
                  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
                  backdropFilter: 'blur(5px)',
                  maxWidth: '100%',
                  wordBreak: 'break-word',
                }
              }"
            >
              <template #avatar>
                <Avatar
                  :icon="h(UserOutlined)"
                  :style="chatMessage.isuser ? userAvatarStyle : aiAvatarStyle"
                />
              </template>
              <template #header>
                <div :class="chatMessage.isuser?'user-message-header':'ai-message-header'">
                  <span class="message-header-text">{{ chatMessage.isuser ? 'user' : 'assistant' }}</span>
                </div>
              </template>
              <template #message>
                <div class="message-content">
                  <MdPreview 
                    :theme="systemStore.theme ? 'dark' : 'light'"
                    :codeTheme="systemStore.theme ? 'github' : 'atom'"
                    v-model="chatMessage.content"
                    previewOnly
                    previewTheme="github"
                    :style="{ background: 'transparent' }"
                  />
                </div>
              </template>
              <template #footer>
                <transition name="fade">
                  <div class="chat-message-actions" :class="{ 'show-actions': hoveredMessageIndex === chatMessage.id }">
                    <div v-if="chatMessage.isuser" class="chat-message">
                      <button class="action-btn copy-btn" @click="copyMessage(chatMessage.content)" title="复制">
                        <svg class="action-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M8 4V16C8 16.5523 8.44772 17 9 17H19C19.5523 17 20 16.5523 20 16V7.41421C20 7.149 19.8946 6.89464 19.7071 6.70711L16.2929 3.29289C16.1054 3.10536 15.851 3 15.5858 3H9C8.44772 3 8 3.44772 8 4Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                          <path d="M16 3V7H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          <path d="M16 13H12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          <path d="M16 9H12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          <path d="M4 8V20C4 20.5523 4.44772 21 5 21H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span class="action-text">复制</span>
                      </button>
                      <button class="action-btn edit-btn" @click="editMessage(chatMessage.id)" title="编辑">
                        <svg class="action-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M13.0207 5.82839L15.8491 2.99996L20.7988 7.94971L17.9704 10.7781M13.0207 5.82839L3.41386 15.435C3.22099 15.6279 3.11713 15.8759 3.1228 16.1342L3.25742 19.3342C3.26443 19.6596 3.53322 19.9284 3.85858 19.9354L7.05858 20.0701C7.31688 20.0757 7.56485 19.9718 7.75774 19.779L17.3646 10.1723M13.0207 5.82839L17.3646 10.1723" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span class="action-text">编辑</span>
                      </button>
                      <button class="action-btn delete-btn" @click="deleteMessage(chatMessage.id)" title="删除">
                        <svg class="action-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M3 6H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          <path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span class="action-text">删除</span>
                      </button>
                    </div>
                    <div v-else class="chat-message">
                      <button class="action-btn copy-btn" @click="copyMessage(chatMessage.content)" title="复制">
                        <svg class="action-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M8 4V16C8 16.5523 8.44772 17 9 17H19C19.5523 17 20 16.5523 20 16V7.41421C20 7.149 19.8946 6.89464 19.7071 6.70711L16.2929 3.29289C16.1054 3.10536 15.851 3 15.5858 3H9C8.44772 3 8 3.44772 8 4Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                          <path d="M16 3V7H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          <path d="M16 13H12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          <path d="M16 9H12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          <path d="M4 8V20C4 20.5523 4.44772 21 5 21H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span class="action-text">复制</span>
                      </button>
                      <button class="action-btn regenerate-btn" @click="regenerateResponse(chatMessage.id)" title="重新生成">
                        <svg class="action-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M19.7285 10.9288C20.4413 13.5978 19.7507 16.5635 17.6569 18.6573C14.5327 21.7815 9.46734 21.7815 6.34315 18.6573C3.21895 15.5331 3.21895 10.4677 6.34315 7.34352C9.46734 4.21933 14.5327 4.21933 17.6569 7.34352L21 10.6866" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          <path d="M21 4V10.6866H14.3137" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span class="action-text">重新生成</span>
                      </button>
                      <button class="action-btn delete-btn" @click="deleteMessage(chatMessage.id)" title="删除">
                        <svg class="action-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M3 6H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          <path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span class="action-text">删除</span>
                      </button>
                    </div>
                  </div>
                </transition>
              </template>
            </Bubble>
          </Transition>
        </div>
      </div>
        <INput ref="inputRef"/>
        <div class="tobottom" @click="tobottom">
      <svg v-if="!systemStore.theme" t="1744904680050" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3864" width="16" height="16"><path d="M880.9 961.27H143.1c-24.91 0-45.1-20.19-45.1-45.1s20.19-45.1 45.1-45.1h737.8c24.91 0 45.1 20.19 45.1 45.1s-20.2 45.1-45.1 45.1zM543.9 811.04c-17.62 17.62-46.16 17.62-63.77 0L169.4 500.34c-17.62-17.62-17.62-46.16 0-63.77s46.16-17.62 63.77 0l233.74 233.72V107.83c0-24.91 20.19-45.1 45.1-45.1s45.1 20.19 45.1 45.1v562.45l233.72-233.72c8.81-8.81 20.35-13.21 31.89-13.21s23.08 4.4 31.89 13.21c17.62 17.62 17.62 46.16 0 63.77L543.9 811.04z" fill="#333333" p-id="3865"></path></svg>    
      <svg v-else t="1744904680050" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3864" width="16" height="16"><path d="M880.9 961.27H143.1c-24.91 0-45.1-20.19-45.1-45.1s20.19-45.1 45.1-45.1h737.8c24.91 0 45.1 20.19 45.1 45.1s-20.2 45.1-45.1 45.1zM543.9 811.04c-17.62 17.62-46.16 17.62-63.77 0L169.4 500.34c-17.62-17.62-17.62-46.16 0-63.77s46.16-17.62 63.77 0l233.74 233.72V107.83c0-24.91 20.19-45.1 45.1-45.1s45.1 20.19 45.1 45.1v562.45l233.72-233.72c8.81-8.81 20.35-13.21 31.89-13.21s23.08 4.4 31.89 13.21c17.62 17.62 17.62 46.16 0 63.77L543.9 811.04z" fill="#ffffff" p-id="3865"></path></svg>
    </div>
  </div>
  </div>
</template>
<script setup lang='ts'>
import INput from "@/pages/chat/input.vue"         // 输入框组件
import Lside from "@/pages/chat/chatManage.vue"    // 左侧聊天管理组件
import { Bubble } from 'ant-design-x-vue';         // 气泡组件
import { useConversationStore } from "@/store/dataconfig.ts"; // 对话管理存储
import { watch, nextTick, ref, h } from 'vue';        // Vue核心函数
import { message, Modal, Avatar } from 'ant-design-vue';          // 导入message服务
import { UserOutlined } from '@ant-design/icons-vue';
import { useUserConfig, useSystemConfig } from "@/store/dataconfig.ts"; // 导入用户配置store
import { MdPreview } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
import axios from 'axios';
const messageApi = message;
  
// 使用Pinia store获取聊天数据和用户配置
const chatStore = useConversationStore();
const systemStore = useSystemConfig();
const userStore = useUserConfig();
  
// 输入框组件引用
const inputRef = ref<InstanceType<typeof INput> | null>(null);
  
// 聊天区域DOM引用，用于滚动控制
const chatAreaRef = ref<HTMLDivElement | null>(null);
const lsideRef = ref();
let content = ref()
// 当前悬停的消息索引
const hoveredMessageIndex = ref<string | null>(null);

const tobottom = () => {
  if(chatAreaRef.value) chatAreaRef.value.scrollTop = chatAreaRef.value.scrollHeight;
  return ;
}

// 头像样式
const userAvatarStyle = {
  color: '#f56a00',
  backgroundColor: '#fde3cf',
};

const aiAvatarStyle = {
  color: '#fff',
  backgroundColor: '#87d068',
};

  
// 复制消息内容
const copyMessage = (content: string) => {
  navigator.clipboard.writeText(content)
    .then(() => {
      messageApi.success('复制成功');
    })
    .catch(err => {
      messageApi.error('复制失败: ' + err);
    });
};
  
// 重新生成响应
const regenerateResponse = async (messageId: string) => {
  const found = chatStore.findMessage(messageId)
  if(!found) return;

  if (!chatStore.selectedConversationId) {
    messageApi.error('请先选择一个对话或创建新对话');
    return;
  }

  chatStore.updateMessage(messageId, '');

  if(!chatStore.currentConversation) return;

  const messages = chatStore.currentConversation.chatmessages;
  const currentMsgIndex = messages.findIndex(msg => msg.id === messageId);
  if (currentMsgIndex === -1 || currentMsgIndex === 0) return;
  
  const historyCount = Math.min(systemStore.message_max + 1, currentMsgIndex);
  const history_message = historyCount > 0 ? 
    messages.slice(currentMsgIndex - historyCount, currentMsgIndex) : [];

  try {
    const response = await fetch(systemStore.baseurl + '/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('JWTtoken')}` },
      body: JSON.stringify({
        username: userStore.userinfo.username,
        model_name: systemStore.model_name,
        api_name: systemStore.api_name,
        history_message:history_message,
        message: "重新生成",
        filelist_id: []
      })
    });
    
    if (!response.ok) throw new Error(`HTTP错误: ${response.status}`);
    
    const reader = response.body?.getReader();
    if (!reader) throw new Error('无法获取响应流');
    
    const decoder = new TextDecoder();
    
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value, { stream: true });
      for (const line of chunk.split('\n')) {
        if (!line.trim()) continue;
        try {
          const data = JSON.parse(line);
          if (data.content) {
            chatStore.updateMessage(messageId, data.content, true);
          }
        } catch {
          // 忽略JSON解析错误
        }
      }
    }
  } catch (error: any) {
    console.error("错误:", error);
    chatStore.updateMessage(messageId, "请求失败: " + (error.message || "未知错误"));
  }
  
  // 同步消息到服务器
  if (userStore.isLoggedIn) {
    try {
      await axios.post(systemStore.baseurl + '/message/Updatemessage', {
        username: userStore.userinfo.username,
        message: chatStore.conversations[found.convIndex].chatmessages[found.msgIndex].content,
        messageId:messageId
      }, {
        headers: { 
          'Content-Type': 'application/json', 
          Authorization: `Bearer ${localStorage.getItem('JWTtoken')}` 
        }
      });
    } catch (error) {
      console.error('同步消息失败:', error);
      messageApi.error('消息同步失败');
    }
  }
};
  
// 编辑消息
const editMessage = async (messageId: string) => {
  const found = chatStore.findMessage(messageId);
  if (!found || !inputRef.value) return;
  
  const { convIndex, msgIndex } = found;
  const message = chatStore.conversations[convIndex].chatmessages[msgIndex];
  if (!message.isuser) return;
  
  inputRef.value.setInputValue(message.content);
  
  const confirmEdit = async () => {
    const newContent = inputRef.value?.getInputValue()?.trim();
    if (!newContent) {
      messageApi.warning('消息内容不能为空');
      return;
    }
    
    chatStore.updateMessage(messageId, newContent);
    inputRef.value?.setInputValue('');
    inputRef.value?.removeConfirmButton();
    messageApi.success('消息已更新');
     // 同步消息到服务器
     if (userStore.isLoggedIn) {
    try {
      await axios.post(systemStore.baseurl + '/message/Updatemessage', {
        username: userStore.userinfo.username,
        message: chatStore.conversations[found.convIndex].chatmessages[found.msgIndex].content,
        messageId:messageId,
      }, {
        headers: { 
          'Content-Type': 'application/json', 
          Authorization: `Bearer ${localStorage.getItem('JWTtoken')}` 
        }
      });
    } catch (error) {
      console.error('同步消息失败:', error);
      messageApi.error('消息同步失败');
    }
  }
  };
  
  inputRef.value.addConfirmButton('确认编辑', confirmEdit);
   
};
  
// 删除消息
const deleteMessage = async (messageId: string) => {
  const found = chatStore.findMessage(messageId)
  if(!found) return;

  Modal.confirm({
    title: '确认删除',
    content: '确定要删除这条消息吗？',
    okText: '删除',
    okType: 'danger',
    cancelText: '取消',
    onOk: async() => {
      const found = chatStore.findMessage(messageId);
      if (!found) return;
      
      const { convIndex } = found;
      chatStore.conversations[convIndex].chatmessages = 
     chatStore.conversations[convIndex].chatmessages.filter(msg => msg.id !== messageId);
        
    // 同步消息到服务器
    if (userStore.isLoggedIn) {
    try {
      await axios.post(systemStore.baseurl + '/message/Deletemessage', {
        username: userStore.userinfo.username,
        messageId:messageId
      }, {
        headers: { 
          'Content-Type': 'application/json', 
          Authorization: `Bearer ${localStorage.getItem('JWTtoken')}` 
        }
      });
    } catch (error) {
      console.error('同步消息失败:', error);
      messageApi.error('消息同步失败');
    }
  }
    }
  });
  

};

</script>

<style scoped>
/* 主容器布局 */
.chat-container {
  display: flex;
  height: calc(100vh - 3.5rem);
  width: 100vw;
  background: transparent;
}
  
/* 聊天区域布局 */
.Chat {
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: calc(100vh - 3.5rem);
  overflow: hidden;
  background-color: transparent;
  align-items: center;
}
  
/* 左侧菜单固定定位 */
.lside {
  position: fixed;
  height: calc(100vh - 3.5rem);
  z-index: 200;
}
  
/* 聊天消息区域样式 */
.chat-area {
  padding-top: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100vw;
  height: calc(100vh - 3.5rem - 80px);
  overflow-y: auto;
}
/* 聊天消息框样式 */
.chat-box {
  width: 70vw;
}
.tobottom {
  position: fixed;
  right: 2rem;
  bottom: 7rem;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  background: var(--text-ground);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  z-index: 1000;
}

.tobottom:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* 手机端适配 */
@media screen and (max-width: 768px) {
  .tobottom {
    right: 1rem;
    bottom: 6rem;
    width: 2rem;
    height: 2rem;
  }
}

.chat-area::-webkit-scrollbar {
  width: 6px;
}
  
.chat-area::-webkit-scrollbar-track {
  background: transparent;
}
  
.chat-area::-webkit-scrollbar-thumb {
  background-color: rgba(155, 155, 155, 0.5);
  border-radius: 20px;
}
  
.-input{
 background-color: transparent;
}
  
  
/* 聊天消息操作按钮样式 */
.chat-message-actions {
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease, transform 0.3s ease, visibility 0.3s ease;
  transform: translateY(5px);
}
  
.show-actions {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}
  
.chat-message {
  display: flex;
  gap: 0.8rem;
  padding: 0.3rem 0;
}
  
.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.3rem 0.5rem;
  border-radius: 8px;
  color: var(--text-color);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.7;
  transition: all 0.3s ease, transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
  
.action-icon {
  margin-right: 4px;
}
  
.action-text {
  font-size: 12px;
}
  
/* 复制按钮悬停样式 */
.copy-btn:hover {
  color: #1890ff;
  background-color: rgba(24, 144, 255, 0.1);
  transform: scale(1.1);
  opacity: 1;
  box-shadow: 0 2px 6px rgba(24, 144, 255, 0.2);
}
  
/* 编辑按钮悬停样式 */
.edit-btn:hover {
  color: #fa8c16;
  background-color: rgba(250, 140, 22, 0.1);
  transform: scale(1.1);
  opacity: 1;
  box-shadow: 0 2px 6px rgba(250, 140, 22, 0.2);
}
  
/* 删除按钮悬停样式 */
.delete-btn:hover {
  color: #ff4d4f;
  background-color: rgba(255, 77, 79, 0.1);
  transform: scale(1.1);
  opacity: 1;
  box-shadow: 0 2px 6px rgba(255, 77, 79, 0.2);
}
  
/* 重新生成按钮悬停样式 */
.regenerate-btn:hover {
  color: #52c41a;
  background-color: rgba(82, 196, 26, 0.1);
  transform: scale(1.1);
  opacity: 1;
  box-shadow: 0 2px 6px rgba(82, 196, 26, 0.2);
}
  
/* 深色模式适配 */
[data-theme="dark"] .Finput {
  background: var(--text-ground);
  border-top: 1px solid rgba(48, 48, 48, 0.5);
}
  
/* 聊天气泡主题样式 */
.chat-message-content {
  font-family: 'Microsoft YaHei';
  color: var(--text-color);
}

.ai-message-header {
  font-family: 'Microsoft YaHei';
  background: linear-gradient(45deg, #8a2be2, #0078d7);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-weight: bold;
}
.user-message-header {
  font-family: 'Microsoft YaHei';
  background: linear-gradient(45deg, #ff6b6b, #ff8e00);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-weight: bold;
}
/* 响应式设计 */
@media screen and (max-width: 768px) {
  .chat-area {
    width: 95%;
    margin: auto;
    gap: 0.3rem;
  }
    
  .action-btn {
    padding: 0.2rem;
  }
    
  .chat-box {
    width: 95%;
  }
}
  
/* 淡入淡出动画效果 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* 代码高亮样式 - 适应聊天气泡 */
:deep(.code-block) {
  margin: 0.5em 0;
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.03);
  overflow: auto;
  max-height: 300px;
}

:deep(.hljs) {
  background: transparent !important;
  padding: 0.8em;
  border-radius: 6px;
  font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
  font-size: 0.9em;
  line-height: 1.5;
}

/* 用户和AI消息中的代码块样式调整 */
:deep(.markdown-body) {
  color: inherit;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* 暗色模式适配 */
[data-theme="dark"] :deep(.code-block) {
  background: rgba(255, 255, 255, 0.05);
}

[data-theme="dark"] :deep(.markdown-body pre) {
  background-color: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

[data-theme="dark"] :deep(.markdown-body code:not(.hljs)) {
  background-color: rgba(255, 255, 255, 0.06);
}

.message-content {
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
  background: transparent;
}

:deep(.message-content .md-preview) {
  color: inherit !important;
}

:deep(.message-content .md-preview-wrapper) {
  padding: 0 !important;
  margin: 0 !important;
}

:deep(.message-content .md-preview p) {
  margin: 0;
  padding: 0;
}

:deep(.message-content .md-preview pre),
:deep(.message-content .md-preview code) {
  background: var(--code-background, rgba(0, 0, 0, 0.05)) !important;
}

[data-theme="dark"] :deep(.message-content .md-preview pre),
[data-theme="dark"] :deep(.message-content .md-preview code) {
  background: var(--code-background, rgba(255, 255, 255, 0.05)) !important;
}
</style> 