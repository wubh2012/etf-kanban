<template>
  <div class="core-data-management">
    <div class="toolbar">
      <el-select v-model="selectedIndex" placeholder="请选择指数" @change="handleIndexChange" style="width: 200px; margin-right: 10px;">
        <el-option
          v-for="item in indices"
          :key="item.code"
          :label="`${item.name} (${item.code})`"
          :value="item.code"
        />
      </el-select>
      <el-button type="primary" @click="showAddDialog" :disabled="!selectedIndex">添加核心数据</el-button>
    </div>
    
    <el-table :data="coreDataList" style="width: 100%" border v-if="selectedIndex">
      <el-table-column prop="index_code" label="指数代码" width="120" />
      <el-table-column prop="etf_code" label="场内基金代码" width="150" />
      <el-table-column prop="mutual_code" label="场外基金代码" width="150" />
      <el-table-column prop="support_level" label="支撑点位笔记" width="200" show-overflow-tooltip />
      <el-table-column prop="normal_level" label="正常区间笔记" width="200" show-overflow-tooltip />
      <el-table-column prop="pressure_level" label="压力点位笔记" width="200" show-overflow-tooltip />
      <el-table-column prop="sell_level" label="卖出点位笔记" width="200" show-overflow-tooltip />
      <el-table-column prop="other_level" label="其他信息" width="200" show-overflow-tooltip />
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
      :title="isEdit ? '编辑核心数据' : '添加核心数据'"
      width="600px"
      @close="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        label-width="140px"
      >
        <el-form-item label="指数代码">
          <el-input v-model="form.index_code" disabled />
        </el-form-item>
        <el-form-item label="场内基金代码">
          <el-input v-model="form.etf_code" placeholder="请输入场内基金代码" />
        </el-form-item>
        <el-form-item label="场外基金代码">
          <el-input v-model="form.mutual_code" placeholder="请输入场外基金代码" />
        </el-form-item>
        <el-form-item label="支撑点位笔记">
          <el-input v-model="form.support_level" type="textarea" :rows="3" placeholder="请输入支撑点位笔记" />
        </el-form-item>
        <el-form-item label="正常区间笔记">
          <el-input v-model="form.normal_level" type="textarea" :rows="3" placeholder="请输入正常区间笔记" />
        </el-form-item>
        <el-form-item label="压力点位笔记">
          <el-input v-model="form.pressure_level" type="textarea" :rows="3" placeholder="请输入压力点位笔记" />
        </el-form-item>
        <el-form-item label="卖出点位笔记">
          <el-input v-model="form.sell_level" type="textarea" :rows="3" placeholder="请输入卖出点位笔记" />
        </el-form-item>
        <el-form-item label="其他信息">
          <el-input v-model="form.other_level" type="textarea" :rows="3" placeholder="请输入其他信息" />
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
import { getIndices, getIndexCoreData, createCoreData, updateCoreData, deleteCoreData } from '../../services/api'

export default {
  name: 'CoreDataManagement',
  setup() {
    const indices = ref([])
    const selectedIndex = ref('')
    const coreDataList = ref([])
    const dialogVisible = ref(false)
    const isEdit = ref(false)
    const formRef = ref(null)
    
    // 表单数据
    const form = reactive({
      index_code: '',
      etf_code: '',
      mutual_code: '',
      support_level: '',
      normal_level: '',
      pressure_level: '',
      sell_level: '',
      other_level: ''
    })
    
    // 获取指数列表
    const fetchIndices = async () => {
      try {
        const data = await getIndices()
        indices.value = data
      } catch (error) {
        ElMessage.error('获取指数列表失败: ' + error.message)
      }
    }
    
    // 获取核心数据
    const fetchCoreData = async (indexCode) => {
      if (!indexCode) {
        coreDataList.value = []
        return
      }
      
      try {
        const data = await getIndexCoreData(indexCode)
        // 将数据转换为数组形式，以便在表格中显示
        // 确保数据中包含index_code字段
        coreDataList.value = [{
          ...data,
          index_code: indexCode
        }]
      } catch (error) {
        // 如果没有核心数据，显示空数组
        if (error.response && error.response.status === 404) {
          coreDataList.value = []
        } else {
          ElMessage.error('获取核心数据失败: ' + error.message)
        }
      }
    }
    
    // 处理指数选择变化
    const handleIndexChange = (indexCode) => {
      selectedIndex.value = indexCode
      fetchCoreData(indexCode)
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
        form[key] = row[key] || ''
      })
      
      // 确保index_code字段正确设置
      form.index_code = selectedIndex.value
    }
    
    // 重置表单
    const resetForm = () => {
      if (formRef.value) {
        formRef.value.resetFields()
      }
      
      Object.keys(form).forEach(key => {
        form[key] = ''
      })
    }
    
    // 提交表单
    const handleSubmit = async () => {
      if (!formRef.value) return
      
      try {
        if (isEdit.value) {
          await updateCoreData(form.index_code, form)
          ElMessage.success('更新成功')
        } else {
          await createCoreData(form.index_code, form)
          ElMessage.success('添加成功')
        }
        
        dialogVisible.value = false
        fetchCoreData(selectedIndex.value)
      } catch (error) {
        ElMessage.error(isEdit.value ? '更新失败: ' + error.message : '添加失败: ' + error.message)
      }
    }
    
    // 删除核心数据
    const handleDelete = (row) => {
      ElMessageBox.confirm(
        `确定要删除该核心数据吗？此操作不可恢复。`,
        '警告',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          await deleteCoreData(row.index_code)
          ElMessage.success('删除成功')
          fetchCoreData(selectedIndex.value)
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
      coreDataList,
      dialogVisible,
      isEdit,
      formRef,
      form,
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
.core-data-management {
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