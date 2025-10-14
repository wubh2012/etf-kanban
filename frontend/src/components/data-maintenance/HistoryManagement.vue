<template>
  <div class="history-management">
    <div class="toolbar">
      <el-select v-model="selectedIndex" placeholder="请选择指数" @change="handleIndexChange" style="width: 200px; margin-right: 10px;">
        <el-option
          v-for="item in indices"
          :key="item.code"
          :label="`${item.name} (${item.code})`"
          :value="item.code"
        />
      </el-select>
      <el-button type="primary" @click="showAddDialog" :disabled="!selectedIndex">添加历史数据</el-button>
    </div>
    
    <el-table :data="historyList" style="width: 100%" border_no v-if="selectedIndex">
      <el-table-column prop="index_code" label="指数代码" width="120" />
      <el-table-column prop="type" label="类型" width="150">
        <template #default="scope">
          <el-tag :type="scope.row.type === 'three_year_high' ? 'danger' : 'success'">
            {{ scope.row.type === 'three_year_high' ? '三年高点' : '三年低点' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="value" label="点位" width="120" />
      <el-table-column prop="date" label="日期" width="150" />
      <el-table-column prop="change_percent" label="涨跌幅(%)" width="120" />
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="showEditDialog(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <div v-else class="no-data">
      <el-empty description="请选择指数" />
    </div>
    
    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑历史数据' : '添加历史数据'"
      width="500px"
      @close="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="指数代码">
          <el-input v-model="form.index_code" disabled />
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择类型" style="width: 100%" :disabled="isEdit">
            <el-option label="三年低点" value="three_year_low" />
            <el-option label="三年高点" value="three_year_high" />
          </el-select>
        </el-form-item>
        <el-form-item label="点位" prop="value">
          <el-input-number v-model="form.value" :precision="2" :step="0.01" style="width: 100%" />
        </el-form-item>
        <el-form-item label="日期" prop="date">
          <el-date-picker
            v-model="form.date"
            type="date"
            placeholder="选择日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="涨跌幅(%)">
          <el-input-number v-model="form.change_percent" :precision="2" :step="0.01" style="width: 100%" />
        </el-form-item>
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
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getIndices, getIndexHistory, createHistory, updateHistory, deleteHistory } from '@/api/index'

export default {
  name: 'HistoryManagement',
  setup() {
    const indices = ref([])
    const selectedIndex = ref('')
    const historyList = ref([])
    const dialogVisible = ref(false)
    const isEdit = ref(false)
    const formRef = ref(null)
    
    // 表单数据
    const form = reactive({
      index_code: '',
      type: '',
      value: null,
      date: '',
      change_percent: null
    })
    
    // 表单验证规则
    const rules = {
      type: [
        { required: true, message: '请选择类型', trigger: 'change' }
      ],
      value: [
        { required: true, message: '请输入点位', trigger: 'blur' }
      ],
      date: [
        { required: true, message: '请选择日期', trigger: 'change' }
      ]
    }
    
    // 获取指数列表
    const fetchIndices = async () => {
      try {
        const data = await getIndices()
        indices.value = data
      } catch (error) {
        ElMessage.error('获取指数列表失败: ' + error.message)
      }
    }
    
    // 获取历史数据
    const fetchHistory = async (indexCode) => {
      if (!indexCode) {
        historyList.value = []
        return
      }
      
      try {
        const data = await getIndexHistory(indexCode)
        // 将后端返回的对象转换为数组形式，以便在表格中显示
        if (data && typeof data === 'object') {
          historyList.value = Object.keys(data).map(key => ({
            index_code: indexCode,
            type: key,
            value: data[key].value,
            date: data[key].date,
            change_percent: data[key].change_percent
          }))
        } else {
          historyList.value = []
        }
      } catch (error) {
        // 如果没有历史数据，显示空数组
        if (error.response && error.response.status === 404) {
          historyList.value = []
        } else {
          ElMessage.error('获取历史数据失败: ' + error.message)
        }
      }
    }
    
    // 处理指数选择变化
    const handleIndexChange = (indexCode) => {
      selectedIndex.value = indexCode
      fetchHistory(indexCode)
    }
    
    // 显示添加对话框
    const showAddDialog = () => {
      isEdit.value = false
      dialogVisible.value = true
      form.index_code = selectedIndex.value
    }
    
    // 显示编辑对话框
    const showEditDialog = (row) => {
      isEdit.value = true
      dialogVisible.value = true
      
      // 填充表单数据
      Object.keys(form).forEach(key => {
        form[key] = row[key]
      })
    }
    
    // 重置表单
    const resetForm = () => {
      if (formRef.value) {
        formRef.value.resetFields()
      }
      
      Object.keys(form).forEach(key => {
        form[key] = key === 'value' || key === 'change_percent' ? null : ''
      })
    }
    
    // 提交表单
    const handleSubmit = async () => {
      if (!formRef.value) return
      
      await formRef.value.validate(async (valid) => {
        if (valid) {
          try {
            if (isEdit.value) {
              await updateHistory(form.index_code, form.type, form)
              ElMessage.success('更新成功')
            } else {
              await createHistory(form.index_code, form)
              ElMessage.success('添加成功')
            }
            
            dialogVisible.value = false
            fetchHistory(selectedIndex.value)
          } catch (error) {
            ElMessage.error(isEdit.value ? '更新失败: ' + error.message : '添加失败: ' + error.message)
          }
        }
      })
    }
    
    // 删除历史数据
    const handleDelete = (row) => {
      ElMessageBox.confirm(
        `确定要删除该历史数据吗？此操作不可恢复。`,
        '警告',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          await deleteHistory(row.index_code, row.type)
          ElMessage.success('删除成功')
          fetchHistory(selectedIndex.value)
        } catch (error) {
          ElMessage.error('删除失败: ' + error.message)
        }
      }).catch(() => {
        // 用户取消删除
      })
    }
    
    onMounted(() => {
      fetchIndices()
    })
    
    return {
      indices,
      selectedIndex,
      historyList,
      dialogVisible,
      isEdit,
      formRef,
      form,
      rules,
      handleIndexChange,
      showAddDialog,
      showEditDialog,
      resetForm,
      handleSubmit,
      handleDelete
    }
  }
}
</script>

<style scoped>
.history-management {
  width: 100%;
}

.toolbar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.no-data {
  margin-top: 50px;
}
</style>