<template>
  <div class="data-maintenance">
    <IndexWithDataManagement />
    <!-- <el-tabs v-model="activeTab" type="card" @tab-click="handleTabClick">
      <el-tab-pane label="指数数据管理" name="index-with-data">
        
      </el-tab-pane>
      <el-tab-pane label="历史数据管理" name="history">
        <HistoryManagement />
      </el-tab-pane>
    </el-tabs> -->
  </div>
</template>

<script>
import { ref } from 'vue'
import IndexWithDataManagement from '../components/data-maintenance/IndexWithDataManagement.vue'
import HistoryManagement from '../components/data-maintenance/HistoryManagement.vue'

export default {
  name: 'DataMaintenance',
  components: {
    IndexWithDataManagement,
    HistoryManagement
  },
  setup() {
    const activeTab = ref('index-with-data')
    
    const handleTabClick = (tab) => {
      console.log('切换到标签页:', tab.props.name)
    }
    
    return {
      activeTab,
      handleTabClick
    }
  }
}
</script>

<style scoped>
</style>