<template>
  <div class="templates-page">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>模板管理</span>
          <el-button type="primary" :icon="Plus" @click="handleAdd">新建模板</el-button>
        </div>
      </template>
      
      <!-- 模板列表 -->
      <el-table
        v-loading="loading"
        :data="templateList"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="code" label="模板编码" width="150" />
        <el-table-column prop="name" label="模板名称" width="150" />
        <el-table-column prop="type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.type === 'email'">邮件</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="subject_template" label="主题模板" show-overflow-tooltip />
        <el-table-column prop="version" label="版本" width="80" />
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.is_active" type="success">启用</el-tag>
            <el-tag v-else type="info">禁用</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="warning" size="small" link @click="handleHistory(row)">历史</el-button>
            <el-button type="danger" size="small" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新建/编辑模板对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="60%"
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="120px"
      >
        <el-form-item label="模板编码" prop="code">
          <el-input
            v-model="formData.code"
            placeholder="请输入模板编码（唯一标识）"
            :disabled="isEdit"
          />
        </el-form-item>
        
        <el-form-item label="模板名称" prop="name">
          <el-input
            v-model="formData.name"
            placeholder="请输入模板名称"
          />
        </el-form-item>
        
        <el-form-item label="模板类型" prop="type">
          <el-select
            v-model="formData.type"
            placeholder="请选择模板类型"
            :disabled="isEdit"
            style="width: 100%"
          >
            <el-option label="邮件" value="email" />
            <el-option label="短信" value="sms" disabled />
            <el-option label="微信" value="wechat" disabled />
          </el-select>
        </el-form-item>
        
        <el-form-item label="主题模板" prop="subject_template">
          <el-input
            v-model="formData.subject_template"
            placeholder="请输入主题模板（支持 Jinja2 语法，如：{{ username }}）"
          />
        </el-form-item>
        
        <el-form-item label="内容模板" prop="content_template">
          <el-input
            v-model="formData.content_template"
            type="textarea"
            :rows="10"
            placeholder="请输入内容模板（支持 Jinja2 语法和 HTML）"
          />
        </el-form-item>
        
        <el-form-item label="模板描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入模板描述"
          />
        </el-form-item>
        
        <el-form-item label="是否启用" prop="is_active">
          <el-switch v-model="formData.is_active" />
        </el-form-item>
        
        <el-form-item v-if="isEdit" label="变更原因" prop="change_reason">
          <el-input
            v-model="formData.change_reason"
            placeholder="请输入本次修改的原因"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 历史版本对话框 -->
    <el-dialog
      v-model="historyDialogVisible"
      title="历史版本"
      width="70%"
      :close-on-click-modal="false"
    >
      <el-table
        v-loading="historyLoading"
        :data="historyList"
        style="width: 100%"
      >
        <el-table-column prop="version" label="版本号" width="100" />
        <el-table-column prop="subject_template" label="主题模板" show-overflow-tooltip />
        <el-table-column prop="change_reason" label="变更原因" show-overflow-tooltip />
        <el-table-column prop="changed_by" label="变更人" width="120" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              link
              @click="handleViewHistory(row)"
            >
              查看详情
            </el-button>
            <el-button
              type="warning"
              size="small"
              link
              @click="handleRollback(row)"
            >
              回滚
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <!-- 历史版本详情对话框 -->
    <el-dialog
      v-model="historyDetailDialogVisible"
      title="版本详情"
      width="60%"
    >
      <el-descriptions :column="1" border v-if="currentHistory">
        <el-descriptions-item label="版本号">
          {{ currentHistory.version }}
        </el-descriptions-item>
        <el-descriptions-item label="主题模板">
          {{ currentHistory.subject_template }}
        </el-descriptions-item>
        <el-descriptions-item label="内容模板">
          <pre style="white-space: pre-wrap; max-height: 400px; overflow-y: auto;">{{ currentHistory.content_template }}</pre>
        </el-descriptions-item>
        <el-descriptions-item label="变更原因">
          {{ currentHistory.change_reason || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="变更人">
          {{ currentHistory.changed_by || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ formatDate(currentHistory.created_at) }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox, FormInstance, FormRules } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import {
  getTemplateList,
  createTemplate,
  updateTemplate,
  deleteTemplate,
  getTemplateHistory,
  rollbackTemplate,
  type Template,
  type TemplateHistory,
} from '@/api/template'
import dayjs from 'dayjs'

const loading = ref(false)
const templateList = ref<Template[]>([])

// 对话框相关
const dialogVisible = ref(false)
const isEdit = ref(false)
const currentTemplate = ref<Template | null>(null)
const formRef = ref<FormInstance>()
const submitLoading = ref(false)

// 表单数据
const formData = ref({
  code: '',
  name: '',
  type: 'email',
  subject_template: '',
  content_template: '',
  description: '',
  is_active: true,
  change_reason: '',
})

// 表单验证规则
const formRules: FormRules = {
  code: [
    { required: true, message: '请输入模板编码', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' },
  ],
  name: [
    { required: true, message: '请输入模板名称', trigger: 'blur' },
    { min: 2, max: 200, message: '长度在 2 到 200 个字符', trigger: 'blur' },
  ],
  type: [
    { required: true, message: '请选择模板类型', trigger: 'change' },
  ],
  subject_template: [
    { max: 500, message: '长度不能超过 500 个字符', trigger: 'blur' },
  ],
  content_template: [
    { required: true, message: '请输入内容模板', trigger: 'blur' },
  ],
}

// 历史版本相关
const historyDialogVisible = ref(false)
const historyLoading = ref(false)
const historyList = ref<TemplateHistory[]>([])
const currentHistoryTemplateId = ref<number | null>(null)

// 历史详情相关
const historyDetailDialogVisible = ref(false)
const currentHistory = ref<TemplateHistory | null>(null)

// 对话框标题
const dialogTitle = computed(() => {
  return isEdit.value ? '编辑模板' : '新建模板'
})

const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const fetchTemplateList = async () => {
  loading.value = true
  
  try {
    const response = await getTemplateList()
    templateList.value = response.data
  } catch (error) {
    console.error('获取模板列表失败:', error)
    ElMessage.error('获取模板列表失败')
  } finally {
    loading.value = false
  }
}

// 新建模板
const handleAdd = () => {
  isEdit.value = false
  currentTemplate.value = null
  formData.value = {
    code: '',
    name: '',
    type: 'email',
    subject_template: '',
    content_template: '',
    description: '',
    is_active: true,
    change_reason: '',
  }
  dialogVisible.value = true
}

// 编辑模板
const handleEdit = (row: Template) => {
  isEdit.value = true
  currentTemplate.value = row
  formData.value = {
    code: row.code,
    name: row.name,
    type: row.type,
    subject_template: row.subject_template || '',
    content_template: row.content_template,
    description: row.description || '',
    is_active: row.is_active,
    change_reason: '',
  }
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    
    submitLoading.value = true
    
    if (isEdit.value && currentTemplate.value) {
      // 编辑模板
      await updateTemplate(currentTemplate.value.id, {
        name: formData.value.name,
        subject_template: formData.value.subject_template,
        content_template: formData.value.content_template,
        description: formData.value.description,
        is_active: formData.value.is_active,
        change_reason: formData.value.change_reason,
      })
      ElMessage.success('模板更新成功')
    } else {
      // 新建模板
      await createTemplate({
        code: formData.value.code,
        name: formData.value.name,
        type: formData.value.type,
        subject_template: formData.value.subject_template,
        content_template: formData.value.content_template,
        description: formData.value.description,
        is_active: formData.value.is_active,
      })
      ElMessage.success('模板创建成功')
    }
    
    dialogVisible.value = false
    fetchTemplateList()
  } catch (error: any) {
    console.error('提交失败:', error)
    ElMessage.error(error.response?.data?.detail || '操作失败')
  } finally {
    submitLoading.value = false
  }
}

// 查看历史
const handleHistory = async (row: Template) => {
  currentHistoryTemplateId.value = row.id
  historyDialogVisible.value = true
  historyLoading.value = true
  
  try {
    const response = await getTemplateHistory(row.id)
    historyList.value = response.data
  } catch (error) {
    console.error('获取历史版本失败:', error)
    ElMessage.error('获取历史版本失败')
  } finally {
    historyLoading.value = false
  }
}

// 查看历史详情
const handleViewHistory = (row: TemplateHistory) => {
  currentHistory.value = row
  historyDetailDialogVisible.value = true
}

// 回滚模板
const handleRollback = async (row: TemplateHistory) => {
  if (!currentHistoryTemplateId.value) return
  
  try {
    await ElMessageBox.confirm(
      `确定要回滚到版本 ${row.version} 吗？`,
      '回滚模板',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await rollbackTemplate(currentHistoryTemplateId.value, row.version)
    ElMessage.success('回滚成功')
    
    historyDialogVisible.value = false
    fetchTemplateList()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('回滚失败:', error)
      ElMessage.error(error.response?.data?.detail || '回滚失败')
    }
  }
}

// 删除模板
const handleDelete = async (row: Template) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除模板 "${row.name}" 吗？`,
      '删除模板',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await deleteTemplate(row.id)
    ElMessage.success('删除成功')
    fetchTemplateList()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }
}

onMounted(() => {
  fetchTemplateList()
})
</script>

<style scoped>
.templates-page {
  width: 100%;
}
</style>

