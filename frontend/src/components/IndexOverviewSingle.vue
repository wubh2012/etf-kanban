<template>
  <div class="index-overview-single">
    <div class="index-header-row">
      <div class="index-name-code">
        <div class="index-name"><a :href="getIndexUrl()" target="_blank" class="index-link">{{ index.name }}</a></div>
        <div class="index-code"><a :href="getIndexUrl()" target="_blank" class="index-link">{{ index.code }}</a></div>
      </div>
      <div class="index-value-container">
        <div class="index-current-value">{{ index.current_point }}</div>
        <div class="update-time" v-if="index.updated_at">更新时间: {{ formatUpdateTime(index.updated_at) }}</div>
      </div>
    </div>
    <div class="percentage-info">
      <div class="percentage-item">
        <span class="percentage-label">距离支撑点位:</span>
        <span class="percentage-value support-distance"
          :style="{ color: calculateSupportDistance() > 0 ? 'red' : '#00AF50' }">{{ calculateSupportDistance()
          }}%</span>
      </div>
      <div class="percentage-item" v-if="index.pressure_point">
        <span class="percentage-label">距离压力位:</span>
        <span class="percentage-value pressure-distance"
          :style="{ color: calculatePressureDistance() > 0 ? 'red' : '#00AF50' }">{{ calculatePressureDistance()
          }}%</span>
      </div>
    </div>
    <div class="scale-container">
      <!-- 使用渐变色实现标尺 -->
      <div class="scale-bar" :style="getScaleBarStyle()"></div>
      <!-- 支撑位标记 -->
      <div class="marker" :style="{ left: '15%' }">
        <div class="marker-line"></div>
        <div class="marker-label">
          <div class="marker-value">{{ index.support_point }}</div>
          <div class="marker-text">支撑位</div>
        </div>
      </div>
      <!-- 压力位标记 -->
      <div class="marker" :style="{ left: '80%' }" v-if="index.pressure_point">
        <div class="marker-line red"></div>
        <div class="marker-label">
          <div class="marker-value" style="color: #d9534f;">{{ index.pressure_point }}</div>
          <div class="marker-text" style="color: #007bff;">压力位</div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'IndexOverviewSingle',
  props: {
    index: {
      type: Object,
      required: true
    }
  },
  methods: {
    getIndexUrl() {
      // 特殊指数列表，需要使用gb前缀
      const specialIndices = ['GDAXI', 'HSHCI', 'HSI', 'HSTECH'];

      // 检查当前指数是否在特殊列表中
      if (specialIndices.includes(this.index.code)) {
        return `https://quote.eastmoney.com/gb/zs${this.index.code}.html`;
      }
      if (this.index.code === 'H30533') {
        return 'https://quote.eastmoney.com/zz/2.H30533.html';
      }
      if (this.index.code === '932000') {
        return 'https://quote.eastmoney.com/zz/2.932000.html';
      }
      if (this.index.code === "00700") {
        return `https://xueqiu.com/S/00700`;
      }

      // 默认使用普通链接
      return `http://quote.eastmoney.com/zs${this.index.code}.html`;
    },
    // 获取标尺渐变色样式
    getScaleBarStyle() {
      let css = ``;
      if (this.index.current_point <= this.index.support_point) {
        let supportDistance = Math.abs(this.calculateSupportDistance());
        let tempSupportDistance = 14 - Math.ceil(supportDistance * 15 / 100);
        css = `#01FFCD 0%, ${tempSupportDistance}%,
        #D5FFEB ${tempSupportDistance}% 15%, #ECF0F9 15% 100%`;
      } else if (this.index.current_point > this.index.support_point) {
        // 计算支撑位和中间区域的位置百分比
        let middlePosition = Number(this.getChangePercent()) * 65 / 100 + 15;
        css = `#01FFCD 0% 15%, #FFC000 15% ${middlePosition}%, #FFF2CD ${middlePosition}% 80%, #FFF2CD 80% 100%`;

        if (this.index.pressure_point && this.index.current_point >= this.index.pressure_point) {
          let pressureDistance = Math.abs(this.calculatePressureDistance());
          let tempPressureDistance = 80 + (pressureDistance * 25 / 100);
          css = `#01FFCD 0% 15%, #FFC000 15% 80%, #fe0000 80% ${tempPressureDistance}%, #fde0e2 ${tempPressureDistance}% 100%`;
        } else {
          css = `#01FFCD 0% 15%, #FFC000 15% ${middlePosition}%, #FFF2CD ${middlePosition}% 80%, #FDE0E2 80% 100%`;
        }

      }

      return {
        background: `linear-gradient(to right, ${css})`
      };
    },
    // 计算支撑位在标尺上的位置百分比
    getChangePercent() {
      // 假设标尺的最小值是支撑位的0.9倍，最大值是支撑位的1.8倍
      const minValue = parseFloat(this.index.support_point);
      const currentPoint = parseFloat(this.index.current_point);
      const maxValue = this.index.pressure_point ? parseFloat(this.index.pressure_point) : minValue * 2;

      // 计算支撑位在整个范围中的位置百分比
      return ((currentPoint - minValue) / (maxValue - minValue) * 100).toFixed(2);
    },
    calculateSupportDistance() {
      if (this.index.support_point) {
        const currentPoint = parseFloat(this.index.current_point);
        const support_point = parseFloat(this.index.support_point);
        const distance = ((support_point - currentPoint) / support_point * 100).toFixed(2);
        return (distance);
      }
      return 0;
    },
    // 计算当前点位距离压力位的百分比
    calculatePressureDistance() {
      if (this.index.pressure_point) {
        const currentPoint = parseFloat(this.index.current_point);
        const pressurePoint = parseFloat(this.index.pressure_point);
        const distance = ((pressurePoint - currentPoint) / pressurePoint * 100).toFixed(2);
        return (distance);
      }
      return 0;
    },
    // 格式化更新时间
    formatUpdateTime(timeStr) {
      if (!timeStr) return '';

      // 如果时间字符串包含空格，说明是完整的时间戳
      if (timeStr.includes(' ')) {
        const date = new Date(timeStr);
        return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
      }

      // 否则假设是日期字符串
      return timeStr;
    }
  }
}
</script>

<style scoped>
.index-overview-single {
  padding: 10px;
  background-color: #ffffff;
  border-radius: 4px;
  border: 1px solid #ebeef5;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  max-width: 400px;
}

.index-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.index-name-code {
  display: flex;
  flex-direction: column;
}

.index-name {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.index-code {
  font-size: 14px;
  color: #909399;
}

.index-current-value {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
  background-color: #f0f0f0;
  padding: 5px 10px;
  border-radius: 4px;
}

.index-value-container {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.update-time {
  font-size: 10px;
  color: #909399;
  margin-top: 2px;
}

.percentage-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.percentage-item {
  display: flex;
  align-items: center;
}

.percentage-label {
  font-size: 12px;
  color: #606266;
  margin-right: 5px;
}

.percentage-value {
  font-size: 12px;
  font-weight: bold;
}

.support-distance {
  color: #F56C6C;
  /* 红色 */
}

.index-link {
  color: #000;
  text-decoration: none;
  transition: color 0.2s;
}

.index-link:hover {
  color: #409EFF;
  text-decoration: underline;
}

.scale-container {
  position: relative;
  margin-top: 20px;
  height: 60px;
}

.scale-bar {
  position: absolute;
  top: 10px;
  width: 100%;
  height: 12px;
  border-radius: 6px;
}

.marker {
  position: absolute;
  top: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  transform: translateX(-50%);
  /* 使标记以自身中心对齐 */
}

.marker-line {
  width: 2px;
  height: 18px;
  background-color: #666;
  position: absolute;
  top: 7px;
}

.marker-line.red {
  background-color: #d9534f;
  /* 红色刻度线 */
}

.marker-label {
  position: absolute;
  bottom: 0;
  text-align: center;
  white-space: nowrap;
}

.marker-value {
  font-weight: bold;
  font-size: 14px;
  color: #333;
}

.marker-text {
  font-size: 12px;
  color: #555;
}
</style>