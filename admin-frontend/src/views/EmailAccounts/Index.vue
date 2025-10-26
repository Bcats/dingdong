<template>
  <div class="email-accounts-page">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>邮箱管理</span>
          <el-button type="primary" :icon="Plus" @click="handleAdd">添加邮箱</el-button>
        </div>
      </template>
      
      <!-- 邮箱列表 -->
      <el-table
        v-loading="loading"
        :data="emailAccountList"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="email" label="邮箱地址" width="220" />
        <el-table-column label="显示名称" width="220">
          <template #default="{ row }">
            {{ row.display_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="SMTP服务器" width="200">
          <template #default="{ row }">
            {{ row.smtp_host }}:{{ row.smtp_port }}
          </template>
        </el-table-column>
        <el-table-column label="今日发送" width="150">
          <template #default="{ row }">
            <div style="display: flex; align-items: center; gap: 8px;">
              <el-progress
                :percentage="Math.round((row.daily_sent_count / row.daily_limit) * 100)"
                :status="row.daily_sent_count >= row.daily_limit ? 'exception' : undefined"
                :stroke-width="8"
                style="flex: 1;"
              />
              <span style="white-space: nowrap; font-size: 12px; color: #606266;">
                {{ row.daily_sent_count }}/{{ row.daily_limit }}
              </span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="优先级" width="120" />
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-tag v-if="row.is_active && row.is_available" type="success">
              正常
            </el-tag>
            <el-tag v-else-if="row.is_active && !row.is_available" type="warning">
              不可用
            </el-tag>
            <el-tag v-else type="info">禁用</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button type="primary" size="small" link @click="handleEdit(row)">
                编辑
              </el-button>
              <el-button type="success" size="small" link @click="handleTest(row.id)">
                测试
              </el-button>
              <el-button type="danger" size="small" link @click="handleDelete(row)">
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑邮箱对话框 -->
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
        <el-form-item label="邮箱地址" prop="email">
          <el-input
            v-model="formData.email"
            placeholder="请输入邮箱地址"
            :disabled="isEdit"
          />
        </el-form-item>
        
        <el-form-item label="显示名称" prop="display_name">
          <el-input
            v-model="formData.display_name"
            placeholder="请输入显示名称（可选）"
          />
        </el-form-item>
        
        <el-form-item label="SMTP服务器" prop="smtp_host">
          <el-input
            v-model="formData.smtp_host"
            placeholder="例如：smtp.gmail.com"
          />
        </el-form-item>
        
        <el-form-item label="SMTP端口" prop="smtp_port">
          <el-input-number
            v-model="formData.smtp_port"
            :min="1"
            :max="65535"
            controls-position="right"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="SMTP用户名" prop="smtp_username">
          <el-input
            v-model="formData.smtp_username"
            placeholder="通常与邮箱地址相同"
          />
        </el-form-item>
        
        <el-form-item label="SMTP密码" prop="smtp_password">
          <el-input
            v-model="formData.smtp_password"
            type="password"
            show-password
            :placeholder="isEdit ? '不修改请留空' : '请输入SMTP密码或授权码'"
          />
        </el-form-item>
        
        <el-form-item label="使用TLS" prop="use_tls">
          <el-switch v-model="formData.use_tls" />
          <span style="margin-left: 10px; color: #909399; font-size: 12px;">
            SSL/TLS加密连接（推荐）
          </span>
        </el-form-item>
        
        <el-form-item label="每日限额" prop="daily_limit">
          <el-input-number
            v-model="formData.daily_limit"
            :min="1"
            :max="10000"
            controls-position="right"
            style="width: 100%"
          />
          <span style="margin-left: 10px; color: #909399; font-size: 12px;">
            每日最多发送邮件数量
          </span>
        </el-form-item>
        
        <el-form-item label="优先级" prop="priority">
          <el-input-number
            v-model="formData.priority"
            :min="0"
            :max="100"
            controls-position="right"
            style="width: 100%"
          />
          <span style="margin-left: 10px; color: #909399; font-size: 12px;">
            数字越大优先级越高
          </span>
        </el-form-item>
        
        <el-form-item label="是否启用" prop="is_active">
          <el-switch v-model="formData.is_active" />
        </el-form-item>
        
        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="formData.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息（可选）"
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

    <!-- 测试邮箱对话框 -->
    <el-dialog
      v-model="testDialogVisible"
      title="测试邮箱"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="testFormRef"
        :model="testFormData"
        :rules="testFormRules"
        label-width="100px"
      >
        <el-form-item label="测试类型">
          <el-radio-group v-model="testFormData.testType">
            <el-radio value="connection">仅测试连接</el-radio>
            <el-radio value="send_email">发送测试邮件</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item 
          v-if="testFormData.testType === 'send_email'" 
          label="收件人" 
          prop="test_email"
        >
          <el-input
            v-model="testFormData.test_email"
            placeholder="请输入测试邮件的收件人地址"
          />
          <div style="color: #909399; font-size: 12px; margin-top: 4px;">
            将发送一封测试邮件到此地址
          </div>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="testDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="testLoading" @click="handleTestSubmit">
          开始测试
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox, ElLoading, FormInstance, FormRules } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import {
  getEmailAccountList,
  createEmailAccount,
  updateEmailAccount,
  testEmailAccount,
  deleteEmailAccount,
  type EmailAccount,
  type EmailAccountCreate,
  type EmailAccountUpdate,
} from '@/api/emailAccount'

const loading = ref(false)
const emailAccountList = ref<EmailAccount[]>([])

// 对话框相关
const dialogVisible = ref(false)
const isEdit = ref(false)
const currentAccount = ref<EmailAccount | null>(null)
const formRef = ref<FormInstance>()
const submitLoading = ref(false)

// 测试对话框相关
const testDialogVisible = ref(false)
const testFormRef = ref<FormInstance>()
const testLoading = ref(false)
const currentTestAccountId = ref<number | null>(null)
const testFormData = ref({
  testType: 'connection',
  test_email: '',
})

// 表单数据
const formData = ref<EmailAccountCreate>({
  email: '',
  display_name: '',
  smtp_host: '',
  smtp_port: 465,
  smtp_username: '',
  smtp_password: '',
  use_tls: true,
  daily_limit: 500,
  priority: 10,
  is_active: true,
  remark: '',
})

// 表单验证规则
const formRules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' },
  ],
  smtp_host: [
    { required: true, message: '请输入SMTP服务器', trigger: 'blur' },
  ],
  smtp_port: [
    { required: true, message: '请输入SMTP端口', trigger: 'blur' },
  ],
  smtp_username: [
    { required: true, message: '请输入SMTP用户名', trigger: 'blur' },
  ],
  smtp_password: [
    {
      validator: (rule: any, value: any, callback: any) => {
        if (!isEdit.value && !value) {
          callback(new Error('请输入SMTP密码'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
  daily_limit: [
    { required: true, message: '请输入每日限额', trigger: 'blur' },
  ],
  priority: [
    { required: true, message: '请输入优先级', trigger: 'blur' },
  ],
}

// 测试表单验证规则
const testFormRules: FormRules = {
  test_email: [
    { required: true, message: '请输入收件人邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' },
  ],
}

// 对话框标题
const dialogTitle = computed(() => {
  return isEdit.value ? '编辑邮箱' : '添加邮箱'
})

const fetchEmailAccountList = async () => {
  loading.value = true
  
  try {
    const response = await getEmailAccountList()
    emailAccountList.value = response.data
  } catch (error) {
    console.error('获取邮箱列表失败:', error)
    ElMessage.error('获取邮箱列表失败')
  } finally {
    loading.value = false
  }
}

// 添加邮箱
const handleAdd = () => {
  isEdit.value = false
  currentAccount.value = null
  formData.value = {
    email: '',
    display_name: '',
    smtp_host: '',
    smtp_port: 465,
    smtp_username: '',
    smtp_password: '',
    use_tls: true,
    daily_limit: 500,
    priority: 10,
    is_active: true,
    remark: '',
  }
  dialogVisible.value = true
}

// 编辑邮箱
const handleEdit = (row: EmailAccount) => {
  isEdit.value = true
  currentAccount.value = row
  formData.value = {
    email: row.email,
    display_name: row.display_name || '',
    smtp_host: row.smtp_host,
    smtp_port: row.smtp_port,
    smtp_username: row.smtp_username,
    smtp_password: '', // 编辑时密码留空
    use_tls: row.use_tls,
    daily_limit: row.daily_limit,
    priority: row.priority,
    is_active: row.is_active,
    remark: row.remark || '',
  }
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    
    submitLoading.value = true
    
    if (isEdit.value && currentAccount.value) {
      // 编辑邮箱
      const updateData: EmailAccountUpdate = {
        display_name: formData.value.display_name,
        smtp_host: formData.value.smtp_host,
        smtp_port: formData.value.smtp_port,
        smtp_username: formData.value.smtp_username,
        use_tls: formData.value.use_tls,
        daily_limit: formData.value.daily_limit,
        priority: formData.value.priority,
        is_active: formData.value.is_active,
        remark: formData.value.remark,
      }
      
      // 只在密码不为空时更新密码
      if (formData.value.smtp_password) {
        updateData.smtp_password = formData.value.smtp_password
      }
      
      await updateEmailAccount(currentAccount.value.id, updateData)
      ElMessage.success('邮箱更新成功')
    } else {
      // 添加邮箱
      await createEmailAccount(formData.value)
      ElMessage.success('邮箱添加成功')
    }
    
    dialogVisible.value = false
    fetchEmailAccountList()
  } catch (error: any) {
    console.error('提交失败:', error)
    ElMessage.error(error.response?.data?.detail || '操作失败')
  } finally {
    submitLoading.value = false
  }
}

// 打开测试对话框
const handleTest = (id: number) => {
  currentTestAccountId.value = id
  testFormData.value = {
    testType: 'connection',
    test_email: '',
  }
  testDialogVisible.value = true
}

// 执行测试
const handleTestSubmit = async () => {
  if (!currentTestAccountId.value) return
  
  // 如果选择发送测试邮件，需要验证表单
  if (testFormData.value.testType === 'send_email') {
    if (!testFormRef.value) return
    try {
      await testFormRef.value.validate()
    } catch {
      return
    }
  }
  
  testLoading.value = true
  
  try {
    const loadingInstance = ElLoading.service({
      lock: true,
      text: testFormData.value.testType === 'send_email' 
        ? '正在发送测试邮件...' 
        : '正在测试连接...',
      background: 'rgba(0, 0, 0, 0.7)'
    })
    
    const response = await testEmailAccount(
      currentTestAccountId.value,
      testFormData.value.testType === 'send_email' ? testFormData.value.test_email : undefined
    )
    
    loadingInstance.close()
    
    // 检查响应状态（后端返回code=0表示成功）
    const testResult = response.data
    
    if (testResult.success) {
      const successMsg = testFormData.value.testType === 'send_email'
        ? `测试邮件发送成功！\n\n耗时: ${testResult.duration_ms}ms\n收件人: ${testFormData.value.test_email}\n\n请检查收件箱（包括垃圾邮件）`
        : `SMTP连接测试成功！\n\n耗时: ${testResult.duration_ms}ms\n服务器响应正常`
      
      ElMessageBox.alert(
        successMsg,
        '✅ 测试成功',
        {
          confirmButtonText: '确定',
          type: 'success',
          dangerouslyUseHTMLString: false,
        }
      )
      
      testDialogVisible.value = false
    } else {
      // 测试失败，显示详细错误信息
      const errorDetail = testResult.error || testResult.message || '未知错误'
      const errorMsg = `${testResult.message || '测试失败'}\n\n详细信息：\n${errorDetail}\n\n常见问题：\n• 检查SMTP服务器地址和端口是否正确\n• 确认用户名和密码（授权码）是否正确\n• 检查是否启用了TLS/SSL\n• 确认邮箱服务商是否允许SMTP访问`
      
      ElMessageBox.alert(
        errorMsg,
        '❌ 测试失败',
        {
          confirmButtonText: '确定',
          type: 'error',
          dangerouslyUseHTMLString: false,
        }
      )
    }
  } catch (error: any) {
    // 网络或其他错误
    const errorMsg = error.response?.data?.detail || error.message || '网络请求失败'
    ElMessageBox.alert(
      `请求失败，请检查：\n\n• 后端服务是否正常运行\n• 网络连接是否正常\n\n错误详情：\n${errorMsg}`,
      '❌ 请求错误',
      {
        confirmButtonText: '确定',
        type: 'error',
      }
    )
  } finally {
    testLoading.value = false
  }
}

const handleDelete = async (row: EmailAccount) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除邮箱 "${row.email}" 吗？`,
      '删除邮箱',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    try {
      await deleteEmailAccount(row.id)
      ElMessage.success('删除成功')
      fetchEmailAccountList()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  } catch {
    // 取消
  }
}

onMounted(() => {
  fetchEmailAccountList()
})
</script>

<style scoped>
.email-accounts-page {
  width: 100%;
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

