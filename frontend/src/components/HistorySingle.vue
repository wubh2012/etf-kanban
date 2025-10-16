<template>
  <div class="history-single">
    <div v-if="history" class="history-container">
      <!-- 最高点跌幅卡片 -->
      <div v-if="history.three_year_high" class="history-item high">
        <div class="history-header">
          <span class="history-title">自最高点跌幅</span>
        </div>
        <div class="history-content">
          <div class="history-change-percent negative">{{ history.three_year_high.drop_from_high }}%</div>
          <div class="history-point">
            <div class="point-label">最高点</div>
            <div class="point-value">{{ history.three_year_high.value }}</div>
          </div>
          <div class="history-date">{{ history.three_year_high.date }}</div>
        </div>
      </div>

      <!-- 最低点涨幅卡片 -->
      <div v-if="history.three_year_low" class="history-item low">
        <div class="history-header">
          <span class="history-title low-title">自最低点上涨</span>
        </div>
        <div class="history-content">
          <div class="history-change-percent positive">+{{ history.three_year_low.rise_from_low }}% ↑</div>
          <div class="history-point">
            <div class="point-label">最低点</div>
            <div class="point-value">{{ history.three_year_low.value }}</div>
          </div>
          <div class="history-date">{{ history.three_year_low.date }}</div>
        </div>
      </div>
    </div>

    <div v-else class="no-data-container">
      <div class="no-data">暂无历史数据</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HistorySingle',
  props: {
    history: {
      type: Object,
      default: null
    }
  }
}
</script>

<style scoped>
.history-single {
  height: 100%;
  background-color: #DAE1F3;
}

.history-container {
  display: flex;
  flex-direction: row;
  gap: 10px;
  height: 100%;
}

.history-item {
  flex: 1;
  padding: 6px;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
}

/* 最高点跌幅卡片样式 */
.history-item.high {
  background: #000000;
}

/* 最低点涨幅卡片样式 */
.history-item.low {
  background: #fff;
}

.history-header {
  margin-bottom: 8px;
}

.history-title {
  font-size: 14px;
  color: #00FDC9;
}

/* 自最低点上涨标题 - 红色 */
.low-title {
  color: #FF0015;
}

.history-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.history-change-percent {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 6px;
  padding: 4px 8px;
  border-radius: 4px;
}

/* 跌幅样式 - 黑色背景，绿色文字 */
.negative {
  color: #00FDC9;
  background-color: #000000;
}

/* 涨幅样式 - 红色文字 */
.positive {
  color: #FF0015;
}

.history-point {
  margin-bottom: 4px;
}

/* 最高点文字样式 - 红色 */
.history-item.high .point-label,
.history-item.high .point-value,
.history-item.high .history-date {
  color: #d73e3e;
}

/* 最低点文字样式 - 绿色 */
.history-item.low .point-label,
.history-item.low .point-value,
.history-item.low .history-date {
  color: #3f9e3f;
}

.history-item.low .point-label {
  background-color: #00CC99;
  color: #fff;
}

.history-item.low .point-value {
  background-color: #D5FFEB;
  color: #3f9e3f;
}

.point-label {
  font-size: 12px;
  color: #909399;
  padding: 4px;
  margin-bottom: 2px;
}

.point-value {
  font-size: 16px;
  padding: 4px;
  font-weight: bold;
}

.history-date {
  font-size: 14px;
  color: #909399;
  margin-top: auto;
}

.no-data-container {
  text-align: center;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.no-data {
  color: #909399;
  font-size: 14px;
}
</style>