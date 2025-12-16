<template>
  <div class="flex items-start space-x-3">
    <div :class="`w-8 h-8 ${iconColor} rounded-full flex items-center justify-center flex-shrink-0`">
      <el-icon :size="12" :class="iconTextColor">
        <component :is="icon" />
      </el-icon>
    </div>
    <div class="flex-1">
      <p class="text-sm text-gray-900">{{ title }}</p>
      <p class="text-xs text-gray-500">{{ description }} • {{ time }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, computed } from 'vue'

interface Props {
  type: 'create' | 'publish' | 'error' | 'edit'
  title: string
  description: string
  time: string
}

const props = defineProps<Props>()

const iconMap = {
  create: 'Plus',
  publish: 'Check',
  error: 'Warning',
  edit: 'Edit'
}

const colorMap = {
  create: { bg: 'bg-blue-100', text: 'text-blue-600' },
  publish: { bg: 'bg-green-100', text: 'text-green-600' },
  error: { bg: 'bg-red-100', text: 'text-red-600' },
  edit: { bg: 'bg-purple-100', text: 'text-purple-600' }
}

const icon = computed(() => iconMap[props.type] || 'Info')
const iconColor = computed(() => colorMap[props.type]?.bg || 'bg-gray-100')
const iconTextColor = computed(() => colorMap[props.type]?.text || 'text-gray-600')
</script>



