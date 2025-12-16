<template>
  <div class="bg-white rounded-2xl p-6 shadow-sm hover-lift">
    <div class="flex items-center justify-between mb-4">
      <div :class="`w-12 h-12 ${color} rounded-xl flex items-center justify-center`">
        <el-icon :size="24" class="text-white">
          <component :is="icon" />
        </el-icon>
      </div>
      <span v-if="trend" class="text-xs text-gray-500">{{ trend }}</span>
    </div>
    <h3 class="text-2xl font-bold text-gray-900 mb-1">{{ value }}</h3>
    <p class="text-gray-600 text-sm">{{ title }}</p>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

interface Props {
  title: string
  value: string | number
  icon: string
  color: string
  trend?: string
}

defineProps<Props>()
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



