<template>
  <div id="app">
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <h1>ETF看板</h1>
        </div>
        <div class="header-center">
          <el-menu mode="horizontal" :default-active="activeIndex" class="nav-menu" @select="handleSelect" style="width: 100%; max-width: 600px;">
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/data-maintenance">数据维护</el-menu-item>
            <el-menu-item index="/about">关于</el-menu-item>
          </el-menu>
        </div>
        <div class="header-right">
          <div class="timestamp">{{ currentTime }}</div>
        </div>
      </el-header>
      
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
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
    
    // 处理菜单选择
    const handleSelect = (index) => {
      router.push(index)
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
      activeIndex,
      handleSelect
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

.nav-menu {
  background-color: transparent;
  border-bottom: none;
  width: 100%;
  min-width: 400px;
  display: flex;
  justify-content: center;
}

.nav-menu .el-menu-item {
  color: white;
  border-bottom: 2px solid transparent;
  padding: 0 20px;  /* 增加左右内边距，使导航项分散 */
  margin: 0 5px;   /* 增加外边距，进一步分散导航项 */
}

.nav-menu .el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-menu .el-menu-item.is-active {
  border-bottom-color: white;
  background-color: white; /* 改为白色背景 */
  color: #409EFF; /* 文字颜色改为蓝色，与标题栏背景色匹配 */
  font-weight: bold; /* 加粗文字，使其更突出 */
}

.timestamp {
  font-size: 16px;
}

.main-content {
  padding: 10px;
  background-color: #ffffff;
}
</style>