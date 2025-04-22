//每一个聊天
export interface ChatItem {
  id: string
  title: string
  createdAt: Date
  chatmessages: ChatMessage[]
}

//每一个对话记录
export interface ChatMessage {
  id: string  // 唯一标识符
  isuser: boolean
  content: string
}

export interface ApiRequest {
  message: string
  image_url?: string[]
}

// API接口
export interface ApiItem {
  id?: number;
  api_name: string;
  api_url: string;
  api_key: string;
}
export interface ModelOption {
  model_id: string;
  model_owned_by: string;
}