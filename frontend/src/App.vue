<template>
  <div id="app">
    <el-container>
      <el-header class="header">
        <h1>ETF看板</h1>
        <div class="timestamp">{{ currentTime }}</div>
      </el-header>
      
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'App',
  setup() {
    const currentTime = ref('')
    let timer = null
    
    // 格式化当前时间
    const formatCurrentTime = () => {
      const now = new Date()
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const hours = String(now.getHours()).padStart(2, '0')
      const minutes = String(now.getMinutes()).padStart(2, '0')
      const seconds = String(now.getSeconds()).padStart(2, '0')
      
      currentTime.value = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
    }
    
    onMounted(() => {
      // 初始化时间
      formatCurrentTime()
      timer = setInterval(formatCurrentTime, 1000)
    })
    
    onUnmounted(() => {
      if (timer) {
        clearInterval(timer)
      }
    })
    
    return {
      currentTime
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

body {
  margin: 0;
  padding: 0;
}

.header {
  background-color: #409EFF;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header h1 {
  margin: 0;
}

.timestamp {
  font-size: 16px;
}

.main-content {
  padding: 10px;
  background-color: #ffffff;
}
</style>