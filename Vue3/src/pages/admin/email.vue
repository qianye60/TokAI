<template>
    <div class="admin-title">邮件配置</div>
    <div class="email-config-container">
        <form class="email-form" @submit.prevent="saveEmailConfig">
            <div class="form-group">
                <label>SMTP服务器</label>
                <input type="text" v-model="emailConfig.smtp_server" placeholder="例如: smtp.qq.com"/>
            </div>
            
            <div class="form-group">
                <label>端口</label>
                <input type="number" v-model="emailConfig.port" placeholder="例如: 465"/>
            </div>
            
            <div class="form-group">
                <label>发件人邮箱</label>
                <input type="email" v-model="emailConfig.sender" placeholder="例如: example@qq.com"/>
            </div>
            
            <div class="form-group">
                <label>用户名</label>
                <input type="text" v-model="emailConfig.user" placeholder="通常是邮箱地址"/>
            </div>
            
            <div class="form-group">
                <label>密码/授权码</label>
                <input type="password" v-model="emailConfig.passwd" placeholder="密码或授权码"/>
            </div>
            
            <div class="actions">
                <button type="submit" class="primary-btn">保存</button>
                <button type="button" class="secondary-btn" @click="showTestPanel = !showTestPanel">
                    {{ showTestPanel ? '隐藏测试' : '测试' }}
                </button>
            </div>
        </form>
        
        <!-- 测试面板 -->
        <div v-if="showTestPanel" class="test-panel">
            <div class="form-group">
                <label>测试邮箱</label>
                <div class="test-input">
                    <input type="email" v-model="testEmail" placeholder="接收测试邮件的邮箱"/>
                    <button @click="sendTestEmail" :disabled="isSending" class="test-btn">
                        {{ isSending ? '发送中...' : '发送' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useSystemConfig } from '@/store/dataconfig';
import { message } from 'ant-design-vue';

// 状态和配置
const systemConfig = useSystemConfig();
const showTestPanel = ref(false);
const isSending = ref(false);
const testEmail = ref('');

// 邮件配置
const emailConfig = reactive({
    smtp_server: '',
    sender: '',
    user: '',
    port: 465,
    passwd: ''
});

// 获取邮件配置
const getEmailConfig = async () => {
    try {
        const token = localStorage.getItem('JWTtoken');
        const response = await axios.get(`${systemConfig.baseurl}/admin/email`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        
        if (response.data.error) {
            message.error('获取配置失败');
            return;
        }
        
        const data = response.data;
        emailConfig.smtp_server = data.smtp_server || '';
        emailConfig.sender = data.sender || '';
        emailConfig.user = data.user || '';
        emailConfig.port = data.port || 465;
    } catch (error) {
        message.error('获取配置失败');
        console.error(error);
    }
};

// 保存邮件配置
const saveEmailConfig = async () => {
    if (!emailConfig.smtp_server || !emailConfig.sender || !emailConfig.user || !emailConfig.passwd) {
        message.warning('请填写所有必要项');
        return;
    }
    
    try {
        const token = localStorage.getItem('JWTtoken');
        
        const response = await axios.put(`${systemConfig.baseurl}/admin/email`, emailConfig, {
            headers: { Authorization: `Bearer ${token}` }
        });
        if (response.data.success) {
            message.success('配置已保存');
            await getEmailConfig();
        } else {
            message.error('保存失败');
        }
    } catch (error) {
        message.error('保存失败');
        console.error(error);
    }
};

// 发送测试邮件
const sendTestEmail = async () => {
    if (!testEmail.value) {
        message.warning('请填写测试邮箱');
        return;
    }
    
    isSending.value = true;
    try {
        const token = localStorage.getItem('JWTtoken');
        const response = await axios.post(`${systemConfig.baseurl}/admin/email_test`, {
            email: testEmail.value
        }, {
            headers: { Authorization: `Bearer ${token}` }
        });
        
        if (response.data.success) {
            message.success('测试邮件已发送');
        } else {
            message.warning('发送失败');
        }
    } catch (error) {
        message.error('发送失败');
        console.error(error);
    } finally {
        isSending.value = false;
    }
};

// 页面加载时获取配置
onMounted(() => {
    getEmailConfig();
});
</script>

<style scoped>
.admin-title {
    margin-top: 30px;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 30px;
    padding-bottom: 10px;
}

.email-config-container {
    padding: 0 20px;
}

.email-form {
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

.form-group input {
    width: 90%;
    max-width: 400px;
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
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

.secondary-btn {
    background-color: #52c41a;
    color: white;
}

.test-panel {
    margin-top: 20px;
    padding: 16px;
    background-color: #f5f5f5;
    border-radius: 4px;
    max-width: 500px;
}

.test-input {
    display: flex;
    gap: 8px;
    align-items: center;
}

.test-input input {
    flex: 1;
}

.test-btn {
    background-color: #faad14;
    color: white;
    white-space: nowrap;
}
</style>