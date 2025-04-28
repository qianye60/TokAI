<template>
    <div class="admin-container">
        <!-- 页面标题 -->
        <h2 class="admin-title">用户管理</h2>
        
        <!-- 操作区域 -->
        <div class="user-header">
            <div class="search-box">
                <input type="text" placeholder="搜索用户...(ID/用户名)" v-model="searchQuery">
            </div>
            <button class="primary-btn" @click="showAddModal = true">添加用户</button>
        </div>

        <!-- 表格区域 -->
        <div class="table-container">
            <table class="data-table">
                <!-- 表头定义 -->
                <thead>
                    <tr>
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
                        <td colspan="5" class="text-center">加载中...</td>
                    </tr>
                    <!-- 无数据状态 -->
                    <tr v-else-if="filteredUsers.length === 0">
                        <td colspan="5" class="text-center">没有找到用户</td>
                    </tr>
                    <!-- 用户数据行 -->
                    <tr v-for="user in paginatedUsers" :key="user.id">
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
                                <button class="edit-btn" @click="editUser(user.id)">编辑</button>
                                <button class="delete-btn" @click="deleteUser(user.id)">注销</button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- 分页控件 -->
        <div class="pagination" v-if="users.length > 0">
            <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">&laquo;</button>
            <button 
                v-for="page in displayedPageNumbers" 
                :key="page" 
                :class="{ active: currentPage === page }"
                @click="goToPage(page)"
            >
                {{ page }}
            </button>
            <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">&raquo;</button>
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
                    <label>用户名</label>
                    <input type="text" v-model="editingUser.username" />
                </div>
                <div class="form-group">
                    <label>邮箱</label>
                    <input type="text" v-model="editingUser.email"/>
                </div>
                <div class="form-group">
                    <label>用户密码<span class="note">(不改请不要输入)</span></label>
                    <input type="text" v-model="password"/>
                </div>
                <div class="form-group">
                    <label>账户余额</label>
                    <input type="number" v-model="editingUser.money" />
                </div>
                <div class="form-group">
                    <label>用户角色</label>
                    <select v-model="editingUser.authuser">
                        <option value="0">普通用户</option>
                        <option value="1">管理员</option>
                    </select>
                </div>
            </div>
            <div class="modal-footer">
                <button class="cancel-btn" @click="showEditModal = false">取消</button>
                <button class="primary-btn" @click="saveUserChanges">保存</button>
            </div>
        </div>
    </div>
    
    <!-- 添加用户对话框 -->
    <div class="modal" v-if="showAddModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>添加用户</h3>
                <span class="close-btn" @click="showAddModal = false">&times;</span>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label>用户名</label>
                    <input type="text" v-model="newUser.username" />
                </div>
                <div class="form-group">
                    <label>邮箱</label>
                    <input type="text" v-model="newUser.email"/>
                </div>
                <div class="form-group">
                    <label>用户密码</label>
                    <input type="text" v-model="newUser.password"/>
                </div>
                <div class="form-group">
                    <label>账户余额 (默认: {{defaultMoney}})</label>
                    <input type="number" v-model="newUser.money" />
                </div>
                <div class="form-group">
                    <label>用户角色</label>
                    <select v-model="newUser.userauth">
                        <option value="0">普通用户</option>
                        <option value="1">管理员</option>
                    </select>
                </div>
            </div>
            <div class="modal-footer">
                <button class="cancel-btn" @click="showAddModal = false">取消</button>
                <button class="primary-btn" @click="createUser">创建</button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
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

// 分页相关状态
const currentPage = ref(1);
const pageSize = ref(10);
const maxDisplayedPages = ref(5);

// 默认余额
const defaultMoney = ref(0);

// 外部组件
const messageAPI = message;

// 计算总页数
const totalPages = computed(() => {
    return Math.ceil(filteredUsers.value.length / pageSize.value);
});

// 计算要显示的页码
const displayedPageNumbers = computed(() => {
    const pages = [];
    let startPage = Math.max(1, currentPage.value - Math.floor(maxDisplayedPages.value / 2));
    let endPage = Math.min(totalPages.value, startPage + maxDisplayedPages.value - 1);
    
    if (endPage - startPage + 1 < maxDisplayedPages.value) {
        startPage = Math.max(1, endPage - maxDisplayedPages.value + 1);
    }
    
    for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
    }
    
    return pages;
});

// 切换到指定页面
const goToPage = (page: number) => {
    if (page < 1 || page > totalPages.value) {
        return;
    }
    currentPage.value = page;
};

// 根据当前页数和分页大小，获取用户列表的分页数据
const paginatedUsers = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value;
    const end = start + pageSize.value;
    return filteredUsers.value.slice(start, end);
});

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
    authuser: '0'
});

// 添加用户状态
const showAddModal = ref(false);
const newUser = ref({
    username: '',
    email: '',
    password: '',
    money: 0,
    userauth: '0'
});

// 监听搜索条件变化，重置到第一页
watch(searchQuery, () => {
    currentPage.value = 1;
});

// 获取默认余额
const fetchDefaultMoney = async () => {
    try {
        const token = localStorage.getItem('JWTtoken');
        if (!token) return;
        
        const response = await axios.get(`${systemConfig.baseurl}/admin/default-money`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        
        if (response.data && response.data.default_money !== undefined) {
            defaultMoney.value = response.data.default_money;
            newUser.value.money = response.data.default_money;
        }
    } catch (error) {
        messageAPI.error('获取默认余额失败: ' + error);
    }
};

// 创建新用户
const createUser = async () => {
    try {
        loading.value = true;
        const token = localStorage.getItem('JWTtoken');
        
        // 验证表单数据
        if (!newUser.value.username || !newUser.value.email || !newUser.value.password) {
            messageAPI.error('请填写必要的信息');
            loading.value = false;
            return;
        }
        
        // 调用管理员创建用户API
        await axios.post(
            `${systemConfig.baseurl}/admin/users`, 
            {
                username: newUser.value.username,
                email: newUser.value.email,
                password: newUser.value.password,
                money: newUser.value.money,
                userauth: parseInt(newUser.value.userauth)
            },
            {
                headers: { Authorization: `Bearer ${token}` }
            }
        );
        
        // 重新加载用户列表
        await fetchUsers();
        
        // 重置表单并关闭对话框
        newUser.value = {
            username: '',
            email: '',
            password: '',
            money: defaultMoney.value,
            userauth: '0'
        };
        showAddModal.value = false;
        messageAPI.success('用户创建成功');
    } catch (error: any) {
        if (error.response) {
            messageAPI.error(`创建用户失败: ${error.response.data.detail || '未知错误'}`);
        } else {
            messageAPI.error('创建用户失败: ' + error);
        }
    } finally {
        loading.value = false;
    }
};

// 重新加载用户列表
const fetchUsers = async () => {
    try {
        const token = localStorage.getItem('JWTtoken');
        if (!token) {
            router.push('/login');
            return;
        }

        users.value = []; // 清空现有数据
        
        // 获取用户列表数据
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
    } catch (error) {
        messageAPI.error('获取用户数据失败: ' + error);
    }
};

// 初始化函数
const initialize = async () => {
    loading.value = true;
    try {
        const token = localStorage.getItem('JWTtoken');
        if (!token) {
            router.push('/login');
            return;
        }

        // 获取默认余额
        await fetchDefaultMoney();
        
        // 获取用户列表
        await fetchUsers();
    } catch (error) {
        messageAPI.error('初始化失败: ' + error);
    } finally {
        loading.value = false;
    }
};

// 初始化：获取用户列表数据
onMounted(initialize);

const editUser = (userId: number) => {
    // 找到要编辑的用户
    const userToEdit = users.value.find(user => user.id === userId);
    if (userToEdit) {
        // 复制用户数据到编辑用户对象
        editingUser.value = { 
            ...userToEdit,
            authuser: userToEdit.authuser.toString()
        };
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
                userauth: parseInt(editingUser.value.authuser)
            },
            {
                headers: { Authorization: `Bearer ${token}` }
            }
        );
        
        // 更新本地数据
        const index = users.value.findIndex(user => user.id === editingUser.value.id);
        if (index !== -1) {
            users.value[index].money = editingUser.value.money;
            users.value[index].authuser = parseInt(editingUser.value.authuser);
        }
        
        // 关闭对话框
        showEditModal.value = false;
        messageAPI.success('用户信息已更新');
    } catch (error: any) {
        messageAPI.error('更新用户信息失败:' + (error.response?.data?.detail || error));
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
/* 管理页面容器 */
.admin-container {
    width: 100%;

    box-sizing: border-box;
    background-color: var(--background-color, #333);
    color: var(--text-color, #fff);
}

/* 页面标题样式 */
.admin-title {
    margin-top: 20px;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    padding-bottom: 10px;
    color: var(--text-color, #fff);
}

/* 操作区域 */
.user-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

/* 搜索框 */
.search-box {
    width: 300px;
}

.search-box input {
    width: 100%;
    padding: 8px 12px;
    border-radius: 15px;
    border: 1px solid var(--border-color, #444);
    background-color: var(--background-color, #333);
    color: var(--text-color, #fff);
    font-size: 14px;
}

/* 表格容器 */
.table-container {
    width: 100%;
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 15px rgba(0, 0, 0, 0.2);
    overflow: hidden;
}

/* 数据表格样式 */
.data-table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
    color: var(--text-color, #fff);
    table-layout: fixed;
}

.data-table th, 
.data-table td {
    padding: 12px;
    border-bottom: 1px solid var(--border-color, #444);
}

.data-table th {
    background-color: var(--header-bg, rgba(0, 0, 0, 0.2));
    font-weight: 600;
}

.data-table tr:hover {
    background-color: var(--hover-bg, rgba(139, 139, 139, 0.3));
    transition: all 0.2s ease;
}

/* 文本居中 */
.text-center {
    text-align: center;
}

/* 角色标签样式 */
.role-tag {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
}

.superadmin {
    background-color: #141414;
    background-image: linear-gradient(135deg, #141414, #2d2d2d);
    color: #ffcc00;
    border: 1px solid #ffcc00;
    text-shadow: 0 1px 1px rgba(0, 0, 0, 0.7);
}

.admin {
    background-color: var(--primary-color, #0062ff);
    color: white;
}

.user {
    background-color: var(--background-sidebar, #4d4d4d);
    color: var(--text-color, #ddd);
}

/* 按钮样式 */
button {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s;
}

.primary-btn {
    background-color: var(--primary-color, #28a745);
    color: white;
}

.primary-btn:hover {
    background-color: var(--primary-hover, #218838);
    transform: translateY(-1px);
}

.edit-btn {
    background-color: var(--info-color, #0d6efd);
    color: white;
    margin-right: 8px;
}

.edit-btn:hover {
    background-color: var(--info-hover, #0b5ed7);
    transform: translateY(-1px);
}

.delete-btn {
    background-color: var(--danger-color, #dc3545);
    color: white;
}

.delete-btn:hover {
    background-color: var(--danger-hover, #bb2d3b);
    transform: translateY(-1px);
}

.cancel-btn {
    background-color: var(--text-color, #f0f0f0);
    color: var(--background-color);
}

/* 操作按钮容器 */
.action-buttons {
    display: flex;
    gap: 5px;
}

/* 分页控件 */
.pagination {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 5px;
    margin: 15px 0;
}

.pagination button {
    padding: 5px 10px;
    border: 1px solid var(--border-color, #444);
    background-color: var(--page-bg, #333);
    color: var(--text-color, #fff);
    cursor: pointer;
    border-radius: 4px;
    transition: all 0.2s ease;
    min-width: 32px;
}

.pagination button.active {
    background-color: var(--primary-color, #0d6efd);
    border-color: var(--primary-color, #0d6efd);
}

.pagination button:hover:not(:disabled) {
    background-color: rgba(var(--primary-color, 13, 110, 253), 0.1);
    border-color: var(--primary-color, #0d6efd);
}

.pagination button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* 模态对话框 */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    backdrop-filter: blur(3px);
}

.modal-content {
    background-color: var(--background-color);
    border-radius: 10px;
    width: 500px;
    max-width: 95%;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
    overflow: hidden;
    animation: modal-appear 0.3s ease;
}

@keyframes modal-appear {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    border-bottom: 1px solid var(--border-color, #444);
}

.modal-header h3 {
    margin: 0;
    color: var(--text-color);
    font-size: 18px;
}

.close-btn {
    background: none;
    border: none;
    font-size: 22px;
    cursor: pointer;
    color: var(--text-color);
    transition: color 0.2s;
}

.close-btn:hover {
    color: var(--primary-color, #4e89e8);
}

.modal-body {
    padding: 20px;
    max-height: 70vh;
    overflow-y: auto;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
}

.form-group input,
.form-group select {
    width: 100%;
    padding: 10px;
    border: 1px solid var(--border-color, #444);
    border-radius: 6px;
    background-color: var(--background-color);
    color: var(--text-color);
    font-size: 14px;
    box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus {
    border-color: var(--primary-color, #4e89e8);
    outline: 0;
    box-shadow: 0 0 0 3px rgba(78, 137, 232, 0.25);
}

.note {
    color: #ff4d4f;
    font-size: 12px;
    margin-left: 8px;
}

.modal-footer {
    padding: 15px 20px;
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    border-top: 1px solid var(--border-color, #444);
}

/* 响应式调整 */
@media (max-width: 768px) {
    .admin-container{
        overflow-y: auto;
        max-height: 80vh;
        overflow-x: hidden;
    }
    .user-header {
        flex-direction: column;
        align-items: stretch;
        gap: 10px;
    }
    
    .search-box {
        width: 100%;
    }
    
    .action-buttons {
        flex-direction: column;
        width: 100%;
    }
    
    .action-buttons button {
        margin-right: 0;
        margin-bottom: 5px;
        width: 100%;
    }
}
</style>
