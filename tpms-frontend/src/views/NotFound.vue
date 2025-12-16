<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center px-4">
    <div class="text-center">
      <h1 class="text-9xl font-bold text-gray-300 mb-4">404</h1>
      <h2 class="text-3xl font-bold text-gray-900 mb-4">Страница не найдена</h2>
      <p class="text-gray-600 mb-8">Запрашиваемая страница не существует</p>
      <el-button type="primary" size="large" @click="$router.push('/')">
        Вернуться на главную
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
// NotFound page
</script>



