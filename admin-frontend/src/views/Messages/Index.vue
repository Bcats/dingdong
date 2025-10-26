<template>
  <div class="messages-page">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>消息管理</span>
          <div style="display: flex; gap: 12px;">
            <el-button 
              type="warning" 
              :icon="RefreshRight" 
              @click="handleBatchRetry"
              :disabled="selectedIds.length === 0"
            >
              批量重试 ({{ selectedIds.length }})
            </el-button>
            <el-button 
              type="danger" 
              :icon="Delete" 
              @click="handleBatchDelete"
              :disabled="selectedIds.length === 0"
            >
              批量删除 ({{ selectedIds.length }})
            </el-button>
            <el-button type="success" :icon="Download" @click="handleExport">
              导出数据
            </el-button>
          </div>
        </div>
      </template>
      
      <!--筛选表单 -->
      <el-form :inline="true" :model="queryParams" class="query-form">
        <el-form-item label="状态">
          <el-select v-model="queryParams.status" placeholder="全部" clearable style="width: 150px">
            <el-option label="待发送" value="pending" />
            <el-option label="发送中" value="sending" />
            <el-option label="成功" value="success" />
            <el-option label="失败" value="failed" />
            <el-option label="重试中" value="retrying" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="渠道">
          <el-select v-model="queryParams.channel" placeholder="全部" clearable style="width: 150px">
            <el-option label="邮件" value="email" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="dateRange"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 380px"
          />
        </el-form-item>
        
        <el-form-item label="收件人">
          <el-input 
            v-model="queryParams.to" 
            placeholder="输入收件人邮箱" 
            clearable 
            style="width: 200px"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="handleQuery">查询</el-button>
          <el-button :icon="Refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 消息列表表格 -->
      <el-table
        v-loading="loading"
        :data="messageList"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="channel" label="渠道" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.channel === 'email'" type="info">邮件</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="to" label="收件人" width="200" show-overflow-tooltip />
        <el-table-column prop="subject" label="主题" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.status === 'success'" type="success">成功</el-tag>
            <el-tag v-else-if="row.status === 'failed'" type="danger">失败</el-tag>
            <el-tag v-else-if="row.status === 'sending'" type="warning">发送中</el-tag>
            <el-tag v-else-if="row.status === 'retrying'" type="warning">重试中</el-tag>
            <el-tag v-else>待发送</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="重试次数" width="100">
          <template #default="{ row }">
            <el-text v-if="row.retry_count > 0" type="warning">
              {{ row.retry_count }}/{{ row.max_retry }}
            </el-text>
            <el-text v-else type="info">-</el-text>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button type="primary" size="small" link @click="handleDetail(row.id)">
                详情
              </el-button>
              <el-button 
                v-if="row.status === 'failed'"
                type="warning" 
                size="small" 
                link 
                @click="handleRetry(row.id)"
              >
                重试
              </el-button>
              <el-button type="danger" size="small" link @click="handleDelete(row.id)">
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <el-pagination
        v-model:current-page="queryParams.page"
        v-model:page-size="queryParams.page_size"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleQuery"
        @current-change="handleQuery"
        style="margin-top: 20px; justify-content: flex-end;"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, ElLoading } from 'element-plus'
import { Search, Refresh, RefreshRight, Delete, Download } from '@element-plus/icons-vue'
import { getMessageList, retryMessage, deleteMessage, type Message } from '@/api/message'
import dayjs from 'dayjs'

const router = useRouter()

const loading = ref(false)
const messageList = ref<Message[]>([])
const total = ref(0)
const selectedIds = ref<number[]>([])
const dateRange = ref<[string, string] | null>(null)

const queryParams = ref({
  page: 1,
  page_size: 20,
  status: '',
  channel: '',
  to: '',
})

// 格式化日期
const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

// 选择变化
const handleSelectionChange = (selection: Message[]) => {
  selectedIds.value = selection.map(item => item.id)
}

// 查询消息列表
const fetchMessageList = async () => {
  loading.value = true
  
  try {
    const params: any = {
      page: queryParams.value.page,
      page_size: queryParams.value.page_size,
    }
    
    if (queryParams.value.status) {
      params.status = queryParams.value.status
    }
    if (queryParams.value.channel) {
      params.channel = queryParams.value.channel
    }
    if (queryParams.value.to) {
      params.to = queryParams.value.to
    }
    
    // 添加时间范围筛选
    if (dateRange.value && dateRange.value.length === 2) {
      params.start_time = dateRange.value[0]
      params.end_time = dateRange.value[1]
    }
    
    const response = await getMessageList(params)
    messageList.value = response.data.items
    total.value = response.data.pagination.total
  } catch (error) {
    console.error('获取消息列表失败:', error)
    ElMessage.error('获取消息列表失败')
  } finally {
    loading.value = false
  }
}

// 查询
const handleQuery = () => {
  queryParams.value.page = 1
  fetchMessageList()
}

// 重置
const handleReset = () => {
  queryParams.value = {
    page: 1,
    page_size: 20,
    status: '',
    channel: '',
    to: '',
  }
  dateRange.value = null
  selectedIds.value = []
  fetchMessageList()
}

// 查看详情
const handleDetail = (id: number) => {
  router.push(`/messages/${id}`)
}

// 重试单条消息
const handleRetry = async (id: number) => {
  try {
    await ElMessageBox.confirm(
      '确定要重试该消息吗？',
      '重试消息',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    const loadingInstance = ElLoading.service({
      lock: true,
      text: '正在重试...',
      background: 'rgba(0, 0, 0, 0.7)'
    })
    
    try {
      await retryMessage(id)
      loadingInstance.close()
      ElMessage.success('重试请求已提交')
      fetchMessageList()
    } catch (error) {
      loadingInstance.close()
      ElMessage.error('重试失败')
    }
  } catch {
    // 取消
  }
}

// 批量重试
const handleBatchRetry = async () => {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请先选择要重试的消息')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      `确定要重试选中的 ${selectedIds.value.length} 条消息吗？`,
      '批量重试',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    const loadingInstance = ElLoading.service({
      lock: true,
      text: '正在批量重试...',
      background: 'rgba(0, 0, 0, 0.7)'
    })
    let successCount = 0
    let failCount = 0
    
    for (const id of selectedIds.value) {
      try {
        await retryMessage(id)
        successCount++
      } catch (error) {
        failCount++
      }
    }
    
    loadingInstance.close()
    
    if (failCount === 0) {
      ElMessage.success(`批量重试成功，共 ${successCount} 条`)
    } else {
      ElMessage.warning(`批量重试完成：成功 ${successCount} 条，失败 ${failCount} 条`)
    }
    
    selectedIds.value = []
    fetchMessageList()
  } catch {
    // 取消
  }
}

// 删除单条消息
const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该消息吗？删除后无法恢复。',
      '删除消息',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await deleteMessage(id)
    ElMessage.success('删除成功')
    fetchMessageList()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }
}

// 批量删除
const handleBatchDelete = async () => {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请先选择要删除的消息')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedIds.value.length} 条消息吗？删除后无法恢复。`,
      '批量删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    const loadingInstance = ElLoading.service({
      lock: true,
      text: '正在批量删除...',
      background: 'rgba(0, 0, 0, 0.7)'
    })
    let successCount = 0
    let failCount = 0
    
    for (const id of selectedIds.value) {
      try {
        await deleteMessage(id)
        successCount++
      } catch (error) {
        failCount++
      }
    }
    
    loadingInstance.close()
    
    if (failCount === 0) {
      ElMessage.success(`批量删除成功，共 ${successCount} 条`)
    } else {
      ElMessage.warning(`批量删除完成：成功 ${successCount} 条，失败 ${failCount} 条`)
    }
    
    selectedIds.value = []
    fetchMessageList()
  } catch {
    // 取消
  }
}

// 导出数据
const handleExport = async () => {
  try {
    const params: any = {}
    
    if (queryParams.value.status) {
      params.status = queryParams.value.status
    }
    if (queryParams.value.channel) {
      params.channel = queryParams.value.channel
    }
    if (queryParams.value.to) {
      params.to = queryParams.value.to
    }
    if (dateRange.value && dateRange.value.length === 2) {
      params.start_time = dateRange.value[0]
      params.end_time = dateRange.value[1]
    }
    
    const loadingInstance = ElLoading.service({
      lock: true,
      text: '正在导出数据...',
      background: 'rgba(0, 0, 0, 0.7)'
    })
    
    try {
      // 获取所有数据（不分页）
      const response = await getMessageList({ ...params, page: 1, page_size: 10000 })
      
      // 生成CSV内容
      const csvContent = generateCSV(response.data.items)
      
      // 下载文件
      const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      const url = URL.createObjectURL(blob)
      link.setAttribute('href', url)
      link.setAttribute('download', `messages_${dayjs().format('YYYY-MM-DD_HH-mm-ss')}.csv`)
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      loadingInstance.close()
      ElMessage.success('导出成功')
    } catch (error) {
      loadingInstance.close()
      ElMessage.error('导出失败')
    }
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

// 生成CSV内容
const generateCSV = (data: Message[]) => {
  const headers = ['ID', '渠道', '收件人', '主题', '状态', '重试次数', '创建时间', '发送时间', '错误信息']
  const rows = data.map(item => [
    item.id,
    item.channel === 'email' ? '邮件' : item.channel,
    item.to,
    `"${(item.subject || '').replace(/"/g, '""')}"`,
    getStatusText(item.status),
    `="${item.retry_count || 0}/${item.max_retry || 3}"`,  // 使用 ="x/x" 格式，强制Excel识别为文本
    formatDate(item.created_at),
    item.sent_at ? formatDate(item.sent_at) : '',
    `"${(item.error_message || '').replace(/"/g, '""')}"`,
  ])
  
  return [headers.join(','), ...rows.map(row => row.join(','))].join('\n')
}

// 获取状态文本
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    pending: '待发送',
    sending: '发送中',
    success: '成功',
    failed: '失败',
    retrying: '重试中',
  }
  return statusMap[status] || status
}

onMounted(() => {
  fetchMessageList()
})
</script>

<style scoped>
.messages-page {
  width: 100%;
}

.query-form {
  margin-bottom: 20px;
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
}

.action-buttons .el-button + .el-button {
  margin-left: 0;
}
</style>

