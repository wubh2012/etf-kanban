<template>
  <div class="core-data-single">
    <!-- 标题栏 -->
    <div class="header-row">
      <div class="header-item-fund-code">致敬 & 基金</div>
      <div class="header-item-support-level">大支撑位</div>
      <div class="header-item-normal-range">正常区间</div>
      <div class="header-item-normal-range"></div>
      <div class="header-item-pressure-level">大压力位</div>
      <div class="header-item-sell-point">卖出点位</div>
    </div>

    <!-- 内容区域 -->
    <div class="content-row">
      <!-- 左侧代码信息 -->
      <div class="content-item-fund-code">
        <div v-if="coreData.etf_code" class="code-tag">场内 {{ coreData.etf_code }}</div>
        <div v-if="coreData.mutual_code" class="code-tag">场外 {{ coreData.mutual_code }}</div>
      </div>

      <!-- 大支撑位 -->
      <div class="content-item-support-level">
        <div class="level-content support">
          <div class="level-value">{{ coreData.support_level }}</div>
          <div v-if="coreData.support_comment" class="level-comment">{{ coreData.support_comment }}</div>
          <div v-if="coreData.support_date" class="level-date">{{ coreData.support_date }}</div>
        </div>
      </div>

      <!-- 正常区间 -->
      <div class="content-item-normal-range">
        <div class="level-content normal">
          <div class="level-value">{{ coreData.normal_level }}</div>
          <div v-if="coreData.normal_comment" class="level-comment">{{ coreData.normal_comment }}</div>
          <div v-if="coreData.normal_date" class="level-date">{{ coreData.normal_date }}</div>
        </div>
      </div>
      <div class="content-item-normal-range">
        <div class="level-content normal">
          <div class="level-value">{{ coreData.other_level }}</div>
        </div>
      </div>

      <!-- 大压力位 -->
      <div class="content-item-pressure-level">
        <div class="level-content pressure">
          <div class="level-value">{{ coreData.pressure_level }}</div>
          <div v-if="coreData.pressure_date" class="level-date">{{ coreData.pressure_date }}</div>
        </div>
      </div>

      <!-- 卖出点位 -->
      <div class="content-item-sell-point">
        <div class="level-content sell">
          <div v-if="coreData.sell_comment" class="level-comment">{{ coreData.sell_comment }}</div>
          <div v-if="coreData.sell_date" class="level-date">{{ coreData.sell_date }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CoreDataSingle',
  props: {
    coreData: {
      type: Object,
      required: true
    },
    index: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.core-data-single {
  background-color: #ffffff;
  border-radius: 4px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* 标题栏样式 */
.header-row {
  display: flex;
  flex-direction: row;
  border-bottom: 1px solid #e6e6e6;
}

.header-item-fund-code {
  flex: 1;
  padding: 10px 15px;
  background-color: #00ffcc;
  font-weight: bold;
  text-align: center;
  border-right: 1px solid #ddd;
}

.header-item-support-level {
  flex: 1;
  padding: 10px 15px;
  background-color: #00ffcc;
  font-weight: bold;
  text-align: center;
}

.header-item-normal-range {
  flex: 1;
  padding: 10px 15px;
  background-color: #ffffcc;
  font-weight: bold;
  text-align: center;
  color: #000000;
}

.header-item-pressure-level {
  flex: 1;
  padding: 10px 15px;
  background-color: #ff9999;
  font-weight: bold;
  text-align: center;
  color: #000000;
  border-right: 1px solid #ddd;
}

.header-item-sell-point {
  flex: 1;
  padding: 10px 15px;
  background-color: #ff9999;
  font-weight: bold;
  text-align: center;
  color: #000000;
}

/* 内容区域样式 */
.content-row {
  display: flex;
  flex-direction: row;
  height: calc(100% - 40px);
  overflow: hidden;
}

.content-item-fund-code,
.content-item-support-level,
.content-item-normal-range,
.content-item-pressure-level,
.content-item-sell-point {
  flex: 1;
  padding: 10px;
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  border: 1px solid #ddd;
}

/* 数据项通用样式 */
.level-content {
  width: 100%;
  border-radius: 4px;
  font-size: 12px;
  word-break: break-word;
}

.level-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.level-value {
  color: #1890ff;
  margin-bottom: 5px;
}

.level-comment {
  margin-bottom: 5px;
}

.level-date {
  color: #909399;
  font-size: 12px;
}

/* 代码标签样式 */
.code-tag {
  font-size: 12px;
  background-color: #A6A6A6;
  color: white;
  padding: 2px;
  border-radius: 4px;
  display: inline-block;
  margin-right: 5px;
  margin-bottom: 5px;
}
</style>