<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>Dashboard - 首页概览</h1>
      <div class="header-controls">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          @change="handleDateRangeChange"
          style="width: 300px"
        />
        <el-button
          type="primary"
          :icon="Refresh"
          @click="fetchMetrics"
        >
          刷新
        </el-button>
      </div>
    </div>
    
    <!-- 数据卡片 -->
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background-color: #ecf5ff;">
              <el-icon :size="40" color="#409eff"><Message /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ metrics.total_messages || 0 }}</div>
              <div class="stat-label">总消息数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background-color: #f0f9ff;">
              <el-icon :size="40" color="#67c23a"><CircleCheck /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ metrics.success_messages || 0 }}</div>
              <div class="stat-label">成功数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background-color: #fef0f0;">
              <el-icon :size="40" color="#f56c6c"><CircleClose /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ metrics.failed_messages || 0 }}</div>
              <div class="stat-label">失败数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background-color: #fdf6ec;">
              <el-icon :size="40" color="#e6a23c"><DataLine /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ successRate }}</div>
              <div class="stat-label">成功率</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 图表区 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>发送趋势</span>
          </template>
          <div id="trend-chart" style="height: 400px;"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 快捷操作 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <span>快捷操作</span>
          </template>
          <div class="quick-actions">
            <el-button
              type="primary"
              :icon="Message"
              @click="$router.push('/messages')"
            >
              查看消息
            </el-button>
            <el-button
              type="success"
              :icon="Document"
              @click="$router.push('/templates')"
            >
              管理模板
            </el-button>
            <el-button
              type="warning"
              :icon="Setting"
              @click="$router.push('/email-accounts')"
            >
              邮箱管理
            </el-button>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="16">
        <el-card>
          <template #header>
            <span>系统信息</span>
          </template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="服务状态">
              <el-tag type="success">运行中</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="版本">v1.0.0</el-descriptions-item>
            <el-descriptions-item label="后端API">http://localhost:8000</el-descriptions-item>
            <el-descriptions-item label="Flower监控">
              <el-link href="http://localhost:5555" target="_blank" type="primary">
                访问Flower
              </el-link>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { getSystemMetrics, type SystemMetrics } from '@/api/monitoring'
import { Refresh, Message, Document, Setting, CircleCheck, CircleClose, DataLine } from '@element-plus/icons-vue'

const metrics = ref<SystemMetrics>({
  total_messages: 0,
  success_messages: 0,
  failed_messages: 0,
  success_rate: 0,
  pending_messages: 0,
  hourly_stats: [],
})

let chartInstance: echarts.ECharts | null = null

// 日期范围，默认今天
const today = new Date().toISOString().split('T')[0]
const dateRange = ref<[string, string]>([today, today])

// 成功率格式化
const successRate = computed(() => {
  return `${(metrics.value.success_rate * 100).toFixed(2)}%`
})

// 日期范围改变处理
const handleDateRangeChange = () => {
  if (dateRange.value && dateRange.value.length === 2) {
    fetchMetrics()
  }
}

// 获取指标数据
const fetchMetrics = async () => {
  try {
    // 使用日期范围查询
    if (dateRange.value && dateRange.value.length === 2) {
      const [startDate, endDate] = dateRange.value
      const response = await getSystemMetrics(24, startDate, endDate)
      metrics.value = response.data
      renderChart()
    }
  } catch (error) {
    console.error('获取指标失败:', error)
  }
}

// 渲染图表
const renderChart = () => {
  if (!chartInstance) {
    const chartDom = document.getElementById('trend-chart')
    if (!chartDom) return
    chartInstance = echarts.init(chartDom)
  }

  if (!dateRange.value || dateRange.value.length !== 2) return

  const [startDate, endDate] = dateRange.value
  const start = new Date(startDate)
  const end = new Date(endDate)
  
  // 计算日期范围的天数
  const daysDiff = Math.floor((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24)) + 1
  
  // 准备24个刻度的标签和数据
  const labels: string[] = []
  const totalData: number[] = []
  const successData: number[] = []
  const failedData: number[] = []
  
  if (daysDiff === 1) {
    // 单日：24个刻度代表0-23点
    for (let hour = 0; hour < 24; hour++) {
      labels.push(`${hour}点`)
      
      // 从 hourly_stats 中查找对应的数据
      const hourStr = `${startDate} ${hour.toString().padStart(2, '0')}:00`
      const stat = metrics.value.hourly_stats?.find(item => item.hour === hourStr)
      
      totalData.push(stat?.total || 0)
      successData.push(stat?.success || 0)
      failedData.push(stat?.failed || 0)
    }
  } else {
    // 多日：24个刻度均匀分布在日期范围内
    const totalHours = daysDiff * 24
    const hoursPerTick = totalHours / 24
    
    for (let i = 0; i < 24; i++) {
      const tickHour = Math.floor(i * hoursPerTick)
      const tickDate = new Date(start.getTime() + tickHour * 60 * 60 * 1000)
      const dateStr = tickDate.toISOString().split('T')[0]
      const hour = tickDate.getHours()
      
      labels.push(`${dateStr.slice(5)} ${hour}点`)
      
      // 聚合该刻度范围内的数据
      let tickTotal = 0
      let tickSuccess = 0
      let tickFailed = 0
      
      const rangeStart = tickHour
      const rangeEnd = i === 23 ? totalHours : Math.floor((i + 1) * hoursPerTick)
      
      for (let h = rangeStart; h < rangeEnd; h++) {
        const rangeDate = new Date(start.getTime() + h * 60 * 60 * 1000)
        const rangeDateStr = rangeDate.toISOString().split('T')[0]
        const rangeHour = rangeDate.getHours()
        const hourStr = `${rangeDateStr} ${rangeHour.toString().padStart(2, '0')}:00`
        
        const stat = metrics.value.hourly_stats?.find(item => item.hour === hourStr)
        if (stat) {
          tickTotal += stat.total
          tickSuccess += stat.success
          tickFailed += stat.failed
        }
      }
      
      totalData.push(tickTotal)
      successData.push(tickSuccess)
      failedData.push(tickFailed)
    }
  }

  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        let result = `${labels[params[0].dataIndex]}<br/>`
        params.forEach((param: any) => {
          result += `${param.marker}${param.seriesName}: ${param.value}<br/>`
        })
        return result
      }
    },
    legend: {
      data: ['总数', '成功', '失败'],
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: labels,
    },
    yAxis: {
      type: 'value',
      min: 0,
      minInterval: 1,
      scale: false,
    },
    series: [
      {
        name: '总数',
        type: 'line',
        data: totalData,
        smooth: true,
      },
      {
        name: '成功',
        type: 'line',
        data: successData,
        smooth: true,
      },
      {
        name: '失败',
        type: 'line',
        data: failedData,
        smooth: true,
      },
    ],
  }

  chartInstance.setOption(option)
}

onMounted(() => {
  fetchMetrics()
  
  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    chartInstance?.resize()
  })
})

onUnmounted(() => {
  chartInstance?.dispose()
})
</script>

<style scoped>
.dashboard {
  width: 100%;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.dashboard-header h1 {
  margin: 0;
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-cards {
  margin-top: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: 8px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  margin-top: 8px;
  font-size: 14px;
  color: #909399;
}

.quick-actions {
  display: flex;
  flex-direction: row;
  gap: 12px;
  align-items: stretch;
}

.quick-actions .el-button {
  width: 100%;
  justify-content: flex-start;
}
</style>

