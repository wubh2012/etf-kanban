<template>
  <div class="app-container">
    <div class="header">
      <div class="header-left">
        <div class="hamburger-menu" @click="toggleMobileMenu">
          <div class="hamburger-line"></div>
          <div class="hamburger-line"></div>
          <div class="hamburger-line"></div>
        </div>        
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
    </div>

    <!-- 移动端菜单 -->
    <div class="mobile-menu" :class="{ 'mobile-menu-active': isMobileMenuOpen }">
      <div class="mobile-nav-links">
        <router-link to="/" class="mobile-nav-link" :class="{ active: activeIndex === '/' }" @click="closeMobileMenu">首页</router-link>
        <!-- <router-link to="/datamgr" class="mobile-nav-link" :class="{ active: activeIndex === '/datamgr' }" @click="closeMobileMenu">数据维护</router-link> -->
        <router-link to="/about" class="mobile-nav-link" :class="{ active: activeIndex === '/about' }" @click="closeMobileMenu">关于</router-link>
      </div>
    </div>

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
    const isMobileMenuOpen = ref(false)
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

    // 切换移动端菜单
    const toggleMobileMenu = () => {
      isMobileMenuOpen.value = !isMobileMenuOpen.value
    }

    // 关闭移动端菜单
    const closeMobileMenu = () => {
      isMobileMenuOpen.value = false
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
      isMobileMenuOpen,
      toggleMobileMenu,
      closeMobileMenu
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
  overflow-x: hidden;
}
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.main-content {
  flex: 1;
  width: 100%;
}
.header {
  background-color: #409EFF;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  position: relative;
  z-index: 1000;
}

.header-left {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.header-left h1 {
  margin: 0;
  font-size: 22px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
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
  transition: all 0.3s ease;
  border-bottom: 2px solid transparent;
  font-weight: 500;
  font-size: 16px;
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
  font-size: 15px;
  font-weight: 400;
  letter-spacing: 0.3px;
}

.main-content {
  padding: 0;
}

/* 汉堡菜单样式 */
.hamburger-menu {
  display: none;
  flex-direction: column;
  cursor: pointer;
  margin-right: 18px;
  padding: 8px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.hamburger-menu:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.hamburger-line {
  width: 22px;
  height: 2.5px;
  background-color: white;
  margin: 2.5px 0;
  transition: 0.3s;
  border-radius: 1px;
}

/* 移动端菜单样式 */
.mobile-menu {
  position: fixed;
  top: 60px;
  left: -100%;
  width: 100%;
  height: calc(100vh - 60px);
  background-color: #409EFF;
  transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 999;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.mobile-menu-active {
  left: 0;
}

.mobile-nav-links {
  display: flex;
  flex-direction: column;
  padding: 24px 20px;
}

.mobile-nav-link {
  color: white;
  text-decoration: none;
  padding: 16px 0;
  font-size: 17px;
  font-weight: 500;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  transition: all 0.3s ease;
  letter-spacing: 0.3px;
}

.mobile-nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.mobile-nav-link.active {
  color: #fff;
  font-weight: bold;
  background-color: rgba(255, 255, 255, 0.2);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hamburger-menu {
    display: flex;
  }
  
  .header-center {
    display: none;
  }
  
  .header-left h1 {
    font-size: 18px;
    font-weight: 600;
  }
  
  .timestamp {
    font-size: 13px;
    font-weight: 400;
  }
  
  .header {
    padding: 0 16px;
    height: 56px;
  }
  
  .mobile-menu {
    top: 56px;
    height: calc(100vh - 56px);
  }
}

@media (max-width: 480px) {
  .header-left h1 {
    font-size: 16px;
    font-weight: 600;
  }
  
  .timestamp {
    font-size: 12px;
    font-weight: 400;
  }
  
  .hamburger-line {
    width: 20px;
    height: 2px;
    margin: 2px 0;
  }
  
  .mobile-nav-link {
    font-size: 16px;
    padding: 14px 0;
  }
  
  .header {
    padding: 0 14px;
    height: 54px;
  }
  
  .mobile-menu {
    top: 54px;
    height: calc(100vh - 54px);
  }
}
</style>