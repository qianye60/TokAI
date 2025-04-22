// 功能列表：
// useSystemConfig - 系统配置存储;
// useConversationStore - 对话管理存储
  // -  selectConversation - 选择对话,
  // -  addMessage - 添加消息,
  // -  createNewConversation - 创建对话,
  // -  deleteConversation - 删除对话,
  // -  updateConversationTitle - 更新标题;
// useModelConfig - AI模型配置存储;
//  useUserConfig - 用户配置存储

// store/dataconfig.ts
import { defineStore } from "pinia"
import { ref, computed ,reactive} from "vue"
import type { ChatItem, ChatMessage } from "@/interface" // 导入聊天相关的类型定义
import { nanoid } from "nanoid"
import axios from "axios"

// 系统配置存储，用于存储全局系统配置
export const useSystemConfig = defineStore(
  "systemConfig",
  () => {
    const theme = ref(false)
    const baseurl = ref("") // API 基础URL/后端 - 在Docker环境中通过Nginx代理
    const message_max = ref(8);
    const title = ref("")
    const emailregister = ref(false);
    const model_name = ref("gpt-3.5-turbo")
    const api_name = ref("newapi")
    return {baseurl,message_max,theme,title,emailregister,model_name,api_name}
  },
  {
      persist: {
        key: "SystemConfig",
        storage: localStorage,
        pick: ["title","emailregister","message_max",'theme','model_name','api_name'],
      },
  }
)

// 对话管理存储，用于管理对话数据、当前选中的对话以及相关操作
export const useConversationStore = defineStore(
  "conversationStore",
  () => {
    // 基础状态
    const conversations = ref<ChatItem[]>([]) // 所有对话记录
    const selectedConversationId = ref<string | null>(null) // 当前选中的对话ID

    //函数调用数据
    const token = localStorage.getItem('JWTtoken')
    const SystemConfig = useSystemConfig()
    const userStore = useUserConfig()


    // 计算属性
    // 获取当前选中的对话对象
    const currentConversation = computed(() => {
      if (!selectedConversationId.value) return null
      return conversations.value.find((chat) => chat.id === selectedConversationId.value) || null
    })

    // 获取当前选中对话的消息列表
    const currentMessages = computed(() => {
      if (!selectedConversationId.value) return []
      const chat = conversations.value.find((chat) => chat.id === selectedConversationId.value)
      return chat ? chat.chatmessages : []
    })

    // 查找消息
    const findMessage = (messageId: string) => {
      if (!selectedConversationId.value) return null

      const convIndex = conversations.value.findIndex(
        chat => chat.id === selectedConversationId.value
      )

      if (convIndex === -1) return null

      const msgIndex = conversations.value[convIndex].chatmessages.findIndex(
        msg => msg.id === messageId
      )

      return msgIndex !== -1 ? { convIndex, msgIndex } : null
    }

    // 更新消息内容
    const updateMessage = (messageId: string, content: string, append = false) => {
      const found = findMessage(messageId)
      if (!found) return console.log("消息未找到")

      const { convIndex, msgIndex } = found
      const currentContent = conversations.value[convIndex].chatmessages[msgIndex].content
      conversations.value[convIndex].chatmessages[msgIndex].content = append ? currentContent + content : content
    }

    // 操作方法
    // 选择一个对话
    const selectConversation = (conversationId: string) => {
      selectedConversationId.value = conversationId
    }

    // 向当前选中的对话添加一条消息
    const addMessage = async (message: ChatMessage) => {
      try {
        // 如果没有选中的对话，先创建一个新对话
        if (!selectedConversationId.value) {
          await createNewConversation();
          if (!selectedConversationId.value) return;
        }

        // 确保消息有唯一ID
        if (!message.id) {
          message = { ...message, id: nanoid() }
        }

        // 确保 conversations.value 是一个数组
        if (!Array.isArray(conversations.value)) {
          conversations.value = [];
        }

        const chatIndex = conversations.value.findIndex((chat) => chat.id === selectedConversationId.value)
        if (chatIndex === -1) {
          // 如果找不到对话，创建一个新的对话
          const newChat: ChatItem = {
            id: selectedConversationId.value,
            title: `新对话 ${conversations.value.length + 1}`,
            createdAt: new Date(),
            chatmessages: [message]
          }
        } else {
          // 确保 chatmessages 是一个数组
          if (!Array.isArray(conversations.value[chatIndex].chatmessages)) {
            conversations.value[chatIndex].chatmessages = [];
          }
          // 直接更新数组中的对象
          conversations.value[chatIndex].chatmessages.push(message)
        }
      } catch (error) {
        console.error('添加消息失败:', error);
        throw error;
      }
    }

    // 创建新对话
    const createNewConversation = async () => {
      const token = localStorage.getItem('JWTtoken')
      const newChat: ChatItem = {
        id: nanoid(),
        title: `新对话 ${conversations.value.length + 1}`,
        createdAt: new Date(),
        chatmessages: []
      }

      if(userStore.isLoggedIn){
        try {
          const response = await axios.post(
            SystemConfig.baseurl + '/chat/Createchat',
          {
            username:userStore.userinfo.username,
            title: newChat.title,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )
          newChat.id = response.data.chat_id
        } catch (error) {
          console.error('创建对话失败:', error)
        }
      }
      selectConversation(newChat.id)
      conversations.value.push(newChat)
      return newChat
    }

    // 删除对话
    const deleteConversation = async (conversationId: string) => {
      const token = localStorage.getItem('JWTtoken')
      conversations.value = conversations.value.filter(chat => chat.id !== conversationId)

      if(userStore.isLoggedIn){
        try {
          const response = await axios.post(
            SystemConfig.baseurl + '/chat/Deletechat',
            {
              username:userStore.userinfo.username,
              user_id: userStore.userinfo.userID,
              conversationId: conversationId,
            },
            {
              headers: {
                Authorization: `Bearer ${token}`
              }
            }
          )
        } catch (error) {
          console.error('删除对话失败:', error)
        }
      }

      // 如果删除的是当前选中的对话，选择新的对话
      if (selectedConversationId.value === conversationId) {
        if (conversations.value.length > 0) {
          selectConversation(conversations.value[0].id)
        } else {
          selectedConversationId.value = null
        }
      }
    }
    // 更新对话标题
    const updateConversationTitle = async (conversationId: string, newTitle: string) => {
      const token = localStorage.getItem('JWTtoken')
      const chatIndex = conversations.value.findIndex(chat => chat.id === conversationId)
      if (chatIndex === -1) return

      // 确保标题不为空
      const title = newTitle.trim() === '' ? `新对话 ${chatIndex + 1}` : newTitle

      const updatedChat = { ...conversations.value[chatIndex], title }
      const newChatList = [...conversations.value]
      newChatList[chatIndex] = updatedChat
      conversations.value = newChatList
      //更新到数据库
      try{
        const response = await axios.post(SystemConfig.baseurl+'/chat/Updatechat',{
          username:userStore.userinfo.username,
          conversationId:conversationId,
          newtitle:newTitle
        },
        {
          headers:{
            Authorization:`Bearer ${token}`
          }
        }
      )
      }
      catch(erroe){
      }
    }
    // 返回所有状态和方法
    return {
      conversations,
      selectedConversationId,
      currentConversation,
      currentMessages,
      findMessage,
      updateMessage,
      selectConversation,
      addMessage,
      createNewConversation,
      deleteConversation,
      updateConversationTitle,
    }
  },
  {
    persist: {
      key: "ConversationStore",
      storage: localStorage,
      pick: ["conversations", "selectedConversationId"],
    },
  }
)

// AI模型配置存储，用于管理AI模型相关的配置
export const useModelConfig = defineStore(
  "modelConfig",
  () => {
    const currentModel = ref("gpt-3.5") // 当前使用的模型
    const temperature = ref(0.7) // 模型温度参数

    return { currentModel, temperature }
  },
  {
    persist: {
      key: "ModelConfig",
      storage: localStorage,
    },
  }
)

// 用户配置存储，用于管理用户相关的信息
export const useUserConfig = defineStore(
  "userConfig",
  () => {
    const userinfo = reactive({
        userID : 0, // 用户ID
        username : "user", // 用户名
        email : "", // 用户邮箱
        money : 0, // 用户余额
        userauth : 0, //0 用户 1 管理员 2超级管理员
    })
    const isLoggedIn = ref(false); // 用户登录状态
    // 设置登录状态
    const setLoginStatus = (status: boolean) => {
      isLoggedIn.value = status;
    };


    return {
      isLoggedIn,
      userinfo,
      setLoginStatus,
    }
  },
  {
    persist: {
      key: "UserConfig",
      storage: localStorage,
    },
  }
)
