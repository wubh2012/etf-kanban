<template>
  <div class="index-with-data-management">
    <div>
      <el-button type="primary" @click="handleAdd">添加指数</el-button>
    </div>

    <el-table :data="tableData" style="width: 100%" border stripe max-width="1600px" >
      <!-- <el-table-column prop="id" label="ID" width="70" /> -->
      <el-table-column prop="order_no" label="排序" width="80" />
      <el-table-column prop="name" label="指数名称" width="120" >
        <template #default="scope">
          <el-link size="small" @click="handleEdit(scope.row)">{{scope.row.name}}</el-link>
        </template>
      </el-table-column>
      <el-table-column prop="code" label="指数代码" width="100" />
      <el-table-column prop="current_point" label="当前点位" width="100" />
      <el-table-column prop="change_percent" label="涨跌幅(%)" width="100" />
      <el-table-column prop="support_point" label="支撑点位" width="100" />
      <el-table-column prop="pressure_point" label="压力点位" width="100" />
      <!-- <el-table-column prop="progress" label="进度(%)" width="80" /> -->
      <el-table-column prop="etf_code" label="场内基金" width="100" />
      <el-table-column prop="mutual_code" label="场外基金" width="100" />
      <el-table-column prop="support_level" label="支撑点位笔记" width="150" show-overflow-tooltip />
      <el-table-column prop="normal_level" label="正常区间1" width="150" show-overflow-tooltip />
      <el-table-column prop="other_level" label="正常区间2" width="150" show-overflow-tooltip />
      <el-table-column prop="pressure_level" label="压力点位笔记" width="150" show-overflow-tooltip />
      <el-table-column prop="sell_level" label="卖出点位笔记" width="150" show-overflow-tooltip />
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 编辑对话框 -->
    <el-dialog v-model="dialogVisible" draggable :title="dialogType === 'add' ? '添加指数' : '编辑指数'" width="900px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" label-position="right">
        <el-row :gutter="12">
          <el-col :span="8">
            <el-form-item label="排序" prop="order_no">
              <el-input-number v-model="form.order_no" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="指数名称" prop="name">
              <el-input v-model="form.name" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="指数代码" prop="code">
              <el-input v-model="form.code" :disabled="dialogType === 'edit'" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="12">
          <el-col :span="8">
            <el-form-item label="当前点位" prop="current_point">
              <el-input-number v-model="form.current_point" style="width: 100%" />
            </el-form-item>
          </el-col>

          <el-col :span="8">
            <el-form-item label="支撑点位" prop="support_point">
              <el-input-number v-model="form.support_point" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="压力点位" prop="pressure_point">
              <el-input-number v-model="form.pressure_point" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="12">
          <!-- <el-col :span="8">
            <el-form-item label="涨跌幅(%)" prop="change_percent">
              <el-input-number v-model="form.change_percent" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="进度(%)" prop="progress">
              <el-input-number v-model="form.progress" style="width: 100%" />
            </el-form-item>
          </el-col> -->
          <el-col :span="8">
            <el-form-item label="场内基金" prop="etf_code">
              <el-input v-model="form.etf_code" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="场外基金" prop="mutual_code">
              <el-input v-model="form.mutual_code" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="12">
          
          <el-col :span="12">
            <el-form-item label="支撑点位笔记" prop="support_level">
              <el-input v-model="form.support_level" type="textarea" :rows="1" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="正常区间笔记" prop="normal_level">
              <el-input v-model="form.normal_level" type="textarea" :rows="1" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="正常区间2" prop="other_level">
              <el-input v-model="form.other_level" type="textarea" :rows="1" />
            </el-form-item>
          </el-col>

        </el-row>

        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="压力点位笔记" prop="pressure_level">
              <el-input v-model="form.pressure_level" type="textarea" :rows="1" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="卖出点位笔记" prop="sell_level">
              <el-input v-model="form.sell_level" type="textarea" :rows="1" />
            </el-form-item>
          </el-col>

        </el-row>

        <!-- 历史数据部分 - 在添加和编辑模式下都显示 -->
        <div>
          <el-divider content-position="left">历史数据</el-divider>
          <el-row :gutter="12">
            <el-col :span="12">
              <el-card shadow="never" style="margin-bottom: 0;">
                <template #header>
                  <div class="card-header">
                    <span>三年高点</span>
                  </div>
                </template>
                <el-form-item label="涨跌幅(%)" prop="historyHigh.change_percent">
                  <el-input-number v-model="form.historyHigh.change_percent" :precision="2" :step="0.01"
                    style="width: 100%" />
                </el-form-item>
                <el-form-item label="点位" prop="historyHigh.value">
                  <el-input-number v-model="form.historyHigh.value" :precision="2" :step="0.01" style="width: 100%" />
                </el-form-item>
                <el-form-item label="日期" prop="historyHigh.date">
                  <el-date-picker v-model="form.historyHigh.date" type="date" placeholder="选择日期" format="YYYY-MM-DD"
                    value-format="YYYY-MM-DD" style="width: 100%" />
                </el-form-item>

              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card shadow="never" style="margin-bottom: 0;">
                <template #header>
                  <div class="card-header">
                    <span>三年低点</span>
                  </div>
                </template>
                <el-form-item label="涨跌幅(%)" prop="historyLow.change_percent">
                  <el-input-number v-model="form.historyLow.change_percent" :precision="2" :step="0.01"
                    style="width: 100%" />
                </el-form-item>
                <el-form-item label="点位" prop="historyLow.value">
                  <el-input-number v-model="form.historyLow.value" :precision="2" :step="0.01" style="width: 100%" />
                </el-form-item>
                <el-form-item label="日期" prop="historyLow.date">
                  <el-date-picker v-model="form.historyLow.date" type="date" placeholder="选择日期" format="YYYY-MM-DD"
                    value-format="YYYY-MM-DD" style="width: 100%" />
                </el-form-item>

              </el-card>
            </el-col>

          </el-row>
        </div>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getIndices, createIndex, updateIndex, deleteIndex, createHistory, getIndexHistory, updateHistory } from '@/api/index'

export default {
  name: 'IndexWithDataManagement',
  setup() {
    const tableData = ref([])
    const dialogVisible = ref(false)
    const dialogType = ref('add') // 'add' or 'edit'
    const formRef = ref(null)

    // 表单数据
    const form = ref({
      id: null,
      order_no: 0,
      name: '',
      code: '',
      current_point: null,
      change_percent: null,
      support_point: null,
      pressure_point: null,
      progress: null,
      etf_code: '',
      mutual_code: '',
      support_level: '',
      normal_level: '',
      pressure_level: '',
      sell_level: '',
      other_level: '',
      // 历史数据字段
      historyLow: {
        value: null,
        date: '',
        change_percent: null
      },
      historyHigh: {
        value: null,
        date: '',
        change_percent: null
      }
    })

    // 表单验证规则
    const rules = {
      name: [
        { required: true, message: '请输入指数名称', trigger: 'blur' }
      ],
      code: [
        { required: true, message: '请输入指数代码', trigger: 'blur' }
      ],
      'historyLow.value': [
        { required: false, message: '请输入点位', trigger: 'blur' }
      ],
      'historyLow.date': [
        { required: false, message: '请选择日期', trigger: 'change' }
      ],
      'historyHigh.value': [
        { required: false, message: '请输入点位', trigger: 'blur' }
      ],
      'historyHigh.date': [
        { required: false, message: '请选择日期', trigger: 'change' }
      ]
    }

    // 获取数据
    const fetchData = async () => {
      try {
        const response = await getIndices()
        console.log('获取到的指数数据:', response);

        tableData.value = response
      } catch (error) {
        ElMessage.error('获取数据失败')
        console.error(error)
      }
    }

    // 重置表单
    const resetForm = () => {
      form.value = {
        id: null,
        order_no: 0,
        name: '',
        code: '',
        current_point: null,
        change_percent: null,
        support_point: null,
        pressure_point: null,
        progress: null,
        etf_code: '',
        mutual_code: '',
        support_level: '',
        normal_level: '',
        pressure_level: '',
        sell_level: '',
        other_level: '',
        // 历史数据字段
        historyLow: {
          value: null,
          date: '',
          change_percent: null
        },
        historyHigh: {
          value: null,
          date: '',
          change_percent: null
        }
      }
    }

    // 添加指数
    const handleAdd = () => {
      resetForm()
      dialogType.value = 'add'
      dialogVisible.value = true
    }

    // 编辑指数
    const handleEdit = async (row) => {
      form.value = { ...row }
      dialogType.value = 'edit'
      // 确保历史数据字段存在
      form.value.historyLow = form.value.historyLow || {
        value: null,
        date: '',
        change_percent: null
      }
      form.value.historyHigh = form.value.historyHigh || {
        value: null,
        date: '',
        change_percent: null
      }

      // 获取历史数据
      try {
        const historyData = await getIndexHistory(row.code)
        // 填充历史数据到表单
        if (historyData['three_year_low']) {
          form.value.historyLow = {
            value: historyData['three_year_low'].value,
            date: historyData['three_year_low'].date,
            change_percent: historyData['three_year_low'].change_percent
          }
        }
        if (historyData['three_year_high']) {
          form.value.historyHigh = {
            value: historyData['three_year_high'].value,
            date: historyData['three_year_high'].date,
            change_percent: historyData['three_year_high'].change_percent
          }
        }
      } catch (error) {
        // 如果没有历史数据，保持默认值
        console.log('获取历史数据失败:', error)
      }

      dialogVisible.value = true
    }

    // 删除指数
    const handleDelete = (row) => {
      ElMessageBox.confirm(
        `确定要删除指数"${row.name}"吗？`,
        '警告',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          await deleteIndex(row.code)
          ElMessage.success('删除成功')
          fetchData()
        } catch (error) {
          ElMessage.error('删除失败')
          console.error(error)
        }
      }).catch(() => {
        // 用户取消删除
      })
    }

    // 提交表单
    const handleSubmit = () => {
      formRef.value.validate(async (valid) => {
        if (valid) {
          try {
            if (dialogType.value === 'add') {
              // 先创建指数
              const indexResponse = await createIndex(form.value)
              ElMessage.success('添加成功')

              // 如果有历史数据，则创建历史数据
              const indexCode = form.value.code
              if (form.value.historyLow.value && form.value.historyLow.date) {
                await createHistory(indexCode, {
                  type: 'three_year_low',
                  value: form.value.historyLow.value,
                  date: form.value.historyLow.date,
                  change_percent: form.value.historyLow.change_percent
                })
              }

              if (form.value.historyHigh.value && form.value.historyHigh.date) {
                await createHistory(indexCode, {
                  type: 'three_year_high',
                  value: form.value.historyHigh.value,
                  date: form.value.historyHigh.date,
                  change_percent: form.value.historyHigh.change_percent
                })
              }
            } else {
              // 更新指数
              await updateIndex(form.value.code, form.value)
              ElMessage.success('更新成功')

              // 更新历史数据
              const indexCode = form.value.code
              // 更新三年低点
              if (form.value.historyLow.value && form.value.historyLow.date) {
                try {
                  await updateHistory(indexCode, 'three_year_low', {
                    value: form.value.historyLow.value,
                    date: form.value.historyLow.date,
                    change_percent: form.value.historyLow.change_percent
                  })
                } catch (error) {
                  // 如果更新失败，可能是不存在该历史数据，尝试创建
                  if (error.response && error.response.status === 404) {
                    try {
                      await createHistory(indexCode, {
                        type: 'three_year_low',
                        value: form.value.historyLow.value,
                        date: form.value.historyLow.date,
                        change_percent: form.value.historyLow.change_percent
                      })
                    } catch (createError) {
                      console.error('创建三年低点历史数据失败:', createError)
                    }
                  } else {
                    console.error('更新三年低点历史数据失败:', error)
                  }
                }
              }

              // 更新三年高点
              if (form.value.historyHigh.value && form.value.historyHigh.date) {
                try {
                  await updateHistory(indexCode, 'three_year_high', {
                    value: form.value.historyHigh.value,
                    date: form.value.historyHigh.date,
                    change_percent: form.value.historyHigh.change_percent
                  })
                } catch (error) {
                  // 如果更新失败，可能是不存在该历史数据，尝试创建
                  if (error.response && error.response.status === 404) {
                    try {
                      await createHistory(indexCode, {
                        type: 'three_year_high',
                        value: form.value.historyHigh.value,
                        date: form.value.historyHigh.date,
                        change_percent: form.value.historyHigh.change_percent
                      })
                    } catch (createError) {
                      console.error('创建三年高点历史数据失败:', createError)
                    }
                  } else {
                    console.error('更新三年高点历史数据失败:', error)
                  }
                }
              }
            }
            dialogVisible.value = false
            fetchData()
          } catch (error) {
            ElMessage.error(dialogType.value === 'add' ? '添加失败' : '更新失败')
            console.error(error)
          }
        }
      })
    }

    onMounted(() => {
      fetchData()
    })

    return {
      tableData,
      dialogVisible,
      dialogType,
      formRef,
      form,
      rules,
      handleAdd,
      handleEdit,
      handleDelete,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.index-with-data-management {
  padding: 20px;
  max-width: 1600px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

.card-header {
  font-weight: bold;
  color: #409EFF;
}

/* 使表单更加紧凑的样式 */
:deep(.el-form-item) {
  margin-bottom: 12px;
}

:deep(.el-card__body) {
  padding: 12px;
}

:deep(.el-dialog__body) {
  padding: 15px 20px;
}

:deep(.el-divider) {
  margin: 8px 0;
}
</style>