<template>
  <div class="about-container">
    <div class="about-card">
      <h1 class="about-title">关于本站</h1>
      <div class="about-content">
        <h2>说明:</h2>
        <ul class="about-list">
          <li class="about-item">
            <i class="icon">⚠️</i>
            <span>本站只做数据展示使用，不构成投资建议，投资须谨慎!</span>
          </li>
          <li class="about-item">
            <i class="icon">🎨</i>
            <span>图表原创来源于新米练习菌，在此基础上进行了一定的修改</span>
          </li>
          <li class="about-item">
            <i class="icon">🐮</i>
            <span>E大牛逼 🍺</span>
          </li>
          <li class="about-item">
            <i class="icon">🔄</i>
            <span>数据还在完善中,不准确之处,请多多包涵!</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutPage'
}
</script>

<style scoped>
.about-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.about-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
  max-width: 600px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.about-title {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.about-content h2 {
  color: #444;
  margin-bottom: 20px;
  font-size: 1.5rem;
  border-bottom: 2px solid #667eea;
  padding-bottom: 10px;
  display: inline-block;
}

.about-list {
  list-style: none;
  padding: 0;
}

.about-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
  padding: 15px;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 10px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.about-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
}

.about-item .icon {
  font-size: 1.5rem;
  margin-right: 15px;
  flex-shrink: 0;
}

.about-item span {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #555;
}

.about-footer {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.about-footer p {
  color: #777;
  font-size: 1.1rem;
  font-style: italic;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .about-card {
    padding: 20px;
    margin: 10px;
  }

  .about-title {
    font-size: 2rem;
  }

  .about-content h2 {
    font-size: 1.3rem;
  }

  .about-item span {
    font-size: 1rem;
  }
}
</style>