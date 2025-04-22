<template>
  <div class="mod-config-wrapper">
    <div class="section">
      <div class="section-title">功能</div>
      <div class="section-content">
        <div class="row">
          <div class="row-label">
            <span class="row-icon">
              <svg t="1744769523296" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2380" width="36" height="36"><path d="M661.333333 490.666667c-36.266667 0-64 27.733333-64 64s27.733333 64 64 64 64-27.733333 64-64-27.733333-64-64-64M362.666667 490.666667c-36.266667 0-64 27.733333-64 64s27.733333 64 64 64 64-27.733333 64-64-27.733333-64-64-64" fill="#2F3CF4" p-id="2381"></path><path d="M128 320c0-23.466667 19.2-42.666667 42.666667-42.666667h170.666666l-61.866666-155.733333c-8.533333-21.333333 2.133333-46.933333 23.466666-55.466667 21.333333-8.533333 46.933333 2.133333 55.466667 23.466667l74.666667 185.6h155.733333l74.666667-185.6c8.533333-21.333333 34.133333-32 55.466666-23.466667 21.333333 8.533333 32 34.133333 23.466667 55.466667L682.666667 277.333333h170.666666c23.466667 0 42.666667 19.2 42.666667 42.666667v597.333333c0 23.466667-19.2 42.666667-42.666667 42.666667H170.666667c-23.466667 0-42.666667-19.2-42.666667-42.666667V320z m85.333333 42.666667v512h597.333334V362.666667H213.333333zM1024 725.333333V512c0-23.466667-19.2-42.666667-42.666667-42.666667s-42.666667 19.2-42.666666 42.666667v213.333333c0 23.466667 19.2 42.666667 42.666666 42.666667s42.666667-19.2 42.666667-42.666667M42.666667 768c23.466667 0 42.666667-19.2 42.666666-42.666667V512c0-23.466667-19.2-42.666667-42.666666-42.666667s-42.666667 19.2-42.666667 42.666667v213.333333c0 23.466667 19.2 42.666667 42.666667 42.666667" fill="#2F3CF4" p-id="2382"></path></svg>
            </span>
            <span>模型选择：</span>
          </div>
          <div class="row-input">
            <select class="select" v-model="systemConfig.model_name" @change="handleModelChange(systemConfig.model_name)">
              <option
                v-for="item in flatModelList"
                :key="item.model_id"
                :value="item.model_id"
                :data-owned_by="item.model_owned_by"
              >
                {{ item.model_id }}
              </option>
            </select>
          </div>
        </div>
        <hr class="divider" />
        <div class="row">
          <div class="row-label">
            <span class="row-icon">
              <svg t="1744770349533" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="6845" width="36" height="36"><path d="M511.99425547 62C263.46681494 62 62 263.46681494 62 511.99425547s201.46681494 450.00574453 449.99425547 450.00574453 450.00574453-201.47830401 450.00574453-449.99425547S760.52169599 62 511.99425547 62z m232.28141396 682.28715849a38.96059131 38.96059131 0 0 1-55.08023466 0L473.05664317 528.13687695V254.24081826a38.94910224 38.94910224 0 1 1 77.8982036 0v241.63379385l193.32082266 193.32082266a38.94910224 38.94910224 0 0 1 0 55.09172372z" fill="#1296db" p-id="6846"></path></svg>
            </span>
            <span>最大历史对话限制：</span>
          </div>
          <div class="row-input row-input-flex">
            <input type="number" v-model="systemConfig.message_max" placeholder="请输入限制数" min="1" />
            <button type="submit" @click="handleSubmit" class="btn-submit">提交</button>
          </div>
        </div>
      </div>
    </div>
    <div class="section">
      <div class="section-title">模型参数</div>
      <div class="section-content empty">
        <span class="placeholder">等待更新（此处可配置模型相关参数）</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useSystemConfig } from '@/store/dataconfig.ts'
import { ModelOption } from '@/interface'
import axios from 'axios'
import {message} from 'ant-design-vue'

const systemConfig = useSystemConfig()
const modelConfig = ref<ModelOption[]>([])

function handleModelChange(modelId: string) {
  // 根据选中的 modelId 查找归属
  const found = flatModelList.value.find(item => item.model_id === modelId)
  systemConfig.api_name = found?.model_owned_by ?? ''
}

const flatModelList = computed(() => {
  // 支持 model_id 为数组或单值
  return modelConfig.value.flatMap(model => {
    const ids = Array.isArray(model.model_id)
      ? model.model_id
      : [model.model_id]
    return ids.map(id => ({ model_id: id, model_owned_by: model.model_owned_by }))
  })
})

onMounted(async () => {
  const config = await axios.get(`${systemConfig.baseurl}/chat/config`,{
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('JWTtoken')}`
    }
  })
  systemConfig.model_name = config.data.model_name
  systemConfig.api_name = config.data.api_name
  systemConfig.message_max = config.data.message_max
  const response = await axios.get(`${systemConfig.baseurl}/api/models`)
  for (const model of response.data.models) {
      modelConfig.value.push({
      model_id: model.model_id,
      model_owned_by: model.model_owned_by
    })
  }
})
const handleSubmit = async () => {
  if (systemConfig.message_max < 1) {
    message.error('对话历史限制必须大于0')
    return
  }
  if (systemConfig.message_max > 20) {
    message.error('对话历史限制必须小于等于20')
    return
  }
  await axios.post(`${systemConfig.baseurl}/chat/config`,{
    message_max: systemConfig.message_max,
    model_name: systemConfig.model_name,
    api_name: systemConfig.api_name
  },{
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('JWTtoken')}`
    }
  })
  message.success('配置保存成功')
}
</script>

<style scoped>
.mod-config-wrapper {
  max-width: 520px;
  margin: 32px auto;
  padding: 28px 14px 36px 14px;
  background: #fff;
  border-radius: 28px;
  box-shadow: 0 4px 32px 0 rgba(0,0,0,0.10);
  font-family: 'Segoe UI', 'PingFang SC', Arial, sans-serif;
}
.section {
  margin-bottom: 40px;
}
.section-title {
  font-size: 1.35rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #222;
  letter-spacing: 1px;
}
.section-content {
  background: #f6f8fb;
  border-radius: 16px;
  padding: 28px 20px 18px 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.06);
}
.section-content.empty {
  text-align: center;
  color: #bbb;
  font-size: 1rem;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
}
.row:last-child {
  margin-bottom: 0;
}
.row-label {
  display: flex;
  align-items: center;
  font-size: 1.08rem;
  font-weight: 500;
  color: #333;
  min-width: 140px;
}
.row-icon {
  margin-right: 12px;
  display: flex;
  align-items: center;
}
.row-input {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}
.row-input-flex {
  gap: 16px;
}
.select {
  width: 180px;
  height: 42px;
  border: 1.5px solid #d0d5dd;
  border-radius: 14px;
  font-size: 1.08rem;
  padding: 0 12px;
  background: #fff;
  transition: border 0.2s, box-shadow 0.2s;
  box-shadow: 0 1px 6px 0 rgba(47,60,244,0.04);
}
.select:focus, .select:hover {
  border: 2px solid #2f3cf4;
  box-shadow: 0 0 8px #2f3cf440;
}
input[type="number"] {
  width: 120px;
  height: 42px;
  border: 1.5px solid #d0d5dd;
  border-radius: 14px;
  font-size: 1.08rem;
  padding: 0 12px;
  margin-right: 8px;
  transition: border 0.2s, box-shadow 0.2s;
  background: #fff;
  box-shadow: 0 1px 6px 0 rgba(18,150,219,0.04);
}
input[type="number"]:focus {
  border: 2px solid #1296db;
  box-shadow: 0 0 8px #1296db40;
}
.btn-submit {
  height: 42px;
  min-width: 76px;
  background: linear-gradient(90deg, #2f3cf4 0%, #1296db 100%);
  color: #fff;
  border: none;
  border-radius: 14px;
  font-size: 1.07rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px 0 rgba(47,60,244,0.08);
  letter-spacing: 1px;
}
.btn-submit:hover {
  background: linear-gradient(90deg, #1296db 0%, #2f3cf4 100%);
  box-shadow: 0 4px 16px 0 rgba(18,150,219,0.13);
}
.divider {
  border: none;
  border-bottom: 1.5px solid #e0e0e0;
  margin: 22px 0 24px 0;
}
.placeholder {
  color: #bbb;
  font-size: 1rem;
}
@media (max-width: 600px) {
  .mod-config-wrapper {
    width: 80%;
    padding: 10px 2vw 20px 2vw;
    border-radius: 14px;
  }
  .section-content {
    padding: 12px 4px 10px 4px;
    border-radius: 9px;
  }
  .row-label {
    min-width: 90px;
    font-size: 0.97rem;
  }
  .select, input[type="number"], .btn-submit {
    height: 36px;
    font-size: 1rem;
    border-radius: 8px;
  }
}
</style>