<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center px-4">
    <div class="max-w-md w-full">
      <div class="bg-white rounded-2xl shadow-lg p-8">
        <div class="text-center mb-8">
          <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center mx-auto mb-4">
            <el-icon :size="32" class="text-white">
              <Promotion />
            </el-icon>
          </div>
          <h1 class="text-2xl font-bold gradient-text mb-2">TPMS</h1>
          <p class="text-gray-600">Войдите в систему</p>
        </div>

        <el-form :model="form" :rules="rules" ref="formRef" @submit.prevent="handleLogin">
          <el-form-item label="Имя пользователя" prop="username">
            <el-input
              v-model="form.username"
              placeholder="Введите имя пользователя"
              size="large"
            />
          </el-form-item>

          <el-form-item label="Пароль" prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="Введите пароль"
              size="large"
              show-password
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              style="width: 100%"
              :loading="loading"
              @click="handleLogin"
            >
              Войти
            </el-button>
          </el-form-item>
        </el-form>

        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Или войдите через Telegram
          </p>
          <el-button
            type="default"
            size="large"
            style="width: 100%; margin-top: 12px"
            @click="handleTelegramLogin"
          >
            <el-icon><ChatLineRound /></el-icon>
            Войти через Telegram
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { Promotion, ChatLineRound } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()

const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules: FormRules = {
  username: [
    { required: true, message: 'Введите имя пользователя', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Введите пароль', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const result = await authStore.login({
          username: form.username,
          password: form.password
        })
        
        if (result.success) {
          router.push('/')
        } else {
          // Show error message
          console.error(result.error)
        }
      } catch (error) {
        console.error('Login error:', error)
      } finally {
        loading.value = false
      }
    }
  })
}

const handleTelegramLogin = () => {
  // TODO: Implement Telegram login
  console.log('Telegram login')
}
</script>

<style scoped>
.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>

