<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h2 class="text-3xl font-bold text-gray-900 mb-8">Настройки</h2>

    <el-card class="mb-6">
      <template #header>
        <h3 class="text-lg font-semibold">Общие настройки</h3>
      </template>
      <el-form :model="settings" label-width="200px">
        <el-form-item label="Язык интерфейса">
          <el-select v-model="settings.language" style="width: 200px">
            <el-option label="Русский" value="ru" />
            <el-option label="English" value="en" />
          </el-select>
        </el-form-item>

        <el-form-item label="Тема">
          <el-radio-group v-model="settings.theme">
            <el-radio value="light">Светлая</el-radio>
            <el-radio value="dark">Темная</el-radio>
            <el-radio value="auto">Автоматически</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSave">Сохранить</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card>
      <template #header>
        <h3 class="text-lg font-semibold">Уведомления</h3>
      </template>
      <el-form :model="notifications" label-width="200px">
        <el-form-item>
          <el-checkbox v-model="notifications.email">Email уведомления</el-checkbox>
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="notifications.telegram">Telegram уведомления</el-checkbox>
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="notifications.errors">Уведомления об ошибках</el-checkbox>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSaveNotifications">Сохранить</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const settings = ref({
  language: 'ru',
  theme: 'light'
})

const notifications = ref({
  email: true,
  telegram: false,
  errors: true
})

const handleSave = () => {
  // TODO: Implement save
  console.log('Save settings:', settings.value)
}

const handleSaveNotifications = () => {
  // TODO: Implement save
  console.log('Save notifications:', notifications.value)
}
</script>



