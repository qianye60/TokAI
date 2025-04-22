<template>
    <h2 class="admin-title">系统配置</h2>
    <div class="config-container">
        <form class="config-form" @submit.prevent="saveConfig">
            <div class="form-group">
                <label>网站标题</label>
                <input type="text" v-model="siteConfig.title" placeholder="输入网站标题"/>
            </div>
            
            <div class="form-group">
                <label>默认余额</label>
                <input type="number" v-model="siteConfig.default_money" placeholder="输入默认余额"/>
            </div>
            
            <div class="form-group">
                <label>开启邮箱注册</label>
                <div class="toggle-container">
                    <button 
                        type="button" 
                        class="toggle-btn" 
                        :class="{'active': siteConfig.email_register}"
                        @click="siteConfig.email_register = !siteConfig.email_register"
                    >
                        {{ siteConfig.email_register ? '已开启' : '已关闭' }}
                    </button>
                    <span class="setting-desc">允许用户通过邮箱注册新账号</span>
                </div>
            </div>
            
            <div class="form-group">
                <label>游客模式 <span class="feature-tag">开发中</span></label>
                <div class="toggle-container">
                    <button 
                        type="button" 
                        class="toggle-btn disabled" 
                        disabled
                    >
                        已关闭
                    </button>
                    <span class="setting-desc">允许未注册用户免费使用网站，可能会导致滥用</span>
                </div>
            </div>
            
            <div class="actions">
                <button type="submit" class="primary-btn">保存配置</button>
            </div>
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useSystemConfig } from '@/store/dataconfig';
import { message } from 'ant-design-vue';

// 状态和配置
const systemConfig = useSystemConfig();

// 网站配置
const siteConfig = reactive({
    title: '',
    default_money: 0,
    email_register: false,
    guest: false
});


// 获取配置
const getConfig = async () => {
    try {
        const response = await axios.get(`${systemConfig.baseurl}/admin/config`);
        
        if (response.data.error) {
            message.error('获取配置失败');
            return;
        }
        
        const data = response.data;
        siteConfig.title = data.title || '';
        siteConfig.default_money = data.default_money || 0;
        siteConfig.email_register = data.email_register || false;
        siteConfig.guest = data.guest || false;
    } catch (error) {
        message.error('获取配置失败');
        console.error(error);
    }
};

// 保存配置
const saveConfig = async () => {
    if (!siteConfig.title) {
        message.warning('请填写网站标题');
        return;
    }
    
    try {
        const token = localStorage.getItem('JWTtoken');
        
        const response = await axios.put(`${systemConfig.baseurl}/admin/config`, siteConfig, {
            headers: { Authorization: `Bearer ${token}` }
        });
        
        if (response.data.error) {
            message.error('保存失败');
        } else {
            message.success('配置已保存');
            document.title = siteConfig.title;
        }
    } catch (error) {
        message.error('保存失败');
        console.error(error);
    }
};

// 页面加载时获取配置
onMounted(() => {
    getConfig();
});
</script>

<style scoped>
.admin-title {
    margin-top: 30px;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 30px;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
}

.config-container {
    padding: 0 20px;
    width: 100%;
}

.config-form {
    max-width: 500px;
}

.form-group {
    margin-bottom: 24px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    color: #333;
}

.toggle-container {
    display: flex;
    align-items: center;
    margin-top: 5px;
}

.toggle-btn {
    min-width: 80px;
    padding: 6px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: #f5f5f5;
    color: #666;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s;
}

.toggle-btn.active {
    background-color: #1890ff;
    color: white;
    border-color: #1890ff;
}

.toggle-btn.disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.setting-desc {
    margin-left: 12px;
    font-size: 14px;
    color: #666;
}

.form-group input[type="text"] {
    width: 90%;
    max-width: 400px;
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
}

.feature-tag {
    display: inline-block;
    background-color: #f56c6c;
    color: white;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 11px;
    margin-left: 8px;
}

.actions {
    display: flex;
    gap: 12px;
    margin-top: 24px;
    margin-bottom: 24px;
}

button {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
}

.primary-btn {
    background-color: #1890ff;
    color: white;
}

.primary-btn:hover {
    background-color: #40a9ff;
}
</style>