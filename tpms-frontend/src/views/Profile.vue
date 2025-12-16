<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h2 class="text-3xl font-bold text-gray-900 mb-8">Профиль</h2>

    <el-card>
      <el-form :model="form" label-width="150px">
        <el-form-item label="Имя пользователя">
          <el-input v-model="form.username" disabled />
        </el-form-item>

        <el-form-item label="Email">
          <el-input v-model="form.email" type="email" />
        </el-form-item>

        <el-form-item label="Роль">
          <el-input v-model="form.role" disabled />
        </el-form-item>

        <el-form-item label="Telegram ID">
          <el-input v-model="form.telegram_id" disabled />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSave">Сохранить</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()

const form = ref({
  username: '',
  email: '',
  role: '',
  telegram_id: null as number | null
})

onMounted(() => {
  if (authStore.user) {
    form.value = {
      username: authStore.user.username || '',
      email: authStore.user.email || '',
      role: authStore.user.role || '',
      telegram_id: authStore.user.telegram_id || null
    }
  }
})

const handleSave = async () => {
  // TODO: Implement save
  console.log('Save profile:', form.value)
}
</script>



