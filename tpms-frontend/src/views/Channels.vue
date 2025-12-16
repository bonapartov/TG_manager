<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8">
      <div>
        <h2 class="text-3xl font-bold text-gray-900 mb-2">Каналы</h2>
        <p class="text-gray-600">Управление Telegram-каналами и ботами</p>
      </div>
      <el-button type="primary" size="large" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        Добавить канал
      </el-button>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <el-card>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600 mb-1">Публичных каналов</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.public }}</p>
          </div>
          <el-icon :size="40" class="text-blue-500"><Promotion /></el-icon>
        </div>
      </el-card>

      <el-card>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600 mb-1">Приватных каналов</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.private }}</p>
          </div>
          <el-icon :size="40" class="text-purple-500"><Lock /></el-icon>
        </div>
      </el-card>

      <el-card>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600 mb-1">Активных ботов</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.bots }}</p>
          </div>
          <el-icon :size="40" class="text-green-500"><Promotion /></el-icon>
        </div>
      </el-card>
    </div>

    <!-- Channels Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <el-card
        v-for="channel in channels"
        :key="channel.id"
        class="hover-lift"
      >
        <div class="flex items-start justify-between mb-4">
          <div class="flex items-center space-x-3">
            <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center">
              <el-icon :size="24" class="text-white"><Promotion /></el-icon>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900">{{ channel.title }}</h3>
              <p class="text-sm text-gray-500">{{ channel.username || 'Приватный канал' }}</p>
            </div>
          </div>
          <el-tag :type="channel.is_active ? 'success' : 'danger'" size="small">
            {{ channel.is_active ? 'Активен' : 'Неактивен' }}
          </el-tag>
        </div>

        <div class="space-y-2 mb-4 text-sm">
          <div class="flex justify-between">
            <span class="text-gray-500">Подписчиков:</span>
            <span class="font-medium">{{ channel.subscribers || 0 }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">Публикаций:</span>
            <span class="font-medium">{{ channel.post_count || 0 }}</span>
          </div>
        </div>

        <div class="flex items-center justify-between pt-4 border-t">
          <span class="text-xs text-gray-500">Бот: {{ channel.bot_name || 'N/A' }}</span>
          <div class="flex space-x-2">
            <el-button link type="primary" @click="editChannel(channel)">
              <el-icon><Edit /></el-icon>
            </el-button>
            <el-button link type="danger" @click="deleteChannel(channel)">
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
        </div>
      </el-card>

      <!-- Add Channel Card -->
      <el-card class="border-2 border-dashed border-gray-300 hover-lift cursor-pointer" @click="showAddDialog = true">
        <div class="text-center py-8">
          <div class="w-12 h-12 bg-gray-100 rounded-xl flex items-center justify-center mx-auto mb-4">
            <el-icon :size="24" class="text-gray-400"><Plus /></el-icon>
          </div>
          <h3 class="font-semibold text-gray-900 mb-2">Добавить канал</h3>
          <p class="text-sm text-gray-500">Подключите новый Telegram-канал к системе</p>
        </div>
      </el-card>
    </div>

    <!-- Add/Edit Dialog -->
    <el-dialog
      v-model="showAddDialog"
      :title="editingChannel ? 'Редактировать канал' : 'Добавить канал'"
      width="600px"
    >
      <el-form :model="channelForm" label-width="140px">
        <el-form-item label="Название канала">
          <el-input v-model="channelForm.title" placeholder="Введите название" />
        </el-form-item>

        <el-form-item label="@username или ссылка">
          <el-input v-model="channelForm.username" placeholder="@channel_username или https://t.me/..." />
        </el-form-item>

        <el-form-item label="Токен бота">
          <el-input v-model="channelForm.bot_token" type="password" show-password placeholder="Введите токен бота" />
        </el-form-item>

        <el-form-item>
          <el-checkbox v-model="channelForm.is_private">Приватный канал</el-checkbox>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showAddDialog = false">Отмена</el-button>
        <el-button type="primary" @click="handleChannelSubmit">Сохранить</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Plus, Promotion, Edit, Delete, Lock } from '@element-plus/icons-vue'
import { channelsApi } from '@/services/api'

const channels = ref([])
const stats = ref({
  public: 12,
  private: 8,
  bots: 15
})
const showAddDialog = ref(false)
const editingChannel = ref(null)

const channelForm = ref({
  title: '',
  username: '',
  bot_token: '',
  is_private: false
})

const loadChannels = async () => {
  try {
    const response = await channelsApi.getChannels()
    channels.value = response.data.items || []
  } catch (error) {
    console.error('Error loading channels:', error)
  }
}

const editChannel = (channel: any) => {
  editingChannel.value = channel
  channelForm.value = {
    title: channel.title,
    username: channel.username || '',
    bot_token: '',
    is_private: channel.is_private
  }
  showAddDialog.value = true
}

const deleteChannel = async (channel: any) => {
  // TODO: Add confirmation
  try {
    await channelsApi.deleteChannel(channel.id)
    loadChannels()
  } catch (error) {
    console.error('Error deleting channel:', error)
  }
}

const handleChannelSubmit = async () => {
  try {
    if (editingChannel.value) {
      await channelsApi.updateChannel(editingChannel.value.id, channelForm.value)
    } else {
      await channelsApi.createChannel({
        ...channelForm.value,
        chat_id: channelForm.value.username || 'temp'
      })
    }
    showAddDialog.value = false
    editingChannel.value = null
    channelForm.value = {
      title: '',
      username: '',
      bot_token: '',
      is_private: false
    }
    loadChannels()
  } catch (error) {
    console.error('Error saving channel:', error)
  }
}

onMounted(() => {
  loadChannels()
})
</script>

<style scoped>
.hover-lift {
  transition: all 0.3s ease;
}

.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}
</style>

