<template>
  <div class="home">
    <div class="dashboard-container">
      <div v-for="(item, index) in dashboardData.data" :key="item.indices" class="index-row">
        <div class="index-row-content">
          <div class="index-overview-section">
            <IndexOverviewSingle :index="item.indices" />
          </div>
          <div class="core-data-section">
            <CoreDataSingle :coreData="item.core_data" :index="item.indices" />
          </div>
          <div class="history-section">
            <HistorySingle :history="item.history" :index="item.indices" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import IndexOverviewSingle from '../components/IndexOverviewSingle.vue'
import CoreDataSingle from '../components/CoreDataSingle.vue'
import HistorySingle from '../components/HistorySingle.vue'
import { getDashboardData } from '@/api/index'

// 响应式数据
const dashboardData = ref({
  timestamp: '',
  data: []
})

let refreshTimer = null

// 获取看板数据
const fetchDashboardData = async (refreshRealtime = false) => {
  try {
    const response = await getDashboardData(refreshRealtime)
    console.log('获取的原始数据:', response)
    
    // 确保数据格式正确
    if (response && response.data) {
      // 新格式，包含success字段
      dashboardData.value = {
        timestamp: response.timestamp || new Date().toISOString(),
        data: response.data
      }
    } else {
      console.error('API返回数据格式不正确:', response)
      dashboardData.value = {
        timestamp: new Date().toISOString(),
        data: []
      }
    }
  } catch (error) {
    console.error('获取看板数据失败:', error)
  }
}

// 生命周期钩子
onMounted(() => {
  // 获取初始数据
  fetchDashboardData()
  
  // 设置定时刷新数据（每5分钟）
  refreshTimer = setInterval(fetchDashboardData, 5 * 60 * 1000)
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style scoped>

.home h1 {
  margin-bottom: 20px;
  color: #303133;
}

.dashboard-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px;
}

.index-row {
  background-color: #ffffff;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
}

.index-row-content {
  display: flex;
  gap: 10px;
  padding: 10px;
  min-width: fit-content;
}

/* 桌面端样式 */
@media (min-width: 1201px) {
  .index-row-content {
    width: 100%;
    overflow-x: visible;
  }
  
  .index-overview-section {
    width: 280px;
    flex-shrink: 0;
  }

  .core-data-section {
    flex: 3;
    min-width: 600px;
    flex-shrink: 0;
  }

  .history-section {
    width: 240px;
    flex-shrink: 0;
  }
}

/* 平板端样式 */
@media (max-width: 1200px) and (min-width: 769px) {
  .index-row {
    overflow-x: auto;
  }
  
  .index-overview-section {
    width: 260px;
    flex-shrink: 0;
  }

  .core-data-section {
    width: 500px;
    flex-shrink: 0;
  }

  .history-section {
    width: 220px;
    flex-shrink: 0;
  }
}

/* 移动端样式 */
@media (max-width: 768px) {
  .index-row {
    overflow-x: auto;
    /* 添加滚动条样式 */
    scrollbar-width: thin;
    scrollbar-color: #909399 #f5f7fa;
  }
  
  /* Webkit浏览器滚动条样式 */
  .index-row::-webkit-scrollbar {
    height: 6px;
  }
  
  .index-row::-webkit-scrollbar-track {
    background: #f5f7fa;
    border-radius: 3px;
  }
  
  .index-row::-webkit-scrollbar-thumb {
    background: #909399;
    border-radius: 3px;
  }
  
  .index-row::-webkit-scrollbar-thumb:hover {
    background: #606266;
  }
  
  .index-row-content {
    padding: 8px;
  }
  
  .index-overview-section {
    width: 240px;
    flex-shrink: 0;
  }

  .core-data-section {
    width: 450px;
    flex-shrink: 0;
  }

  .history-section {
    width: 200px;
    flex-shrink: 0;
  }
}
</style>