<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8 slide-in">
      <h2 class="text-3xl font-bold text-gray-900 mb-2">Панель управления</h2>
      <p class="text-gray-600">Общая статистика и график публикаций</p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <StatCard
        v-for="stat in stats"
        :key="stat.title"
        :title="stat.title"
        :value="stat.value"
        :icon="stat.icon"
        :color="stat.color"
        :trend="stat.trend"
        class="slide-in"
      />
    </div>

    <!-- Charts and Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
      <!-- Chart -->
      <div class="lg:col-span-2 bg-white rounded-2xl p-6 shadow-sm slide-in">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">График публикаций за 7 дней</h3>
        <div ref="chartContainer" class="h-80"></div>
      </div>

      <!-- Recent Activity -->
      <div class="bg-white rounded-2xl p-6 shadow-sm slide-in">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">Последние действия</h3>
        <div class="space-y-4">
          <ActivityItem
            v-for="activity in activities"
            :key="activity.id"
            :type="activity.type"
            :title="activity.title"
            :description="activity.description"
            :time="activity.time"
          />
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="bg-white rounded-2xl p-6 shadow-sm slide-in">
      <h3 class="text-lg font-semibold text-gray-900 mb-6">Быстрые действия</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <QuickActionButton
          title="Создать пост"
          description="Новая публикация"
          icon="Plus"
          color="blue"
          @click="$router.push('/posts/new')"
        />
        <QuickActionButton
          title="Запланировать"
          description="Отложенная публикация"
          icon="Calendar"
          color="green"
          @click="showScheduleModal = true"
        />
        <QuickActionButton
          title="Добавить канал"
          description="Новый Telegram-канал"
          icon="Plus"
          color="purple"
          @click="$router.push('/channels/new')"
        />
      </div>
    </div>

    <!-- Schedule Modal -->
    <el-dialog v-model="showScheduleModal" title="Запланировать публикацию" width="600px">
      <PostScheduleForm @cancel="showScheduleModal = false" @submit="handleScheduleSubmit" />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import StatCard from '@/components/dashboard/StatCard.vue'
import ActivityItem from '@/components/dashboard/ActivityItem.vue'
import QuickActionButton from '@/components/dashboard/QuickActionButton.vue'
import PostScheduleForm from '@/components/posts/PostScheduleForm.vue'

use([LineChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

const chartContainer = ref<HTMLElement>()
const showScheduleModal = ref(false)

// Mock data - in real app this would come from API
const stats = ref([
  {
    title: 'Черновики',
    value: 24,
    icon: 'Document',
    color: 'yellow',
    trend: '+12 сегодня'
  },
  {
    title: 'Запланировано',
    value: 156,
    icon: 'Clock',
    color: 'blue',
    trend: '+5 сегодня'
  },
  {
    title: 'Опубликовано',
    value: 1247,
    icon: 'Check',
    color: 'green',
    trend: '+89 сегодня'
  },
  {
    title: 'Ошибки',
    value: 8,
    icon: 'Warning',
    color: 'red',
    trend: '-3 сегодня'
  }
])

const activities = ref([
  {
    id: 1,
    type: 'create',
    title: 'Создан новый пост',
    description: 'в канале "Tech News" • 2 мин назад',
    time: '2 мин назад'
  },
  {
    id: 2,
    type: 'success',
    title: 'Публикация выполнена',
    description: 'в канале "Бизнес" • 15 мин назад',
    time: '15 мин назад'
  },
  {
    id: 3,
    type: 'error',
    title: 'Ошибка публикации',
    description: 'в канале "Новости" • 1 час назад',
    time: '1 час назад'
  },
  {
    id: 4,
    type: 'edit',
    title: 'Редактирование поста',
    description: 'в канале "Маркетинг" • 2 часа назад',
    time: '2 часа назад'
  }
])

const initChart = () => {
  if (!chartContainer.value) return

  const chart = echarts.init(chartContainer.value)
  
  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e5e7eb',
      borderWidth: 1,
      textStyle: {
        color: '#374151'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['11.06', '12.06', '13.06', '14.06', '15.06', '16.06', '17.06'],
      axisLine: {
        lineStyle: {
          color: '#e5e7eb'
        }
      },
      axisLabel: {
        color: '#6b7280'
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: '#e5e7eb'
        }
      },
      axisLabel: {
        color: '#6b7280'
      },
      splitLine: {
        lineStyle: {
          color: '#f3f4f6'
        }
      }
    },
    series: [
      {
        name: 'Опубликовано',
        type: 'line',
        smooth: true,
        data: [45, 52, 38, 67, 73, 89, 95],
        lineStyle: {
          color: '#3b82f6',
          width: 3
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(59, 130, 246, 0.3)' },
              { offset: 1, color: 'rgba(59, 130, 246, 0.05)' }
            ]
          }
        },
        itemStyle: {
          color: '#3b82f6'
        }
      },
      {
        name: 'Запланировано',
        type: 'line',
        smooth: true,
        data: [32, 41, 45, 52, 48, 56, 62],
        lineStyle: {
          color: '#8b5cf6',
          width: 3
        },
        itemStyle: {
          color: '#8b5cf6'
        }
      }
    ]
  }

  chart.setOption(option)

  // Make chart responsive
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

const handleScheduleSubmit = (formData: any) => {
  console.log('Schedule post:', formData)
  showScheduleModal.value = false
  // In real app, this would call API
}

onMounted(() => {
  initChart()
})
</script>