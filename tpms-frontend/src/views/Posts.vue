<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8">
      <div>
        <h2 class="text-3xl font-bold text-gray-900 mb-2">Публикации</h2>
        <p class="text-gray-600">Управление постами и контентом</p>
      </div>
      <el-button type="primary" size="large" @click="showCreateDialog = true">
        <el-icon><Plus /></el-icon>
        Создать пост
      </el-button>
    </div>

    <!-- Filters -->
    <el-card class="mb-8">
      <el-form :inline="true" :model="filters">
        <el-form-item label="Канал">
          <el-select v-model="filters.channelId" placeholder="Все каналы" clearable style="width: 200px">
            <el-option
              v-for="channel in channels"
              :key="channel.id"
              :label="channel.title"
              :value="channel.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="Статус">
          <el-select v-model="filters.status" placeholder="Все статусы" clearable style="width: 200px">
            <el-option label="Черновик" value="draft" />
            <el-option label="Запланировано" value="scheduled" />
            <el-option label="Опубликовано" value="published" />
            <el-option label="Ошибка" value="error" />
          </el-select>
        </el-form-item>

        <el-form-item label="Дата от">
          <el-date-picker
            v-model="filters.dateFrom"
            type="date"
            placeholder="Выберите дату"
            style="width: 200px"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="loadPosts">Применить фильтры</el-button>
          <el-button @click="resetFilters">Сбросить</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Posts Table -->
    <el-card>
      <el-table :data="posts" v-loading="loading" style="width: 100%">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="content" label="Заголовок" min-width="200">
          <template #default="{ row }">
            <div class="text-sm font-medium text-gray-900">{{ row.content.substring(0, 50) }}...</div>
            <div class="text-sm text-gray-500">{{ row.content.substring(50, 100) }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="channel_title" label="Канал" width="150" />
        <el-table-column prop="status" label="Статус" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="publish_at" label="Дата публикации" width="180">
          <template #default="{ row }">
            {{ row.publish_at ? formatDate(row.publish_at) : 'Не запланировано' }}
          </template>
        </el-table-column>
        <el-table-column prop="created_by_username" label="Автор" width="150" />
        <el-table-column label="Действия" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="editPost(row)">Редактировать</el-button>
            <el-button link type="danger" @click="deletePost(row)">Удалить</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="mt-4 flex justify-between items-center">
        <div class="text-sm text-gray-700">
          Показано {{ posts.length }} из {{ total }} записей
        </div>
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[25, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadPosts"
          @current-change="loadPosts"
        />
      </div>
    </el-card>

    <!-- Create/Edit Dialog -->
    <PostScheduleForm
      v-model="showCreateDialog"
      :title="editingPost ? 'Редактировать пост' : 'Создать пост'"
      @submit="handlePostSubmit"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { postsApi } from '@/services/api'
import PostScheduleForm from '@/components/posts/PostScheduleForm.vue'

const loading = ref(false)
const posts = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(25)
const showCreateDialog = ref(false)
const editingPost = ref(null)

const channels = ref([
  { id: 1, title: 'Tech News' },
  { id: 2, title: 'Бизнес' },
  { id: 3, title: 'Маркетинг' }
])

const filters = ref({
  channelId: null,
  status: null,
  dateFrom: null
})

const loadPosts = async () => {
  loading.value = true
  try {
    const response = await postsApi.getPosts({
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      ...filters.value
    })
    posts.value = response.data.items || []
    total.value = response.data.total || 0
  } catch (error) {
    console.error('Error loading posts:', error)
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filters.value = {
    channelId: null,
    status: null,
    dateFrom: null
  }
  loadPosts()
}

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    draft: 'info',
    scheduled: 'warning',
    published: 'success',
    error: 'danger',
    cancelled: 'info'
  }
  return types[status] || 'info'
}

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    draft: 'Черновик',
    scheduled: 'Запланировано',
    published: 'Опубликовано',
    error: 'Ошибка',
    cancelled: 'Отменено'
  }
  return labels[status] || status
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('ru-RU')
}

const editPost = (post: any) => {
  editingPost.value = post
  showCreateDialog.value = true
}

const deletePost = async (post: any) => {
  // TODO: Add confirmation dialog
  try {
    await postsApi.deletePost(post.id)
    loadPosts()
  } catch (error) {
    console.error('Error deleting post:', error)
  }
}

const handlePostSubmit = async (data: any) => {
  try {
    if (editingPost.value) {
      await postsApi.updatePost(editingPost.value.id, data)
    } else {
      await postsApi.createPost(data)
    }
    showCreateDialog.value = false
    editingPost.value = null
    loadPosts()
  } catch (error) {
    console.error('Error saving post:', error)
  }
}

onMounted(() => {
  loadPosts()
})
</script>



