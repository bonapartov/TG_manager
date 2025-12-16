<template>
  <el-dialog
    v-model="visible"
    :title="title"
    width="600px"
    @close="$emit('close')"
  >
    <el-form :model="form" label-width="120px">
      <el-form-item label="Канал">
        <el-select v-model="form.channelId" placeholder="Выберите канал" style="width: 100%">
          <el-option
            v-for="channel in channels"
            :key="channel.id"
            :label="channel.title"
            :value="channel.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="Текст поста">
        <el-input
          v-model="form.content"
          type="textarea"
          :rows="6"
          placeholder="Введите текст поста..."
        />
      </el-form-item>

      <el-form-item label="Форматирование">
        <el-radio-group v-model="form.parseMode">
          <el-radio value="Markdown">Markdown</el-radio>
          <el-radio value="HTML">HTML</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="Дата публикации">
        <el-date-picker
          v-model="form.publishAt"
          type="datetime"
          placeholder="Выберите дату и время"
          style="width: 100%"
        />
      </el-form-item>

      <el-form-item label="Настройки">
        <el-checkbox v-model="form.disableNotification">Отключить уведомления</el-checkbox>
        <el-checkbox v-model="form.protectContent">Защитить контент</el-checkbox>
        <el-checkbox v-model="form.hasSpoiler">Добавить спойлер</el-checkbox>
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="$emit('close')">Отмена</el-button>
      <el-button type="primary" @click="handleSubmit">Сохранить</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, watch } from 'vue'

interface Props {
  modelValue: boolean
  title?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Создать пост'
})

const emit = defineEmits(['update:modelValue', 'submit', 'close'])

const visible = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
  visible.value = val
})

watch(visible, (val) => {
  emit('update:modelValue', val)
})

const form = ref({
  channelId: null as number | null,
  content: '',
  parseMode: 'Markdown' as 'Markdown' | 'HTML',
  publishAt: null as Date | null,
  disableNotification: false,
  protectContent: false,
  hasSpoiler: false
})

const channels = ref([
  { id: 1, title: 'Tech News' },
  { id: 2, title: 'Бизнес' },
  { id: 3, title: 'Маркетинг' }
])

const handleSubmit = () => {
  emit('submit', form.value)
  visible.value = false
}
</script>



