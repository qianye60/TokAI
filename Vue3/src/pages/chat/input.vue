<template>
<div>
<contextHolder />
<div ref="divRef" class="chatstyle">
  <div v-if="fileList.length > 0" class="list-file">
    <ul class="file-list-container">
      <!-- 使用 file.uid 作为 key -->
      <li class="file-item" v-for="file in fileList" :key="file.uid" :class="{ 'file-error': file.status === 'error' }">
        <div class="file-area">
          <span class="file-name">{{ file.name }}</span>
          <span v-if="file.status === 'uploading'" class="file-status">上传中...</span>
          <span v-else-if="file.status === 'done'" class="file-status success">已上传</span>
          <span v-else-if="file.status === 'error'" class="file-status error">上传失败</span>
        </div>
        <!-- 将 file.uid 传递给 del_file -->
        <button class="del" @click="del_file(file.uid)" :disabled="file.status === 'uploading'">
          <svg t="1742615473763" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2313" width="16" height="16"><path d="M512 883.2A371.2 371.2 0 1 0 140.8 512 371.2 371.2 0 0 0 512 883.2z m0 64a435.2 435.2 0 1 1 435.2-435.2 435.2 435.2 0 0 1-435.2 435.2z" fill="#5A5A68" p-id="2314"></path><path d="M557.056 512l122.368 122.368a31.744 31.744 0 1 1-45.056 45.056L512 557.056l-122.368 122.368a31.744 31.744 0 1 1-45.056-45.056L466.944 512 344.576 389.632a31.744 31.744 0 1 1 45.056-45.056L512 466.944l122.368-122.368a31.744 31.744 0 1 1 45.056 45.056z" fill="#5A5A68" p-id="2315"></path></svg>
        </button>
      </li>
    </ul>
  </div>
  <Flex vertical gap="middle" class="finput">
    <Sender 
      :style="{
        backgroundColor: '#F8F8FF !important', 
      }"
      :prefix="attachmentsNode" 
      v-model:value="inputvalue" 
      class="input" 
      @submit="sendmes"
      placeholder="在这里输入您的消息..."
    />
  </Flex>
</div></div>
</template>

<script setup lang="ts">
import { CloudUploadOutlined, FontColorsOutlined, LinkOutlined } from '@ant-design/icons-vue';
import { message, Button, Flex, Switch, type UploadFile } from 'ant-design-vue';
import { Attachments, Sender } from 'ant-design-x-vue';
import { computed, h, ref, onMounted, nextTick } from 'vue';
import axios from "axios";
import { useConversationStore, useSystemConfig } from "@/store/dataconfig.ts";
import { useUserConfig } from "@/store/dataconfig.ts";
import type { ChatMessage } from '@/interface';
import { nanoid } from 'nanoid';
import { text } from 'stream/consumers';

// 使用Pinia存储
const chatStore = useConversationStore();
const systemStore = useSystemConfig();
const userStore = useUserConfig();

const fullScreenDrop = ref(true); // 是否全屏拖拽 (默认为 true)
const divRef = ref<HTMLDivElement>(); // 用于获取 div 元素的引用
const [messageApi, contextHolder] = message.useMessage(); // 用于显示消息提示
const fileList = ref<UploadFile[]>([]); // 文件列表
const uploading = ref(false); // 添加上传状态标记
const baseurl = systemStore.baseurl;
const inputvalue = ref(''); // 输入框的值
const filelist_id = ref<string[]>([]);

const token = localStorage.getItem('JWTtoken')

// 获取拖拽容器的函数
const getDropContainer = () => (fullScreenDrop.value ? document.body : divRef.value);

const handleChange = async ({ file }: { file: UploadFile }) => {
  // 检查文件是否已存在
  if (fileList.value.some(existingFile => existingFile.name === file.name && existingFile.size === file.size)) {
    return;
  }
  
  if (!file.originFileObj) {
    messageApi.error('文件对象无效');
    return;
  }
  
  fileList.value.push({
    ...file,
    status: 'uploading'
  });

  try {
    const formData = new FormData();
    formData.append('files', file.originFileObj);

    const res = await axios({
      url: baseurl + '/upfile/chatfile',
      method: 'POST',
      headers: { 'Content-Type': 'multipart/form-data' },
      data: formData,
      timeout: 30000
    });

    const updatedFileIndex = fileList.value.findIndex(f => f.uid === file.uid);
    if (updatedFileIndex >= 0) {
      fileList.value[updatedFileIndex].status = 'done';
      if (res.status === 200) {
        messageApi.success('文件上传成功');
        filelist_id.value.push(res.data['id']);
      }
    }
  } catch (error) {
    console.error('上传错误:', error);
    
    if (axios.isAxiosError(error)) {
      if (error.code === 'ERR_NETWORK') {
        messageApi.error('网络错误: 请检查服务器是否运行');
      } else if (error.response) {
        messageApi.error(`服务器错误: ${error.response.status} ${error.response.statusText}`);
      } else {
        messageApi.error(`未知错误: ${error.message}`);
      }
    } else {
      messageApi.error('上传过程中发生未知错误');
    }

    const errorFileIndex = fileList.value.findIndex(f => f.uid === file.uid);
    if (errorFileIndex >= 0) {
      fileList.value[errorFileIndex].status = 'error';
    }
  } finally {
    uploading.value = false;
  }
};

// 实现发送消息功能
const sendmes = async (message: string) => {
  const messageContent = message.trim();
  inputvalue.value = '';
  
  if (!messageContent) {
    messageApi.error('空消息');
    return;
  }

  // 获取历史消息
  const messages = chatStore.currentConversation?.chatmessages || [];
  const max = systemStore.message_max;
  // 如果消息数量大于 max-1，则取最后 max-1 条消息（因为还要加上当前新消息）
  // 同时过滤掉content为空的消息
  const history_message = messages.length > (max - 1) ? 
    messages.slice(messages.length - (max - 1)).filter(msg => msg.content.trim() !== '') : 
    messages.filter(msg => msg.content.trim() !== '');

  // 创建用户消息
  const userMessage: ChatMessage = {
    id: nanoid(),
    isuser: true,
    content: messageContent,
  };

  // 同步消息到服务器
  if (userStore.isLoggedIn) {
    try {
      const response_user = await axios.post(systemStore.baseurl + '/message/Createmessage', {
        username: userStore.userinfo.username,
        message: String(userMessage.content),
        isuser: Boolean(userMessage.isuser),
        conversationId: String(chatStore.selectedConversationId),
        filelist_id: filelist_id.value
      }, {
        headers: { 
          'Content-Type': 'application/json', 
          Authorization: `Bearer ${localStorage.getItem('JWTtoken')}` 
        }
      });
      userMessage.id = response_user.data.message_id;
    } catch (error) {
      console.error('同步消息失败:', error);
    }
  }

  // 添加用户消息
  await chatStore.addMessage(userMessage);

  // 添加文件信息到用户消息
  for(let i = 0; i < fileList.value.length; i++){
    chatStore.updateMessage(userMessage.id,"\n`"+fileList.value[i].name+"`",true);
  }

  // 创建AI回复消息
  const aiMessage: ChatMessage = {
    id: nanoid(),
    isuser: false,
    content: "",
  };
  
  // 添加AI消息
  await chatStore.addMessage(aiMessage);

  try {
    const response = await fetch(baseurl + '/api/chat', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        username: userStore.userinfo.username,
        model_name: systemStore.model_name,
        api_name: systemStore.api_name,
        history_message: history_message,
        message: messageContent,
        filelist_id: filelist_id.value || []
      })
    });

    // 清空文件列表
    fileList.value = [];
    filelist_id.value = [];

    if (!response.ok) throw new Error(`HTTP错误: ${response.status}`);
    
    const reader = response.body?.getReader();
    if (!reader) throw new Error('无法获取响应流');

    const decoder = new TextDecoder()
    
    let fullContent = '';
    
    while (true) {

      const { value, done } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value, { stream: true });
      for (const line of chunk.split('\n')) {
        if (!line.trim()) continue;
        try {
          const data = JSON.parse(line);
          if (data.error) {
            throw new Error(data.error);
          }
          if (data.content) {
            fullContent += data.content;
            chatStore.updateMessage(aiMessage.id, data.content, true);
          }
        } catch(error) {
          if (error instanceof Error) {
            chatStore.updateMessage(aiMessage.id, "请求失败: " + (error.message || "未知错误"));
          }
        }
      }
    }
  
  const found = chatStore.findMessage(aiMessage.id)
  if (!found) return;
  // 同步消息到服务器
  if (userStore.isLoggedIn) {
    try {
      const response_user = await axios.post(systemStore.baseurl + '/message/Createmessage', {
        username: userStore.userinfo.username,
        message: chatStore.conversations[found.convIndex].chatmessages[found.msgIndex].content,
        isuser: chatStore.conversations[found.convIndex].chatmessages[found.msgIndex].isuser,
        conversationId: chatStore.selectedConversationId
      }, {
        headers: { 
          'Content-Type': 'application/json', 
          Authorization: `Bearer ${token}` 
        }
      });
      chatStore.conversations[found.convIndex].chatmessages[found.msgIndex].id = response_user.data.message_id;
    } catch (error) {
      console.error('同步消息失败:', error);
    }
  }
  } catch (error: any) {
    console.error("错误:", error);
    chatStore.updateMessage(aiMessage.id, "请求失败: " + (error.message || "未知错误"));
  }
};

// 设置输入框的值
const setInputValue = (text: string) => {
  inputvalue.value = text;
};

// 获取输入框的值
const getInputValue = () => {
  return inputvalue.value;
};

// 临时保存确认按钮引用
let confirmButtonRef: HTMLButtonElement | null = null;

// 添加确认编辑按钮
const addConfirmButton = (text: string, callback: () => void) => {
  // 如果已经存在确认按钮，先移除
  removeConfirmButton();
  
  // 创建确认按钮
  const button = document.createElement('button');
  button.textContent = text;
  button.className = 'confirm-edit-button';
  button.onclick = () => {
    callback();
    removeConfirmButton(); // 点击后自动移除
  };
  
  // 添加到输入区域旁边
  const inputArea = divRef.value?.querySelector('.finput');
  if (inputArea) {
    inputArea.appendChild(button);
    confirmButtonRef = button;
  }
};

// 移除确认编辑按钮
const removeConfirmButton = () => {
  if (confirmButtonRef) {
    confirmButtonRef.remove();
    confirmButtonRef = null;
  }
};

// 导出函数，使其可以在父组件中使用
defineExpose({
  setInputValue,
  getInputValue,
  addConfirmButton,
  removeConfirmButton
});

//删除文件的函数
function del_file(uid: string) {
  // 找到要删除文件的索引
  const index = fileList.value.findIndex(file => file.uid === uid);
  if (index > -1) {
    // 检查是否正在上传
    if (fileList.value[index].status === 'uploading') {
      messageApi.warning('文件正在上传中，无法删除');
      return;
    }

    // 从数组中移除该文件
    fileList.value.splice(index, 1);
    messageApi.success('文件已成功删除');
  }
}

// 修正后的 Attachments 配置
const attachmentsNode = computed(() => h(Attachments, {
 multiple: true,
 directory: false,
 fileList: fileList.value,
 onChange: handleChange,
 disabled: uploading.value, // 上传中禁用
 placeholder:()=>{ return{       // 正确的对象形式
   icon: h(CloudUploadOutlined),
   title: '拖拽文件到这里',
   description: '支持任意文件类型'
 }},
 children: h(Button, {
   type: 'text',
   icon: h(LinkOutlined),
   disabled: uploading.value // 上传中禁用
 }),
 getDropContainer,
}));
</script>

<style scoped>
.del{
 border: 0;
 background: none;
 cursor: pointer;
 color: rgba(255, 100, 100, 0.8);
 transition: all 0.3s ease;
}
.del:hover{
 transform: scale(1.5);
 color: #ff4d4f;
}
.del:disabled {
 opacity: 0.5;
 cursor: not-allowed;
}

.list-file {
 position: absolute;
 bottom: 100%;
 left: 0;
 height: auto;
 width: 60vw;
 max-height: 150px;
 overflow-x: auto;
 overflow-y: auto;
 white-space: nowrap;
 margin-bottom: 10px;
 scrollbar-width: thin;
 scrollbar-color: rgba(155, 155, 155, 0.5) transparent;
 z-index: 10;
}

.list-file::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

.list-file::-webkit-scrollbar-track {
  background: transparent;
}

.list-file::-webkit-scrollbar-thumb {
  background-color: rgba(155, 155, 155, 0.5);
  border-radius: 10px;
}

.file-list-container {
 display: flex;
 padding: 0;
 list-style: none;
}

.file-item {
 display: flex;
 list-style: none;
 padding: 0.8rem 1rem;
 border-radius: 10px;
 border: 2px solid rgba(45, 140, 240, 0.8);
 min-width: max-content;
 margin-right: 1rem;
 align-items: center;
 justify-content: space-between;
 background-color: rgba(45, 140, 240, 0.1);
 backdrop-filter: blur(4px);
 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
 transition: all 0.3s ease;
}

.file-error {
 border-color: rgba(255, 77, 79, 0.8);
 background-color: rgba(255, 77, 79, 0.1);
}

.file-item:hover {
 transform: translateY(-3px);
 box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.icon:hover {
 border-radius: 50%;
}

.file-area {
 display: flex;
 align-items: center;
 gap: 0.5rem;
 white-space: nowrap;
}

.file-name {
 max-width: 6rem;
 overflow: hidden;
 text-overflow: ellipsis;
 font-weight: 500;
}

.file-status {
 font-size: 0.8rem;
 color: #2d8cf0;
 font-style: italic;
}

.file-status.success {
 color: #52c41a;
}

.file-status.error {
 color: #ff4d4f;
}

.finput {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: auto;
}
.input{
  position:relative;
}
/* IMPORTANT: 固定样式 */
.ant-design-x-sender {
  width: 80% !important;
  max-width: 1200px !important;
  background: #ffffff !important;
  background-color: #ffffff !important;
  border: 1px solid rgba(97, 175, 254, 0.3) !important;
  border-radius: 12px !important;
  transition: all 0.3s ease !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
  color: #333333 !important;
}

.ant-design-x-sender * {
  background-color: #ffffff !important;
}

.ant-design-x-sender:hover {
  border-color: rgba(24, 144, 255, 0.5) !important;
  box-shadow: 0 6px 20px rgba(24, 144, 255, 0.2) !important;
  transform: translateY(-2px) !important;
  background: #ffffff !important;
}

.ant-design-x-sender-textarea {
  background: #ffffff !important;
  color: #333333 !important;
  font-size: 0.95rem !important;
  padding: 0.8rem !important;
}

.ant-design-x-sender-textarea::placeholder {
  color: rgba(0, 0, 0, 0.4) !important;
}

/* 深色模式适配 - 输入框保持白色 */
[data-theme="dark"] .ant-design-x-sender {
  background: #ffffff !important;
  background-color: #ffffff !important;
  border-color: rgba(97, 175, 254, 0.3) !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
  color: #333333 !important;
}

[data-theme="dark"] .ant-design-x-sender * {
  background-color: #ffffff !important;
}

[data-theme="dark"] .ant-design-x-sender-textarea {
  background: #ffffff !important;
  color: #333333 !important;
}

[data-theme="dark"] .ant-design-x-sender-textarea::placeholder {
  color: rgba(0, 0, 0, 0.4) !important;
}

[data-theme="dark"] .ant-design-x-sender:hover {
  border-color: rgba(24, 144, 255, 0.5) !important;
  background: #ffffff !important;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4) !important;
}

/* 电脑端样式 */
.chatstyle {
 max-width: 1200px;
 margin: 0 auto;
 padding: 10px 0 10px 0;
 height: auto;
 width: 60vw;
 position: relative;
 background-color: rgba(0, 0, 0, 0);

}

/* 手机端样式 */
@media screen and (max-width: 768px) {
 .chatstyle {
   width: 90vw;
   max-width: 100%;
   margin: 0;
   padding: 10px;
 }
 .list-file {
   width: 90vw;
 }
 .file-name {
   max-width: 100px;
 }
}

/* 确认编辑按钮样式 */
.confirm-edit-button {
  margin-left: 10px;
  padding: 8px 15px;
  background: linear-gradient(90deg, #3498db, #2980b9);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.confirm-edit-button:hover {
  background: linear-gradient(90deg, #2980b9, #3498db);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

/* 暗黑模式适配 */
[data-theme="dark"] .confirm-edit-button {
  background: linear-gradient(90deg, #1890ff, #096dd9);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}
</style>
