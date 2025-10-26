/**
 * 应用状态管理
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  // 侧边栏是否折叠
  const sidebarCollapse = ref<boolean>(false)
  
  // 切换侧边栏
  function toggleSidebar() {
    sidebarCollapse.value = !sidebarCollapse.value
  }

  // 设置侧边栏状态
  function setSidebarCollapse(value: boolean) {
    sidebarCollapse.value = value
  }

  return {
    sidebarCollapse,
    toggleSidebar,
    setSidebarCollapse,
  }
})

