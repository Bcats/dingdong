<template>
  <div class="message-detail">
    <el-page-header @back="handleBack" title="返回">
      <template #content>
        <span class="text-large font-600 mr-3">消息详情</span>
      </template>
    </el-page-header>
    
    <el-card style="margin-top: 20px;" v-loading="loading">
      <template #header>
        <span>基本信息</span>
      </template>
      
      <el-descriptions :column="2" border v-if="message">
        <el-descriptions-item label="消息ID">{{ message.id }}</el-descriptions-item>
        <el-descriptions-item label="渠道">
          <el-tag v-if="message.channel === 'email'">邮件</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag v-if="message.status === 'success'" type="success">成功</el-tag>
          <el-tag v-else-if="message.status === 'failed'" type="danger">失败</el-tag>
          <el-tag v-else-if="message.status === 'sending'" type="warning">发送中</el-tag>
          <el-tag v-else>待发送</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="收件人">{{ message.to }}</el-descriptions-item>
        <el-descriptions-item label="主题" :span="2">{{ message.subject }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDate(message.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="发送时间">
          {{ message.sent_at ? formatDate(message.sent_at) : '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="错误信息" :span="2" v-if="message.error_message">
          <el-text type="danger">{{ message.error_message }}</el-text>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
    
    <el-card style="margin-top: 20px;">
      <template #header>
        <span>消息内容</span>
      </template>
      <div v-if="message" v-html="message.content" class="message-content"></div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getMessageDetail, type Message } from '@/api/message'
import dayjs from 'dayjs'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const message = ref<Message | null>(null)

const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const fetchMessageDetail = async () => {
  const id = parseInt(route.params.id as string)
  
  loading.value = true
  try {
    const response = await getMessageDetail(id)
    message.value = response.data
  } catch (error) {
    console.error('获取消息详情失败:', error)
    ElMessage.error('获取消息详情失败')
  } finally {
    loading.value = false
  }
}

const handleBack = () => {
  router.back()
}

onMounted(() => {
  fetchMessageDetail()
})
</script>

<style scoped>
.message-content {
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
  min-height: 200px;
}
</style>

