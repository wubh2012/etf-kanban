<template>
  <div class="home">
    <div class="dashboard-container">
      <div v-for="(item, index) in dashboardData.data" :key="item.indices.code" class="index-row">
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
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import IndexOverviewSingle from '../components/IndexOverviewSingle.vue'
import CoreDataSingle from '../components/CoreDataSingle.vue'
import HistorySingle from '../components/HistorySingle.vue'
import { getDashboardData } from '../services/api'

export default {
  name: 'HomePage',
  components: {
    IndexOverviewSingle,
    CoreDataSingle,
    HistorySingle
  },
  setup() {
    const dashboardData = ref({
      timestamp: '',
      data: []
    })
    
    let refreshTimer = null
    
    // 获取看板数据
    const fetchDashboardData = async () => {
      try {
        const data = await getDashboardData()
        console.log('获取的原始数据:', data)
        dashboardData.value = data
      } catch (error) {
        console.error('获取看板数据失败:', error)
      }
    }
    
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
    
    return {
      dashboardData
    }
  }
}
</script>

<style scoped>

.home h1 {
  margin-bottom: 20px;
  color: #303133;
}

.dashboard-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.index-row {
  display: flex;
  gap: 10px;
  background-color: #ffffff;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  /* padding: 10px; */
}

.index-overview-section {
  flex: 1;
  width: 300px;
}

.core-data-section {
  flex: 3;
  min-width: 600px;
}

.history-section {
  flex: 1;
  width: 240px;
}

/* 响应式布局 */
@media (max-width: 1200px) {
  
  .index-overview-section,
  .core-data-section,
  .history-section {
    min-width: auto;
  }
}
</style>