<template>
    <!-- 用户管理主容器 -->
    <div class="user-management">
        <!-- 顶部标题和搜索区域 -->
        <div class="user-header">
            <h2>用户管理</h2>
            <div class="search-box">
                <input class="search-input" type="text" placeholder="搜索用户...(ID/用户名)" v-model="searchQuery">
            </div>
        </div>

        <!-- 表格区域 -->
        <div class="table-wrapper">
            <table class="user-table">
                <!-- 表头定义 -->
                <thead>
                    <tr class="user-table-header">
                        <th>ID</th>
                        <th>用户名</th>
                        <th>余额</th>
                        <th>角色</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <!-- 表格内容 -->
                <tbody>
                    <!-- 加载状态 -->
                    <tr v-if="loading">
                        <td colspan="4" class="text-center">加载中...</td>
                    </tr>
                    <!-- 无数据状态 -->
                    <tr v-else-if="filteredUsers.length === 0">
                        <td colspan="4" class="text-center">没有找到用户</td>
                    </tr>
                    <!-- 用户数据行 -->
                    <tr v-for="user in filteredUsers" :key="user.id" class="user-row">
                        <td>{{ user.id }}</td>
                        <td>{{ user.username }}</td>
                        <td>{{ user.money }}</td>
                        <td>
                            <span class="role-tag" :class="getRoleClass(user.authuser)">
                                {{ getRoleText(user.authuser) }}
                            </span>
                        </td>
                        <td>
                            <div class="action-buttons">
                                <button class="btn edit-btn" @click="editUser(user.id)">编辑</button>
                                <button class="btn delete-btn" @click="deleteUser(user.id)">注销</button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- 分页控件 -->
        <div class="pagination" v-if="users.length > 10">
            <button class="page-btn">&laquo;</button>
            <button class="page-btn active">1</button>
            <button class="page-btn">2</button>
            <button class="page-btn">&raquo;</button>
        </div>
    </div>
    <!-- 编辑用户对话框 -->
    <div class="modal" v-if="showEditModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>编辑用户</h3>
                <span class="close-btn" @click="showEditModal = false">&times;</span>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label >用户名</label>
                    <input class="form-control" type="text" v-model="editingUser.username" />
                </div>
                <div class="form-group">
                    <label>邮箱</label>
                    <input class="form-control" type="text" v-model="editingUser.email"/>
                </div>
                <div class="form-group">
                    <label>用户密码<span style="color: red;">(不改请不要输入)</span></label>
                    <input class="form-control" type="text" v-model="password"/>
                </div>
                <div class="form-group">
                    <label>账户余额</label>
                    <input class="form-control" type="number" v-model="editingUser.money" />
                </div>
                <div class="form-group">
                    <label>用户角色</label>
                    <select class="form-control" v-model="editingUser.authuser">
                        <option value="0">普通用户</option>
                        <option value="1">管理员</option>
                    </select>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn cancel-btn" @click="showEditModal = false">取消</button>
                <button class="btn save-btn" @click="saveUserChanges">保存</button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useUserConfig, useSystemConfig } from "@/store/dataconfig";
import axios from 'axios';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';

// 系统配置和路由
const systemConfig = useSystemConfig();
const userStore = useUserConfig();
const router = useRouter();

// 状态管理
const users = ref<Array<{id: number, username: string, email: string, money: number, authuser: number}>>([]);
const loading = ref(true);
const searchQuery = ref('');
const password = ref('');

// 外部组件
const messageAPI = message;

// 过滤后的用户列表 - 根据搜索关键词实时过滤
const filteredUsers = computed(() => {
    if (!searchQuery.value) return users.value;
    
    const query = searchQuery.value.toLowerCase();
    return users.value.filter(user => 
        user.username.toLowerCase().includes(query) || 
        user.id.toString().includes(query)
    );
});

// 获取角色对应的样式类
const getRoleClass = (authuser: number): string => {
    switch(authuser) {
        case 2: return 'superadmin';
        case 1: return 'admin';
        default: return 'user';
    }
};
const getRoleText = (authuser: number): string => {
    switch(authuser) {
        case 2: return '超级管理员';
        case 1: return '管理员';
        default: return '用户';
    }
};

// 编辑用户相关的状态
const showEditModal = ref(false);
const editingUser = ref({
    id: 0,
    username: '',
    email: '',
    money: 0,
    authuser: 0
});

// 初始化：获取用户列表数据
onMounted(async () => {
    try {
        const token = localStorage.getItem('JWTtoken');
        if (!token) {
            router.push('/login');
            return;
        }

        // 获取用户列表数据
        try {
            const response = await axios.get(`${systemConfig.baseurl}/admin/users`, {
               headers: { Authorization: `Bearer ${token}` }
            });
            for (const user of response.data) {
                users.value.push({
                    id: user.id,
                    username: user.username,
                    email: user.email,
                    money: user.money,
                    authuser: user.userauth
                });
            }
            loading.value = false;
          } catch (error) {
            messageAPI.error('获取用户数据失败:' + error);
            loading.value = false;
        }
    } catch (error) {
        messageAPI.error('初始化失败:' + error);
        loading.value = false;
    }
});

const editUser = (userId: number) => {
    // 找到要编辑的用户
    const userToEdit = users.value.find(user => user.id === userId);
    if (userToEdit) {
        // 复制用户数据到编辑用户对象
        editingUser.value = { ...userToEdit };
        // 显示编辑对话框
        showEditModal.value = true;
    }
};

// 保存用户修改
const saveUserChanges = async () => {
    try {
        loading.value = true;
        const token = localStorage.getItem('JWTtoken');
        
        // 这里需要实现后端API调用来更新用户信息
        // 假设有一个更新用户的API端点
        await axios.put(
            `${systemConfig.baseurl}/admin/users/${editingUser.value.id}`, 
            {
                username: editingUser.value.username,
                email: editingUser.value.email,
                password: password.value,
                money: editingUser.value.money,
                userauth: editingUser.value.authuser
            },
            {
                headers: { Authorization: `Bearer ${token}` }
            }
        );
        
        // 更新本地数据
        const index = users.value.findIndex(user => user.id === editingUser.value.id);
        if (index !== -1) {
            users.value[index].money = editingUser.value.money;
            users.value[index].authuser = editingUser.value.authuser;
        }
        
        // 关闭对话框
        showEditModal.value = false;
        messageAPI.success('用户信息已更新');
    } catch (error) {
        messageAPI.error('更新用户信息失败:' + error);
    } finally {
        loading.value = false;
    }
};

const deleteUser = async (userId: number) => {
    try {
        const token = localStorage.getItem('JWTtoken');
        const response = await axios.delete(`${systemConfig.baseurl}/admin/users/${userId}`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        
        // 更新本地数据
        const index = users.value.findIndex(user => user.id === userId);
        if (index !== -1) {
            users.value.splice(index, 1);
        }
        // 关闭对话框
        showEditModal.value = false;
        messageAPI.success('用户已删除');
    } catch (error) {
        messageAPI.error('删除用户失败:' + error);
    }
};
</script>

<style scoped>
/* 主容器样式 - 占满可用空间并留出顶部边距 */
.user-management {
    width: 100%;
    height: calc(100% - 1.5rem); /* 减去顶部边距 */
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding-top: 1.5rem; /* 顶部与顶端的距离 */
}

/* 标题和搜索区域 - 水平排列 */
.user-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}
.admin-footer {
    position: absolute;
    top: 50%;
    left: 25%;
    width: 50%;
    height: 50%;
}
/* 标题样式 */
.user-header h2 {
    margin: 0;
    color: var(--text-color, #fff);
    font-size: 1.5rem;
    font-weight: 600;
}

/* 搜索框容器 */
.search-box {
    position: relative;
}

/* 搜索输入框样式 */
.search-input {
    padding: 0.5rem 1rem;
    border-radius: 15px;
    border: 1px solid var(--border-color, #444);
    background-color: var(--background-color, #333);
    color: var(--text-color, #fff);
    width: 240px;
    font-size: 0.9rem;
    outline: none;
    outline-color: #66afe9; /* 当有焦点时的轮廓颜色 */
    transition: all 0.2s ease; /* 平滑过渡效果 */
}

/* 搜索框焦点状态 */
.search-input:focus {
    border-color: var(--primary-color, #0d6efd);
    box-shadow: 0 0 3px rgba(13, 110, 253, 0.3);
}

/* 占位符文本颜色 */
.search-input::placeholder {
    color: var(--text-secondary, #999);
}

/* 表头样式 */
.user-table-header {
    background-color: var(--header-bg, rgba(176, 176, 176, 0.498)); /* 更柔和的背景 */
}

/* 表格容器 - 添加阴影和圆角 */
.table-wrapper {
    width: 100%;
    overflow-x: auto; /* 允许水平滚动 */
    background-color: var(--background-color);
    border-radius: 8px;
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.15);
}

/* 表格基本样式 */
.user-table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
    color: var(--text-color, #fff);
}
/* 表头单元格样式 */
.user-table th {
    padding: 1rem;
    background-color: var(--header-bg, rgba(0, 0, 0, 0.1)); /* 更柔和的背景 */
    font-weight: 600;
    border-bottom: 1px solid var(--border-color, #444);
}

/* 数据单元格样式 */
.user-table td {
    padding: 0.8rem 1rem;
    border-bottom: 1px solid var(--border-color, #444);
}

/* 行悬停效果 */
.user-row:hover {
    background-color: var(--hover-bg, rgba(139, 139, 139, 0.559));
    transition: all 0.2s ease;
}

/* 文本居中对齐 */
.text-center {
    text-align: center;
}

/* 角色标签基本样式 */
.role-tag {
    display: inline-block;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 500;
}
/* 超级管理员角色 - 权限值2 */
.superadmin {
    background-color: #141414;
    background-image: linear-gradient(135deg, #141414, #2d2d2d);
    color: #ffcc00;
    font-family: var(--font-family, 'Noto Sans CJK SC', sans-serif);
    font-weight: 600;
    letter-spacing: 0.8px;
    border: 1px solid #ffcc00;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    text-shadow: 0 1px 1px rgba(0, 0, 0, 0.7);
    position: relative;
    overflow: hidden;
    padding: 0.35rem 0.9rem;
    border-radius: 4px;
    transition: all 0.3s ease;
    z-index: 1;
}

.superadmin::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 50%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
    animation: shine 5s infinite ease-in-out;
    z-index: -1;
}

@keyframes shine {
    0% { left: -100%; }
    20% { left: 100%; }
    100% { left: 100%; }
}

/* 管理员角色 - 权限值1 */
.admin {
    background-color: var(--vip-bg, #0062ff);
    color: var(--vip-color, #fff);
}

/* 普通用户角色 - 权限值0 */
.user {
    background-color: var(--user-bg, #4d4d4d);
    color: var(--user-color, #ddd);
}
/* 操作按钮容器 */
.action-buttons {
    display: flex;
    gap: 0.5rem;
}

/* 按钮基本样式 */
.btn {
    padding: 0.3rem 0.6rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.8rem;
    transition: all 0.2s;
}

/* 编辑按钮样式 */
.edit-btn {
    background-color: var(--edit-btn, #0d6efd);
    color: white;
}

/* 编辑按钮悬停效果 */
.edit-btn:hover {
    background-color: var(--edit-btn-hover, #0b5ed7);
}

/* 删除按钮样式 */
.delete-btn {
    background-color: var(--delete-btn, #dc3545);
    color: white;
}

/* 删除按钮悬停效果 */
.delete-btn:hover {
    background-color: var(--delete-btn-hover, #bb2d3b);
}

/* 分页控件容器 */
.pagination {
    display: flex;
    justify-content: center;
    gap: 0.3rem;
    margin-top: 1rem;
}

/* 分页按钮样式 */
.page-btn {
    padding: 0.3rem 0.7rem;
    border: 1px solid var(--border-color, #444);
    background-color: var(--page-bg, #333);
    color: var(--text-color, #fff);
    cursor: pointer;
    border-radius: 4px;
}

/* 当前活动页按钮 */
.page-btn.active {
    background-color: var(--primary-color, #0d6efd);
    border-color: var(--primary-color, #0d6efd);
}

/* 响应式设计 - 适应小屏幕 */
@media (max-width: 768px) {
    /* 小屏幕上标题和搜索框垂直排列 */
    .user-header {
        padding-left: 1rem;
        justify-content: center;
        flex-direction: column;
        align-items: stretch;
        gap: 0.8rem;
    }
    
    .search-input {
        width: 80%;
    }
    
    /* 小屏幕上操作按钮垂直排列 */
    .action-buttons {
        flex-direction: column;
    }
}

/* 模态对话框样式 */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content {
    background-color: var(--background-color);
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    width: 90%;
    max-width: 500px;
    overflow: hidden;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid #ddd;
}

.modal-header h3 {
    margin: 0;
    color: var(--text-color);
}

.close-btn {
    font-size: 1.5rem;
    font-weight: bold;
    cursor: pointer;
    color: var(--text-color);
}

.modal-body {
    padding: 1rem;
}

.form-group {
    margin-bottom: 1rem;
    font-family: var(--background-color);;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
}

.form-group input,
.form-group select {
    width: 97%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: var(--background-color, #f8f8f8);
    color: var(--text-color);
}
input:focus{
    border-color: #66afe9;
    outline: 0;
    -webkit-box-shadow: inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgba(102,175,233,.6);
    box-shadow: inset 0 1px 1px rgba(0,0,0,.075),0 0 8px rgba(102,175,233,.6)
}

.modal-footer {
    padding: 1rem;
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
    border-top: 1px solid #ddd;
}

.btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
}

.cancel-btn {
    background-color: var(--text-color, #f0f0f0);
    color: var(--background-color);
}

.save-btn {
    background-color: var(--primary-color, #4e89e8);
    color: white;
}

.logout-btn {
    background-color: var(--error-color, #e74c3c);
    color: white;
}
</style>