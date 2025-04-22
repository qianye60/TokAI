<template>
  <div class="api-management-page">
    <!-- 页面标题 -->
    <div class="admin-header">
      <h2 class="admin-title">API 管理</h2>
      <button class="btn-primary" @click="showAddApiDialog = true">
        <span class="btn-icon">+</span> 添加 API
      </button>
    </div>

    <!-- API 列表 -->
    <div class="api-list-container">
      <div v-if="api.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect>
            <line x1="7" y1="2" x2="7" y2="22"></line>
            <line x1="17" y1="2" x2="17" y2="22"></line>
            <line x1="2" y1="12" x2="22" y2="12"></line>
            <line x1="2" y1="7" x2="7" y2="7"></line>
            <line x1="2" y1="17" x2="7" y2="17"></line>
            <line x1="17" y1="17" x2="22" y2="17"></line>
            <line x1="17" y1="7" x2="22" y2="7"></line>
          </svg>
        </div>
        <h3>未配置任何API</h3>
        <p>点击「添加 API」按钮开始配置您的第一个API</p>
      </div>

      <div v-else class="api-grid">
        <div v-for="(apiItem, index) in api" :key="index" class="api-card">
          <div class="api-card-header">
            <div class="api-badge" :class="getApiTypeClass(apiItem.api_name)">
              {{ getApiTypeName(apiItem.api_name) }}
            </div>
            <div class="api-actions">
              <button class="icon-btn edit" @click="editApi(apiItem)" title="编辑">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                </svg>
              </button>
              <button class="icon-btn delete" @click="deleteApi(apiItem)" title="删除">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
              </button>
            </div>
          </div>

          <div class="api-card-body">
            <div class="api-detail">
              <span class="detail-label">API URL:</span>
              <span class="detail-value">{{ apiItem.api_url }}</span>
            </div>

            <div class="api-detail">
              <span class="detail-label">API Key:</span>
              <div class="key-container">
                <span class="masked-key">{{ maskApiKey(apiItem.api_key) }}</span>
                <button class="text-btn" @click="toggleShowKey(index)">
                  {{ showKeys[index] ? '隐藏' : '显示' }}
                </button>
              </div>
              <span v-if="showKeys[index]" class="full-key">{{ apiItem.api_key }}</span>
            </div>
          </div>

          <div class="api-card-footer">
            <button class="btn-secondary" @click="configureModels(apiItem)">
              配置模型
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加/编辑API对话框 -->
    <div v-if="showAddApiDialog" class="dialog-overlay" @click.self="showAddApiDialog = false">
      <div class="dialog">
        <div class="dialog-header">
          <h3>{{ isEditing ? '编辑 API' : '添加 API' }}</h3>
          <button class="close-btn" @click="showAddApiDialog = false">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div class="dialog-body">
          <form @submit.prevent="saveApi">
            <div class="form-group">
              <label for="api-type">API 类型</label>
              <select id="api-type" v-model="currentApi.api_name" class="form-control">
                <option value="newapi">NewAPI</option>
                <option value="google">Google</option>
              </select>
            </div>

            <div class="form-group">
              <label for="api-url">API URL</label>
              <input
                id="api-url"
                type="text"
                v-model="currentApi.api_url"
                placeholder="例如: https://api.openai.com/v1/chat/completions"
                class="form-control"
              />
            </div>

            <div class="form-group">
              <label for="api-key">API Key</label>
              <input
                id="api-key"
                type="text"
                v-model="currentApi.api_key"
                placeholder="输入您的API密钥"
                class="form-control"
              />
            </div>

            <div class="dialog-footer">
              <button type="button" class="btn-secondary" @click="showAddApiDialog = false">取消</button>
              <button type="submit" class="btn-primary">保存</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
  <!-- 模型配置对话框 -->
  <div v-if="isEditModel" class="dialog-overlay" @click.self="closeModelDialog">
    <div class="dialog model-dialog">
      <div class="dialog-header">
        <h3>模型：</h3>
        <button class="close-btn" @click="closeModelDialog">×</button>
      </div>

      <div class="dialog-body">
        <!-- 模型选择器 -->
        <div class="model-container">
          <!-- 已选模型区域 -->
          <div class="selected-models-area">
            <div class="model-tags">
              <div v-for="model in modelsList" :key="model.model_id" class="model-tag">
                {{ model.model_id }}
                <button @click="removeModel(model.model_id, 0)">×</button>
              </div>
              <button class="add-model-btn" @click="showModelDropdown = !showModelDropdown">
                <span>添加模型</span>
              </button>
            </div>
          </div>

          <!-- 模型选择区域 -->
          <div class="model-selection-area" v-show="showModelDropdown">
            <div class="search-box">
              <input
                v-model="modelSearchTerm"
                placeholder="搜索模型"
                @input="filterModels"
              />
              <div class="model-actions">
                <button class="action-btn select-all" @click="selectAllModels">全选</button>
                <button class="action-btn deselect-all" @click="deselectAllModels">全不选</button>
              </div>
            </div>
            <div class="model-list">
              <label v-for="model in filteredModels" :key="nanoid()" class="model-item">
                <input type="checkbox" :checked="isModelSelected(model.model_id)" @change="toggleModel(model.model_id)" />
                <span>{{ model.model_id }}</span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="dialog-footer">
        <button class="save-btn" @click="saveModels">保存</button>
        <button class="cancel-btn" @click="closeModelDialog">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue'
import axios from 'axios'
import { message } from 'ant-design-vue'
import { useSystemConfig } from '@/store/dataconfig.ts'
import { ApiItem, ModelOption } from '@/interface.ts'
import { nanoid } from 'nanoid'

const systemConfig = useSystemConfig()

// 状态管理
const api = ref<ApiItem[]>([])
const showAddApiDialog = ref(false)
const isEditing = ref(false)
const currentApi = reactive<ApiItem>({ api_name: 'newapi', api_url: '', api_key: '' })
const isEditModel = ref(false)
const currentApiForModels = ref<ApiItem>({
  api_name: '',
  api_url: '',
  api_key: ''
})

const modelsList = ref<ModelOption[]>([])
const modelsListBackup = ref<ModelOption[]>([])

const allModels = ref<ModelOption[]>([])
const filteredModels = ref<ModelOption[]>([])

const showKeys = ref<Record<number, boolean>>({})
const showModelDropdown = ref(false)
const modelSearchTerm = ref('')
const hasModelChanges = ref(false)

const selectedModelIds = ref<string[]>([])


// 获取API列表
const fetchApiList = () => {
  axios.get(`${systemConfig.baseurl}/admin/api`, {
    headers: { Authorization: `Bearer ${localStorage.getItem('JWTtoken')}` }
  })
    .then(response => {
      if (response.data && response.data.api) {
        api.value = response.data.api
      } else {
        api.value = []
      }
    })
    .catch(error => {
      console.error('获取API列表失败:', error)
      message.error('无法加载API列表')
    })
}

// 页面加载后获取API列表
onMounted(() => {
  fetchApiList()
})

// 编辑API
const editApi = (apiItem: ApiItem) => {
  isEditing.value = true
  Object.assign(currentApi, {
    id: apiItem.id,
    api_name: apiItem.api_name,
    api_url: apiItem.api_url,
    api_key: apiItem.api_key
  })
  showAddApiDialog.value = true
}

// 删除API
const deleteApi = (apiItem: ApiItem) => {
  if (!apiItem.id) {
    message.warning('无法删除该API')
    return
  }

  if (confirm(`确定要删除API"${apiItem.api_name}"吗？`)) {
    axios.delete(`${systemConfig.baseurl}/admin/api/${apiItem.id}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('JWTtoken')}` }
    })
      .then(response => {
        if (response.data && response.data.success) {
          message.success('API已删除')
          fetchApiList()
        } else {
          message.error(response.data?.error || '删除失败')
        }
      })
      .catch(error => {
        console.error('删除API失败:', error)
        message.error('删除API时出错')
      })
  }
}

// 保存API
const saveApi = () => {
  if (!currentApi.api_name || !currentApi.api_url || !currentApi.api_key) {
    message.warning('请填写所有必填字段')
    return
  }

  const method = isEditing.value ? 'put' : 'post'
  const url = `${systemConfig.baseurl}/admin/api`

  axios({
    method,
    url,
    data: currentApi,
    headers: { Authorization: `Bearer ${localStorage.getItem('JWTtoken')}` }
  })
    .then(response => {
      if (response.data && response.data.success) {
        message.success(isEditing.value ? 'API已更新' : 'API已添加')
        showAddApiDialog.value = false
        fetchApiList()
      } else {
        message.error(response.data?.error || (isEditing.value ? '更新失败' : '添加失败'))
      }
    })
    .catch(error => {
      console.error(`${isEditing.value ? '更新' : '添加'}API失败:`, error)
      message.error(`${isEditing.value ? '更新' : '添加'}API时出错`)
    })
}

// 显示/隐藏API Key
const toggleShowKey = (index: number) => {
  showKeys.value[index] = !showKeys.value[index]
}

// 马赛克API Key
const maskApiKey = (key: string) => {
  if (!key) return ''
  if (key.length <= 8) return '********'
  return key.substring(0, 4) + '...' + key.substring(key.length - 4)
}

// 获取API类型名称
const getApiTypeName = (type: string) => {
  const typeMap: Record<string, string> = {
    'newapi': 'NewAPI',
    'google': 'Google',
    'default': ''
  }
  return typeMap[type] || typeMap['default']
}

// 获取API类型样式类
const getApiTypeClass = (type: string) => {
  const classMap: Record<string, string> = {
    'newapi': 'newapi-badge',
    'google': 'google-badge',
    'default': 'default-badge'
  }
  return classMap[type] || classMap['default']
}

// 配置模型
const configureModels = (apiItem: ApiItem) => {
  currentApiForModels.value = { ...apiItem }
  modelsList.value = []
  modelsListBackup.value = []
  modelSearchTerm.value = ''
  isEditModel.value = true
  fetchApiModels(apiItem.id as number)
  showModelDropdown.value = true
  hasModelChanges.value = false
}

// 获取API关联的模型
const fetchApiModels = async (apiId: number) => {
  try {
    // 获取所有可用模型
    const response = await axios.get(`${systemConfig.baseurl}/admin/models/${apiId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('JWTtoken')}` }
    })

    if (response.data && response.data.models) {
        // 保存所有可用模型
        allModels.value = response.data.models

        // 初始化选中的模型列表
        selectedModelIds.value = response.data.select

        // 创建深拷贝作为备份
        modelsListBackup.value = JSON.parse(JSON.stringify(selectedModelIds.value))

        // 更新已选模型列表
        updateModelsList()

        // 过滤显示所有模型
        filteredModels.value = allModels.value
    } else {
        allModels.value = []
        modelsList.value = []
        selectedModelIds.value = []
        modelsListBackup.value = []
        filteredModels.value = []
    }
  } catch (error: any) {
    console.error('获取API关联模型失败:', error)
    message.error('获取API关联模型时出错')
  }
}

// 保存API相关的模型
const saveApiModels = async () => {
  try {
    await axios.put(`${systemConfig.baseurl}/admin/model`, {
      api_id: currentApiForModels.value.id,
      models: selectedModelIds.value
    },
    {
      headers: { Authorization: `Bearer ${localStorage.getItem('JWTtoken')}` }
    })
    message.success('保存成功')
    isEditModel.value = false
    fetchApiList()
  } catch (error: any) {
    message.error(error.message || '保存失败')
  }
}

// 过滤模型列表
const filterModels = () => {
  if (!modelSearchTerm.value) {
    filteredModels.value = allModels.value
    return
  }

  const searchTerm = modelSearchTerm.value.toLowerCase()
  filteredModels.value = allModels.value.filter(model =>
    model.model_id.toLowerCase().includes(searchTerm)
  )
}

// 判断模型是否已被选中
const isModelSelected = (modelId: string) => {
  return selectedModelIds.value.includes(modelId)
}

// 切换模型选中状态
const toggleModel = (modelId: string) => {
  if (isModelSelected(modelId)) {
    // 从选中列表中移除
    const index = selectedModelIds.value.indexOf(modelId)
    if (index !== -1) selectedModelIds.value.splice(index, 1)
  } else {
    // 添加到选中列表
    selectedModelIds.value.push(modelId)
  }
  // 更新模型列表
  updateModelsList()
  hasModelChanges.value = true
}

// 移除模型
const removeModel = (modelId: string, _index: number) => {
  // 从选中列表中移除
  const index = selectedModelIds.value.indexOf(modelId)
  if (index !== -1) selectedModelIds.value.splice(index, 1)
  // 更新模型列表
  updateModelsList()
  hasModelChanges.value = true
}

// 更新模型列表
const updateModelsList = () => {
  // 根据选中的ID更新modelsList
  modelsList.value = allModels.value.filter(model =>
    selectedModelIds.value.includes(model.model_id)
  )
}

// 保存模型配置
const saveModels = () => {
  saveApiModels()
  hasModelChanges.value = false
}

// 关闭模型对话框
const closeModelDialog = () => {
  if (hasModelChanges.value) {
    if (confirm('您有未保存的更改，确定要关闭吗？')) {
      // 恢复备份的模型列表
      selectedModelIds.value = JSON.parse(JSON.stringify(modelsListBackup.value))
      updateModelsList()
      isEditModel.value = false
      hasModelChanges.value = false
    }
  } else {
    isEditModel.value = false
  }
}

// 一键勾选所有模型
const selectAllModels = () => {
  // 获取当前过滤列表中的所有模型 ID
  const allModelIds = filteredModels.value.map(model => model.model_id)

  // 将所有模型 ID 添加到选中列表
  selectedModelIds.value = [...new Set([...selectedModelIds.value, ...allModelIds])]

  // 更新模型列表
  updateModelsList()
  hasModelChanges.value = true
  message.success('已选中所有模型')
}

// 一键取消选择所有模型
const deselectAllModels = () => {
  // 获取当前过滤列表中的所有模型 ID
  const allModelIds = filteredModels.value.map(model => model.model_id)

  // 从选中列表中移除这些模型 ID
  selectedModelIds.value = selectedModelIds.value.filter(id => !allModelIds.includes(id))

  // 更新模型列表
  updateModelsList()
  hasModelChanges.value = true
  message.success('已取消选择所有模型')
}
</script>





















<style scoped>
  .model-selector {
    padding: 16px;
  }
.api-management-page {
  padding-top: 24px;
  width: 100%;
  margin: 0 auto;
}

/* 页面标题 */
.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-color, #eaeaea);
}

.admin-title {
  font-size: 24px;
  color: var(--text-color, #333);
  font-weight: 600;
  margin: 0;
}

/* 按钮样式 */
.btn-primary {
  background-color: var(--primary-color, #0073ff);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: var(--primary-color-dark, #0059c2);
}

.btn-secondary {
  background-color: var(--background-color, #f3f4f6);
  color: var(--text-color, #333);
  border: 1px solid var(--border-color, #e0e0e0);
  padding: 7px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background-color: var(--text-color, #ccc);
  border-color: var(--text-color, #333);
  color: var(--background-color, #333);
}

.btn-icon {
  font-size: 16px;
  font-weight: 600;
  line-height: 1;
}

/* API列表容器 */
.api-list-container {
  margin-top: 20px;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  background-color: var(--background-light, #f9fafb);
  border-radius: 8px;
  border: 1px dashed var(--border-color, #e0e0e0);
  text-align: center;
}

.empty-icon {
  color: var(--text-muted, #9ca3af);
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 18px;
  margin: 0 0 8px 0;
  color: var(--text-color, #333);
}

.empty-state p {
  color: var(--text-muted, #6b7280);
  margin: 0;
  max-width: 400px;
}

/* API卡片网格 */
.api-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

/* API卡片 */
.api-card {
  background-color: var(--text-ground, white);
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color, #e5e7eb);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.api-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* API卡片头部 */
.api-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid var(--border-color, #f0f0f0);
}

/* API类型标识 */
.api-badge {
  display: inline-block;
  padding: 4px 12px;
  font-size: 13px;
  border-radius: 16px;
  font-weight: 500;
}

.newapi-badge {
  background-color: #e6f7ff;
  color: #0073ff;
}

.google-badge {
  background-color: #f0f4c3;
  color: #618833;
}

.default-badge {
  background-color: #f0f0f0;
  color: #666;
}

/* 操作按钮区 */
.api-actions {
  display: flex;
  gap: 8px;
}

.icon-btn {
  background: none;
  border: none;
  padding: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  color: var(--text-muted, #9ca3af);
  transition: all 0.2s;
}

.icon-btn:hover {
  background-color: var(--background-light, #f3f4f6);
}

.icon-btn.edit:hover {
  color: var(--primary-color, #0073ff);
}

.icon-btn.delete:hover {
  color: var(--danger-color, #ef4444);
}

/* API卡片内容 */
.api-card-body {
  padding: 16px;
}

.api-detail {
  margin-bottom: 16px;
}

.api-detail:last-child {
  margin-bottom: 0;
}

.detail-label {
  display: block;
  font-size: 12px;
  color: var(--text-muted, #6b7280);
  margin-bottom: 4px;
}

.detail-value {
  font-size: 14px;
  color: var(--text-color, #333);
  word-break: break-all;
}

/* API密钥显示/隐藏 */
.key-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.masked-key {
  font-family: monospace;
}

.text-btn {
  background: none;
  border: none;
  color: var(--primary-color, #0073ff);
  padding: 0;
  font-size: 13px;
  cursor: pointer;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.text-btn:hover {
  opacity: 1;
  text-decoration: underline;
}

.full-key {
  display: block;
  margin-top: 8px;
  padding: 8px;
  background-color: var(--background-light, #f9fafb);
  border-radius: 4px;
  font-family: monospace;
  font-size: 12px;
  word-break: break-all;
  border: 1px solid var(--border-color, #eee);
}

/* API卡片底部 */
.api-card-footer {
  padding: 12px 16px;
  border-top: 1px solid var(--border-color, #f0f0f0);
  text-align: right;
}

/* 对话框样式 */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog {
  position: relative;
  margin: auto;
  background: white;
  border-radius: 10px;
  width: 95%;
  max-width: 850px;
  min-height: 600px;
  overflow: hidden;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #999;
  font-size: 20px;
  padding: 5px;
  line-height: 1;
}

.close-btn:hover {
  color: #333;
}

.dialog-body {
  position: relative;
  left: 5%;
  padding: 0;
  width: 90%;
  flex: 1;
  overflow: visible;
}

/* 模型配置对话框样式 */


.dialog-header h3 {
  font-size: 16px;
  margin: 0;
  color: var(--text-color, #333);
  font-weight: 600;
}

.models-section {
  margin-bottom: 32px;
}

/* 模型选择器样式 */
.model-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.selected-models-area {
  padding: 20px;
  overflow-y: auto;
  max-height: 200px;
  border-bottom: 1px solid #eee;
}

.model-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  min-height: 50px;
  background-color: #fff;
}

.model-tag {
  display: flex;
  align-items: center;
  padding: 5px 12px;
  border-radius: 5px;
  background-color: #f5f7f9;
  border: 1px solid #eee;
  color: #333;
  font-size: 14px;
}

.model-tag button {
  border: none;
  background: none;
  color: #999;
  cursor: pointer;
  font-size: 14px;
  margin-left: 10px;
  padding: 0;
}

.model-tag button:hover {
  color: #e53e3e;
}

.add-model-btn {
  background-color: transparent;
  border: 1px dashed #ccc;
  border-radius: 5px;
  padding: 5px 12px;
  color: #666;
  cursor: pointer;
}

.add-model-btn:hover {
  border-color: #0073ff;
  color: #0073ff;
}

/* 模型选择区域 */
.model-selection-area {
  padding: 0;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  height: 400px;
}

.search-box {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.search-box input {
  width: 95%;
  padding: 10px 15px;
  border: 1px solid #eee;
  border-radius: 5px;
  font-size: 14px;
  outline: none;
}

.model-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  gap: 10px;
}

.action-btn {
  flex: 1;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  border: 1px solid #ddd;
  transition: all 0.2s;
}

.action-btn.select-all {
  background-color: #e6f7ff;
  color: #0073ff;
  border-color: #91d5ff;
}

.action-btn.select-all:hover {
  background-color: #bae7ff;
  border-color: #0073ff;
}

.action-btn.deselect-all {
  background-color: #fff1f0;
  color: #ff4d4f;
  border-color: #ffccc7;
}

.action-btn.deselect-all:hover {
  background-color: #ffd4d2;
  border-color: #ff4d4f;
}

.model-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 20px;
  max-height: 350px;
}

.model-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
}

.model-item:hover {
  background-color: #f8f8f8;
}

.model-item input {
  margin-right: 10px;
  width: 18px;
  height: 18px;
  accent-color: #0073ff;
}





.dialog-body .form-group {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.dialog-body .form-group label {
  margin-bottom: 8px;
  font-weight: 500;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--text-color, #333);
}

.dialog-body .form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 14px;
  transition: border-color 0.2s;
  display: block;
  box-sizing: border-box;
  height: 40px; /* 统一高度 */
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-color, #0073ff);
  box-shadow: 0 0 0 2px rgba(0, 115, 255, 0.2);
}

.dialog-footer {
  display: flex;
  justify-content: center;
  gap: 15px;
  padding: 20px;
  border-top: 1px solid #eee;
}

.save-btn, .cancel-btn {
  min-width: 100px;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  border: none;
  font-size: 15px;
}

.save-btn {
  background-color: #4CAF50;
  color: white;
}

.save-btn:hover {
  background-color: #45a049;
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #333;
}

.cancel-btn:hover {
  background-color: #e8e8e8;
}
</style>
