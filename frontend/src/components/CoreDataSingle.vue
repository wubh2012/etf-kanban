<template>
  <div class="core-data-single">
    <!-- 标题栏 -->
    <table class="core-data-table">
      <thead>
        <tr>
          <th class="header-item-fund-code">致敬 & 基金</th>
          <th class="header-item-support-level">大支撑位</th>
          <th class="header-item-normal-range" colspan="2">正常区间</th>
          <th class="header-item-pressure-level">大压力位</th>
          <th class="header-item-sell-point">卖出点位</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <!-- 左侧代码信息 -->
          <td class="content-item-fund-code">
            <div v-if="coreData.etf_code" class="code-tag" style="">场内 {{ coreData.etf_code }}</div>
            <div v-if="coreData.mutual_code" class="code-tag">场外 {{ coreData.mutual_code }}</div>
          </td>

          <!-- 大支撑位 -->
          <td class="content-item-support-level">
            <div class="level-content support">
              <div class="level-value">{{ coreData.support_level }}</div>
              <div v-if="coreData.support_comment" class="level-comment">{{ coreData.support_comment }}</div>
              <div v-if="coreData.support_date" class="level-date">{{ coreData.support_date }}</div>
            </div>
          </td>

          <!-- 正常区间 -->
          <td class="content-item-normal-range">
            <div class="level-content normal">
              <div class="level-value">{{ coreData.normal_level }}</div>
              <div v-if="coreData.normal_comment" class="level-comment">{{ coreData.normal_comment }}</div>
              <div v-if="coreData.normal_date" class="level-date">{{ coreData.normal_date }}</div>
             
            </div>
          </td>
          <td class="content-item-normal-range">
            <div class="level-content normal">
              <div class="level-value">{{ coreData.other_level }}</div>
            </div>
          </td>

          <!-- 大压力位 -->
          <td class="content-item-pressure-level">
            <div class="level-content pressure">
              <div class="level-value">{{ coreData.pressure_level }}</div>
              <div v-if="coreData.pressure_date" class="level-date">{{ coreData.pressure_date }}</div>
            </div>
          </td>

          <!-- 卖出点位 -->
          <td class="content-item-sell-point">
            <div class="level-content sell">
              <div v-if="coreData.sell_comment" class="level-comment">{{ coreData.sell_comment }}</div>
              <div v-if="coreData.sell_date" class="level-date">{{ coreData.sell_date }}</div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
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

/* 表格样式 */
.core-data-table {
  width: 100%;
  border-collapse: collapse;
  height: 100%;
  table-layout: fixed;
}

/* 标题栏样式 */
.core-data-table th {
  /* padding: 10px 15px; */
  font-weight: bold;
  text-align: center;
  border-bottom: 1px solid #e6e6e6;
}

.header-item-fund-code {
  width: 16.66%;
  background-color: #00ffcc;
  border-right: 1px solid #ddd;
}

.header-item-support-level {
  width: 16.66%;
  background-color: #00FFCD;
}

.header-item-normal-range {
  width: 33.33%;
  background-color: #FFC000;
  color: #00205F;
}

.header-item-pressure-level {
  width: 16.66%;
  background-color: #FF7C81;
  color: #00205F;
  border-right: 1px solid #ddd;
}

.header-item-sell-point {
  width: 16.69%;
  background-color: #FF7C81;
  color: #00205F;
}

/* 内容区域样式 */
.core-data-table td {
  padding: 6px;
  vertical-align: top;
  border: 1px solid #ddd;
}

.content-item-fund-code,
.content-item-support-level {
  width: 16.66%;
  height: 100%;
}
.content-item-fund-code {
  /* display: flex; */
  flex-direction: row;
  /* width: 100%; */
}

.content-item-normal-range {
  width: 33.33%;
  height: 100%;
}

.content-item-pressure-level,
.content-item-sell-point {
  width: 16.66%;
  height: 100%;
}

/* 数据项通用样式 */
.level-content {
  width: 100%;
  height: 100%;
  border-radius: 4px;
  font-size: 12px;
  word-break: break-word;
  display: flex;
  flex-direction: column;
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
  padding: 1px;
  display: inline-block;
}

/* 移动端适配 */
@media screen and (max-width: 768px) {
  .core-data-single {
    height: 100%;
  }
  
  .core-data-table {
    font-size: 12px;
  }
  
  .core-data-table th {
    padding: 6px 4px;
    font-size: 11px;
  }
  
  .core-data-table td {
    padding: 4px 2px;
  }
  
  .level-content {
    font-size: 11px;
  }
  
  .level-value {
    font-size: 11px;
    margin-bottom: 3px;
  }
  
  .level-comment {
    font-size: 10px;
    margin-bottom: 2px;
  }
  
  .level-date {
    font-size: 10px;
  }
  
  .code-tag {
    font-size: 10px;
    padding: 1px;
    margin-right: 3px;
  }
}
</style>