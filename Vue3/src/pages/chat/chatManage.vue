<template>
<div class="chat_input">
  <!-- 侧边栏主体 -->
  <div :class="!isCollapsed ? 'sidebar-wrapper' : 'sidebar-wrapper-hidden'">
    <div v-if="!isCollapsed" class="sidebar">
      <!-- 顶部区域 -->
      <div class="sidebar-top">
        <div class="sidebar-header">
          <span class="history">对话记录</span>
        </div>
        <button class="new-chat-btn" @click="conversationStore.createNewConversation">
          <svg class="plus-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span class="btn-text">新对话</span>
        </button>
      </div>

      <!-- 对话列表区域 -->
      <div class="container">
        <!-- 无对话时显示提示 -->
        <div v-if="conversationStore.conversations.length === 0" class="empty-state">
          <span>暂无对话记录</span>
        </div>

        <!-- 对话列表项 -->
        <div
          v-for="chat in conversationStore.conversations"
          :key="chat.id"
          class="item"
          :class="{ 'active': conversationStore.selectedConversationId === chat.id }"
          @click="conversationStore.selectConversation(chat.id)"
        >
          <!-- 编辑状态 -->
          <input
            v-if="editingChatId === chat.id"
            ref="editInput"
            v-model="editingTitle"
            class="edit-title-input"
            @blur="saveTitle"
            @keyup.enter="saveTitle"
            @keyup.esc="cancelEdit"
          />
          <!-- 普通状态 -->
          <span v-else class="title">{{ chat.title }}</span>

          <!-- 操作按钮 -->
          <div class="item-actions">
            <button class="action-btn rename-btn" @click.stop="startEdit(chat)" title="重命名">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="action-icon">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
            </button>
            <button class="action-btn delete-btn" @click.stop="confirmDelete(chat.id)" title="删除">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="action-icon">
                <path d="M3 6h18"></path>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"></path>
                <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
            </button>
          </div>
        </div>
      <div class="deleteall" @click="deleteall()">
        全部删除
      </div>
      </div>
    </div>
  </div>

  <!-- 侧边栏切换按钮 -->
  <button class="collapse-btn" @click="toggleCollapse" :style="{ left: isCollapsed ? '0.5rem' : 'calc(300px + 0.5rem)' }">
    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" class="collapse-icon" :class="{ 'rotated': isCollapsed }">
      <rect x="3" y="6" width="18" height="2" rx="1" fill="currentColor" />
      <rect x="3" y="11" width="18" height="2" rx="1" fill="currentColor" />
      <rect x="3" y="16" width="18" height="2" rx="1" fill="currentColor" />
    </svg>
  </button>
</div>
</template>

<script setup lang="ts">
import { ref, nextTick, h, onMounted } from 'vue';
import { useConversationStore, useUserConfig ,useSystemConfig} from "@/store/dataconfig.ts";
import type { ChatItem } from '@/interface';
import { message, Modal } from 'ant-design-vue';
import emitter from "@/utils/mitt";
import axios from "axios"

// 全局状态和用户配置
const conversationStore = useConversationStore();
const userStore = useUserConfig();
const messageApi = message;
const SystemConfig = useSystemConfig()

// 状态管理
const editingChatId = ref<string | null>(null);
const editingTitle = ref('');
const editInput = ref<HTMLInputElement | null>(null);
const isCollapsed = ref(localStorage.getItem('sidebarCollapsed') === 'true');
const token = localStorage.getItem('JWTtoken')

const deleteall = async () => {
  Modal.confirm({
    title: '确认删除',
    content: h('div', { style: 'color:red;' }, '确定要删除所有对话吗？删除后无法恢复。'),
    okText: '删除',
    okType: 'danger',
    cancelText: '取消',
    onOk() {
      conversationStore.conversations = []
      conversationStore.selectedConversationId = null
      if(userStore.isLoggedIn){
        const response = axios.post(SystemConfig.baseurl+'/chat/Deleteall',{
        username:userStore.userinfo.username
      },
      {
        headers: { 
              'Content-Type': 'application/json', 
              Authorization: `Bearer ${token}` 
            }
        })

    }
       messageApi.success('已删除全部对话')
}});
}

emitter.on('closeLside',(isClose: any)=>{
  isCollapsed.value = isClose;
})

// 开始编辑对话标题
const startEdit = (chat: ChatItem) => {
  editingChatId.value = chat.id;
  editingTitle.value = chat.title;
  nextTick(() => {
    if (editInput.value) {
      editInput.value.focus();
    }
  });
};

// 保存编辑后的标题
const saveTitle = () => {
  if (!editingChatId.value) return;
  conversationStore.updateConversationTitle(editingChatId.value, editingTitle.value);
  editingChatId.value = null;
};

// 取消编辑
const cancelEdit = () => {
  editingChatId.value = null;
};

// 确认删除对话
const confirmDelete = (chatId: string) => {
  Modal.confirm({
    title: '确认删除',
    content: '确定要删除这个对话吗？删除后无法恢复。',
    okText: '删除',
    okType: 'danger',
    cancelText: '取消',
    onOk() {
      conversationStore.deleteConversation(chatId);
      messageApi.success('对话已删除');
    }
  });
};

// 切换侧边栏显示状态
const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
  localStorage.setItem('sidebarCollapsed', isCollapsed.value.toString());
};
</script>

<style scoped>
:root {
  --dad:rgba(255, 255, 255, 0.84);
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  --primary-color: #4a9eff;
  --delete-color: #ff4757;
  --bg-dark: #1a1a22;
  --bg-darker: #13131a;
  --item-bg: rgba(28, 28, 36, 0.8);
  --item-hover: rgba(74, 158, 255, 0.1);
  --active-bg: rgba(74, 158, 255, 0.15);
  --border-color: rgba(0, 162, 255, 0.15);
  --text-color: rgba(255, 255, 255, 0.95);
  --text-secondary: rgba(255, 255, 255, 0.7);
  --text-tertiary: rgba(255, 255, 255, 0.5);
}

[data-theme="light"] {
  --bg-dark: #f0f0f4;
  --bg-darker: #e8e8ec;
  --item-bg: rgba(255, 255, 255, 0.8);
  --item-hover: rgba(74, 158, 255, 0.1);
  --active-bg: rgba(74, 158, 255, 0.1);
  --border-color: rgba(74, 158, 255, 0.2);
  --text-color: rgba(0, 0, 0, 0.85);
  --text-secondary: rgba(0, 0, 0, 0.65);
  --text-tertiary: rgba(0, 0, 0, 0.45);
}

.chat_input {
  z-index: 10;
  height: 100%;
}

.sidebar-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 300px;
  height: 100%;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateX(0);
  background: linear-gradient(135deg, var(--bg-dark), var(--bg-darker));
  backdrop-filter: blur(20px);
  border-radius: 0 16px 16px 0;
  box-shadow: 5px 0 30px rgba(0, 0, 0, 0.2);
  z-index: 20;
  overflow: hidden;
  border-right: 1px solid var(--border-color);
}

.sidebar-wrapper-hidden {
  position: absolute;
  top: 0;
  left: 0;
  width: 300px;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateX(-110%);
  z-index: 20;
}

.sidebar {
  height: 100%;
  width: 100%;
  display: grid;
  grid-template-rows: auto 1fr;
  padding-top: 1rem;
}

.sidebar-top {
  padding: 0.8rem 1.5rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 1.2rem;
  position: relative;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.sidebar-top::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 10%;
  width: 80%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--primary-color), transparent);
  filter: blur(1px);
  opacity: 0.5;
}

.history {
  font-size: 1.5rem;
  color: var(--primary-color);
  font-weight: 600;
}

.new-chat-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  padding: 0.8rem;
  background: linear-gradient(135deg, #4a9eff, #2d7bd3);
  color: #fff;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  letter-spacing: 0.05em;
  transition: all 0.3s ease;
}

.new-chat-btn:hover {
  background: linear-gradient(135deg, #2d7bd3, #1a5ca8);
  transform: translateY(-2px);
}

.new-chat-btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.plus-icon {
  width: 18px;
  height: 18px;
  stroke: currentColor;
  transition: transform 0.5s ease;
}

.container {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow-y: auto;
  padding: 0.7rem 1.2rem;
  gap: 0.9rem;
  max-height: calc(100vh - 230px);
  margin-bottom: 70px;
  scrollbar-width: thin;
}

.container::-webkit-scrollbar {
  width: 4px;
}

.container::-webkit-scrollbar-thumb {
  background-color: var(--primary-color);
  border-radius: 4px;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  color: var(--text-secondary);
  text-align: center;
  font-style: italic;
  background: rgba(128, 128, 128, 0.05);
  border-radius: 12px;
  border: 1px dashed var(--border-color);
  margin: 2rem 0;
}

.item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  cursor: pointer;
  transition: var(--transition);
  background-color: var(--item-bg);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.item:hover {
  background-color: var(--item-hover);
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(74, 158, 255, 0.25);
  border-color: var(--primary-color);
}

.item.active {
  background: linear-gradient(135deg, rgba(74, 158, 255, 0.15), rgba(74, 158, 255, 0.05));
  border: 1px solid var(--primary-color);
  border-left: 4px solid var(--primary-color);
  box-shadow: 0 5px 15px rgba(74, 158, 255, 0.3);
}

.title {
  color: var(--text-color);
  font-size: 1.05rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 75%;
}

.item.active .title {
  color: var(--primary-color);
}

.edit-title-input {
  background:linear-gradient(45deg,rgba(212, 0, 255,0.8),rgba(0, 195, 255,0.8));
  border: 1px solid var(--border-color);
  color: var(--text-color);
  font-size: 1rem;
  padding: 0.5rem 0.7rem;
  width: 75%;
  outline: 3px solid rgb(255, 255, 255);
  border-radius: 6px;
}

.item-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.item:hover .item-actions {
  opacity: 1;
}

.action-btn {
  background: rgba(74, 158, 255, 0.1);
  border: none;
  padding: 6px;
  cursor: pointer;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-color);
  transition: var(--transition);
}

.action-btn:hover {
  transform: scale(1.15);
}

.rename-btn {
  background: rgba(74, 158, 255, 0.1);
  color: var(--primary-color);
}

.rename-btn:hover {
  background: rgba(74, 158, 255, 0.2);
  color: var(--primary-color);
}

.delete-btn {
  background: rgba(255, 71, 87, 0.1);
  color: var(--delete-color);
}

.delete-btn:hover {
  background: rgba(255, 71, 87, 0.2);
  color: var(--delete-color);
}

.action-icon {
  width: 16px;
  height: 16px;
}

.deleteall {
  position: fixed;
  bottom: 6px;
  left: 50%;
  transform: translateX(-50%);
  padding: 0.5rem 1rem;
  width: 80%;
  background: linear-gradient(135deg, #ff4757, #ff6a6a);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  text-align: center;
  box-shadow: 0 6px 16px rgba(255, 71, 87, 0.3);
  transition: all 0.3s ease;
}

.deleteall:hover {
  background: linear-gradient(135deg, #ff6a6a, #ff4757);
  transform: translateX(-50%) translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 71, 87, 0.4);
}

.collapse-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  background: var(--bg-dark);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 30;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.collapse-btn:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  transform: translateY(-50%) scale(1.05);
  border-color: var(--primary-color);
}

.collapse-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.4s ease;
  color: var(--text-color);
}

.collapse-icon.rotated {
  transform: rotate(90deg);
}
</style>

