<template>
  <div class="app-container">
    <el-header class="header">
      <div class="header-left">
        <h1>ETF点位看板</h1>
      </div>
      <div class="header-center">
        <div class="nav-links">
          <router-link to="/" class="nav-link" :class="{ active: activeIndex === '/' }">首页</router-link>
          <!-- <router-link to="/datamgr" class="nav-link" :class="{ active: activeIndex === '/datamgr' }">数据维护</router-link> -->
          <router-link to="/about" class="nav-link" :class="{ active: activeIndex === '/about' }">关于</router-link>
        </div>
      </div>
      <div class="header-right">
        <div class="timestamp">{{ currentTime }}</div>
      </div>
    </el-header>

    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const currentTime = ref('')
    const activeIndex = ref('/')
    const router = useRouter()
    const route = useRoute()
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

    // 监听路由变化，更新活动菜单项
    watch(() => route.path, (newPath) => {
      activeIndex.value = newPath
    }, { immediate: true })

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
      currentTime,
      activeIndex
    }
  }
}
</script>

<style>
* {
  box-sizing: border-box;
}

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
.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
.main-content {
  flex: 1;
}
.header {
  background-color: #409EFF;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
}

.header-left {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.header-left h1 {
  margin: 0;
  font-size: 20px;
}

.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
  min-width: 400px;
}

.header-right {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.nav-links {
  display: flex;
  justify-content: center;
  width: 100%;
  max-width: 600px;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0 20px;
  margin: 0 5px;
  height: 60px;
  line-height: 60px;
  display: inline-block;
  transition: all 0.3s;
  border-bottom: 2px solid transparent;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.active {
  border-bottom-color: white;
  background-color: white;
  color: #409EFF;
  font-weight: bold;
}

.timestamp {
  font-size: 16px;
}

.main-content {
  padding: 0;
}
</style>