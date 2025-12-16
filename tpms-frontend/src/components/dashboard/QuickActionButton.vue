<template>
  <button
    :class="`flex items-center justify-center space-x-3 p-4 border-2 border-dashed border-gray-300 rounded-xl hover:border-${color}-400 hover:bg-${color}-50 transition-all`"
    @click="$emit('click')"
  >
    <el-icon :class="`text-${color}-600`">
      <component :is="icon" />
    </el-icon>
    <span class="text-gray-700 font-medium">{{ label }}</span>
  </button>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

interface Props {
  icon: string
  label: string
  color: string
}

defineProps<Props>()
defineEmits(['click'])
</script>



