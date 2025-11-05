<template>
    <div class="register-container">
        <div class="register-form">
            <h2>用户注册</h2>
            <el-form :model="registerForm" :rules="rules" ref="registerFormRef" class="demo-registerForm">
                <el-form-item prop="username">
                    <el-input v-model="registerForm.username" placeholder="用户名" size="large">
                        <template #prefix>
                            <el-icon>
                                <User />
                            </el-icon>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="email">
                    <el-input v-model="registerForm.email" placeholder="邮箱" size="large">
                        <template #prefix>
                            <el-icon>
                                <Message />
                            </el-icon>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input v-model="registerForm.password" type="password" placeholder="密码" size="large"
                        show-password>
                        <template #prefix>
                            <el-icon>
                                <Lock />
                            </el-icon>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password_confirm">
                    <el-input v-model="registerForm.password_confirm" type="password" placeholder="确认密码" size="large"
                        show-password>
                        <template #prefix>
                            <el-icon>
                                <Lock />
                            </el-icon>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="first_name">
                    <el-input v-model="registerForm.first_name" placeholder="姓" size="large">
                        <template #prefix>
                            <el-icon>
                                <User />
                            </el-icon>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="last_name">
                    <el-input v-model="registerForm.last_name" placeholder="名" size="large">
                        <template #prefix>
                            <el-icon>
                                <User />
                            </el-icon>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="phone">
                    <el-input v-model="registerForm.phone" placeholder="手机号码" size="large">
                        <template #prefix>
                            <el-icon>
                                <Phone />
                            </el-icon>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="age">
                    <el-input v-model.number="registerForm.age" placeholder="年龄" size="large" type="number">
                        <template #prefix>
                            <el-icon>
                                <Calendar />
                            </el-icon>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="risk_tolerance">
                    <el-select v-model="registerForm.risk_tolerance" placeholder="风险承受能力" size="large"
                        style="width: 100%">
                        <el-option label="低风险" value="low"></el-option>
                        <el-option label="中风险" value="medium"></el-option>
                        <el-option label="高风险" value="high"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item prop="total_assets">
                    <el-input v-model.number="registerForm.total_assets" placeholder="总资产（元）" size="large"
                        type="number">
                        <template #prefix>
                            <el-icon>
                                <Money />
                            </el-icon>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="investment_goal">
                    <el-input v-model="registerForm.investment_goal" placeholder="投资目标" size="large" type="textarea"
                        :rows="2">
                    </el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" style="width: 100%;" size="large" @click="handleRegister"
                        :loading="loading">
                        注册
                    </el-button>
                </el-form-item>
            </el-form>

            <div class="login-link">
                <span>已有账号？</span>
                <el-link type="primary" @click="$router.push('/login')">立即登录</el-link>
            </div>
        </div>
    </div>
</template>

<script>
import { User, Lock, Message, Phone, Calendar, Money } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { mapActions } from 'vuex'
import { apiService } from '@/api'

export default {
    name: 'Register',
    components: {
        User,
        Lock,
        Message,
        Phone,
        Calendar,
        Money
    },
    data() {
        return {
            registerForm: {
                username: '',
                email: '',
                password: '',
                password_confirm: '',
                first_name: '',
                last_name: '',
                phone: '',
                age: null,
                risk_tolerance: 'medium',
                total_assets: 100000,
                investment_goal: ''
            },
            rules: {
                username: [
                    { required: true, message: '请输入用户名', trigger: 'blur' },
                    { min: 3, max: 30, message: '用户名长度在 3 到 30 个字符', trigger: 'blur' }
                ],
                email: [
                    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
                    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
                ],
                password_confirm: [
                    { required: true, message: '请确认密码', trigger: 'blur' },
                    { validator: this.validatePasswordConfirm, trigger: 'blur' }
                ],
                first_name: [
                    { required: true, message: '请输入姓', trigger: 'blur' }
                ],
                last_name: [
                    { required: true, message: '请输入名', trigger: 'blur' }
                ],
                phone: [
                    { required: true, message: '请输入手机号码', trigger: 'blur' },
                    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
                ],
                age: [
                    { required: true, message: '请输入年龄', trigger: 'blur' },
                    { type: 'number', min: 18, max: 100, message: '年龄必须在18-100岁之间', trigger: 'blur' }
                ],
                risk_tolerance: [
                    { required: true, message: '请选择风险承受能力', trigger: 'change' }
                ],
                total_assets: [
                    { required: true, message: '请输入总资产', trigger: 'blur' },
                    { type: 'number', min: 0, message: '总资产不能为负数', trigger: 'blur' }
                ]
            },
            loading: false
        }
    },
    methods: {
        ...mapActions(['login']),
        validatePasswordConfirm(rule, value, callback) {
            if (value !== this.registerForm.password) {
                callback(new Error('两次输入的密码不一致'))
            } else {
                callback()
            }
        },
        async handleRegister() {
            this.$refs.registerFormRef.validate(async (valid) => {
                if (valid) {
                    this.loading = true
                    try {
                        // 调用注册API
                        const response = await apiService.register(this.registerForm)

                        if (response.success) {
                            const user = response.user

                            // 注册成功后自动登录
                            const loginResponse = await apiService.login({
                                username: this.registerForm.username,
                                password: this.registerForm.password
                            })

                            // JWT返回access和refresh tokens
                            const { access, refresh } = loginResponse

                            // 存储tokens到localStorage
                            localStorage.setItem('access_token', access)
                            localStorage.setItem('refresh_token', refresh)

                            // 使用Vuex store存储用户信息
                            this.login({
                                id: user.id,
                                username: user.username,
                                name: user.first_name && user.last_name ? `${user.last_name}${user.first_name}` : user.username,
                                email: user.email,
                                phone: user.phone,
                                age: user.age,
                                risk_tolerance: user.risk_tolerance,
                                total_assets: user.total_assets,
                                investment_goal: user.investment_goal
                            })

                            // 存储用户信息到localStorage（用于持久化）
                            localStorage.setItem('isLoggedIn', 'true')
                            localStorage.setItem('userId', user.id.toString())
                            localStorage.setItem('userName', user.username)
                            localStorage.setItem('userRisk', user.risk_tolerance)

                            ElMessage.success('注册成功！')

                            // 跳转到仪表盘
                            this.$router.push('/dashboard')
                        } else {
                            ElMessage.error(response.message || '注册失败')
                        }
                    } catch (error) {
                        console.error('Register error:', error)
                        if (error.response && error.response.data) {
                            if (error.response.data.message) {
                                ElMessage.error(error.response.data.message)
                            } else if (error.response.data.detail) {
                                ElMessage.error(error.response.data.detail)
                            } else {
                                ElMessage.error('注册失败，请检查输入信息')
                            }
                        } else {
                            ElMessage.error('注册失败，请稍后重试')
                        }
                    } finally {
                        this.loading = false
                    }
                }
            })
        }
    }
}
</script>

<style scoped>
.register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-form {
    background: white;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    width: 450px;
    max-height: 80vh;
    overflow-y: auto;
}

.register-form h2 {
    text-align: center;
    margin-bottom: 30px;
    color: #333;
}

.login-link {
    text-align: center;
    margin-top: 20px;
    color: #666;
}

.login-link .el-link {
    margin-left: 5px;
}
</style>
