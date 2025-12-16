<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8">
      <div>
        <h2 class="text-3xl font-bold text-gray-900 mb-2">Календарь публикаций</h2>
        <p class="text-gray-600">Планирование и расписание контента</p>
      </div>
      <div class="flex items-center space-x-4 mt-4 sm:mt-0">
        <el-button @click="previousMonth">
          <el-icon><ArrowLeft /></el-icon>
          Назад
        </el-button>
        <h3 class="text-xl font-semibold text-gray-900">{{ currentMonthYear }}</h3>
        <el-button @click="nextMonth">
          Вперед
          <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
      <!-- Calendar -->
      <div class="lg:col-span-3">
        <el-card>
          <el-calendar v-model="selectedDate">
            <template #date-cell="{ data }">
              <div class="calendar-day" :class="{ 'has-posts': hasPosts(data.day) }">
                <span>{{ data.day.split('-').slice(2).join('-') }}</span>
                <div v-if="hasPosts(data.day)" class="post-indicator"></div>
              </div>
            </template>
          </el-calendar>
        </el-card>
      </div>

      <!-- Sidebar -->
      <div class="space-y-6">
        <!-- Today's Posts -->
        <el-card>
          <template #header>
            <h3 class="text-lg font-semibold text-gray-900">Сегодня, {{ todayDate }}</h3>
          </template>
          <div class="space-y-4">
            <div
              v-for="post in todayPosts"
              :key="post.id"
              class="flex items-start space-x-3"
            >
              <div :class="`w-8 h-8 ${getPostIconColor(post.status)} rounded-lg flex items-center justify-center`">
                <el-icon :size="12" class="text-white">
                  <component :is="getPostIcon(post.status)" />
                </el-icon>
              </div>
              <div class="flex-1">
                <div class="flex items-center justify-between mb-1">
                  <h4 class="text-sm font-medium text-gray-900">{{ post.title }}</h4>
                  <span class="text-xs text-gray-500">{{ formatTime(post.publish_at) }}</span>
                </div>
                <p class="text-xs text-gray-600 mb-2">{{ post.channel_title }}</p>
                <el-tag :type="getStatusType(post.status)" size="small">
                  {{ getStatusLabel(post.status) }}
                </el-tag>
              </div>
            </div>
          </div>
        </el-card>

        <!-- Quick Actions -->
        <el-card>
          <template #header>
            <h3 class="text-lg font-semibold text-gray-900">Быстрые действия</h3>
          </template>
          <div class="space-y-3">
            <el-button style="width: 100%" @click="$router.push('/posts?action=create')">
              <el-icon><Plus /></el-icon>
              Создать пост
            </el-button>
            <el-button style="width: 100%" @click="showScheduleDialog = true">
              <el-icon><Calendar /></el-icon>
              Запланировать
            </el-button>
          </div>
        </el-card>
      </div>
    </div>

    <!-- Schedule Dialog -->
    <PostScheduleForm
      v-model="showScheduleDialog"
      title="Запланировать публикацию"
      @submit="handleSchedule"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ArrowLeft, ArrowRight, Plus, Calendar, Clock, Check, File } from '@element-plus/icons-vue'
import { postsApi } from '@/services/api'
import PostScheduleForm from '@/components/posts/PostScheduleForm.vue'

const selectedDate = ref(new Date())
const showScheduleDialog = ref(false)
const todayPosts = ref([])

const currentMonthYear = computed(() => {
  return selectedDate.value.toLocaleDateString('ru-RU', { month: 'long', year: 'numeric' })
})

const todayDate = computed(() => {
  return new Date().toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })
})

const hasPosts = (date: string) => {
  // TODO: Check if date has posts
  return false
}

const getPostIcon = (status: string) => {
  const icons: Record<string, string> = {
    scheduled: 'Clock',
    published: 'Check',
    draft: 'File'
  }
  return icons[status] || 'File'
}

const getPostIconColor = (status: string) => {
  const colors: Record<string, string> = {
    scheduled: 'bg-blue-100',
    published: 'bg-green-100',
    draft: 'bg-yellow-100'
  }
  return colors[status] || 'bg-gray-100'
}

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    draft: 'info',
    scheduled: 'warning',
    published: 'success',
    error: 'danger'
  }
  return types[status] || 'info'
}

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    draft: 'Черновик',
    scheduled: 'Запланировано',
    published: 'Опубликовано',
    error: 'Ошибка'
  }
  return labels[status] || status
}

const formatTime = (date: string) => {
  if (!date) return ''
  return new Date(date).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
}

const previousMonth = () => {
  const date = new Date(selectedDate.value)
  date.setMonth(date.getMonth() - 1)
  selectedDate.value = date
}

const nextMonth = () => {
  const date = new Date(selectedDate.value)
  date.setMonth(date.getMonth() + 1)
  selectedDate.value = date
}

const handleSchedule = async (data: any) => {
  try {
    await postsApi.createPost(data)
    showScheduleDialog.value = false
    loadTodayPosts()
  } catch (error) {
    console.error('Error scheduling post:', error)
  }
}

const loadTodayPosts = async () => {
  try {
    const today = new Date().toISOString().split('T')[0]
    const response = await postsApi.getPosts({
      date_from: today,
      date_to: today
    })
    todayPosts.value = response.data.items || []
  } catch (error) {
    console.error('Error loading today posts:', error)
  }
}

onMounted(() => {
  loadTodayPosts()
})
</script>

<style scoped>
.calendar-day {
  position: relative;
  min-height: 40px;
  padding: 4px;
}

.calendar-day.has-posts::after {
  content: '';
  position: absolute;
  bottom: 4px;
  left: 50%;
  transform: translateX(-50%);
  width: 6px;
  height: 6px;
  background-color: #3b82f6;
  border-radius: 50%;
}

.post-indicator {
  width: 6px;
  height: 6px;
  background-color: #3b82f6;
  border-radius: 50%;
  position: absolute;
  bottom: 2px;
  left: 50%;
  transform: translateX(-50%);
}
</style>



