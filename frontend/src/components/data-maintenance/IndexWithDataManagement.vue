<template>
  <div class="index-with-data-management">
    <div class="toolbar">
      <el-button type="primary" @click="showAddDialog">添加指数数据</el-button>
    </div>
    
    <el-table :data="indexWithDataList" style="width: 100%" border>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="指数名称" width="150" />
      <el-table-column prop="code" label="指数代码" width="120">
        <template #default="scope">
          <a :href="`http://quote.eastmoney.com/zs${scope.row.code}.html`" target="_blank" class="index-link">
            {{ scope.row.code }}
          </a>
        </template>
      </el-table-column>
      <el-table-column prop="current_point" label="当前点位" width="120" />
      <el-table-column prop="change_percent" label="距离大支撑涨跌幅(%)" width="180" />
      <el-table-column prop="support_point" label="支撑点位" width="120" />
      <el-table-column prop="pressure_point" label="压力点位" width="120" />
      <el-table-column prop="progress" label="进度(%)" width="100" />
      <el-table-column prop="etf_code" label="场内基金代码" width="150" />
      <el-table-column prop="mutual_code" label="场外基金代码" width="150" />
      <el-table-column prop="updated_at" label="更新时间" width="180" />
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="showEditDialog(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑指数数据' : '添加指数数据'"
      width="700px"
      @close="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="140px"
      >
        <!-- 指数基本信息 -->
        <el-divider content-position="left">指数基本信息</el-divider>
        <el-form-item label="指数名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入指数名称" />
        </el-form-item>
        <el-form-item label="指数代码" prop="code">
          <el-input v-model="form.code" placeholder="请输入指数代码" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="当前点位" prop="current_point">
          <el-input-number v-model="form.current_point" :precision="2" :step="0.01" />
        </el-form-item>
        <el-form-item label="距离大支撑涨跌幅(%)" prop="change_percent">
          <el-input-number v-model="form.change_percent" :precision="2" :step="0.01" />
        </el-form-item>
        <el-form-item label="支撑点位" prop="support_point">
          <el-input-number v-model="form.support_point" :precision="2" :step="0.01" />
        </el-form-item>
        <el-form-item label="压力点位" prop="pressure_point">
          <el-input-number v-model="form.pressure_point" :precision="2" :step="0.01" />
        </el-form-item>
        <el-form-item label="进度(%)" prop="progress">
          <el-input-number v-model="form.progress" :precision="2" :step="0.01" :min="0" :max="100" />
        </el-form-item>
        
        <!-- 核心数据信息 -->
        <el-divider content-position="left">核心数据信息</el-divider>
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
import { getIndices, createIndex, updateIndex, deleteIndex } from '../../services/api'

export default {
  name: 'IndexWithDataManagement',
  setup() {
    const indexWithDataList = ref([])
    const dialogVisible = ref(false)
    const isEdit = ref(false)
    const formRef = ref(null)
    
    // 表单数据
    const form = reactive({
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
      other_level: ''
    })
    
    // 表单验证规则
    const rules = {
      name: [
        { required: true, message: '请输入指数名称', trigger: 'blur' }
      ],
      code: [
        { required: true, message: '请输入指数代码', trigger: 'blur' }
      ]
    }
    
    // 获取指数列表（包含核心数据）
    const fetchIndexWithDataList = async () => {
      try {
        const data = await getIndices()
        indexWithDataList.value = data
      } catch (error) {
        ElMessage.error('获取指数数据列表失败: ' + error.message)
      }
    }
    
    // 显示添加对话框
    const showAddDialog = () => {
      isEdit.value = false
      dialogVisible.value = true
    }
    
    // 显示编辑对话框
    const showEditDialog = (row) => {
      isEdit.value = true
      dialogVisible.value = true
      
      // 填充表单数据
      Object.keys(form).forEach(key => {
        form[key] = row[key] || (key.includes('point') || key.includes('percent') || key === 'progress' ? null : '')
      })
    }
    
    // 重置表单
    const resetForm = () => {
      if (formRef.value) {
        formRef.value.resetFields()
      }
      
      Object.keys(form).forEach(key => {
        form[key] = key.includes('point') || key.includes('percent') || key === 'progress' ? null : ''
      })
    }
    
    // 提交表单
    const handleSubmit = async () => {
      if (!formRef.value) return
      
      await formRef.value.validate(async (valid) => {
        if (valid) {
          try {
            if (isEdit.value) {
              await updateIndex(form.code, form)
              ElMessage.success('更新成功')
            } else {
              await createIndex(form)
              ElMessage.success('添加成功')
            }
            
            dialogVisible.value = false
            fetchIndexWithDataList()
          } catch (error) {
            ElMessage.error(isEdit.value ? '更新失败: ' + error.message : '添加失败: ' + error.message)
          }
        }
      })
    }
    
    // 删除指数
    const handleDelete = (row) => {
      ElMessageBox.confirm(
        `确定要删除指数"${row.name}"吗？此操作将同时删除相关的核心数据和历史数据，且不可恢复。`,
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
          fetchIndexWithDataList()
        } catch (error) {
          ElMessage.error('删除失败: ' + error.message)
        }
      }).catch(() => {
        // 用户取消删除
      })
    }
    
    onMounted(() => {
      fetchIndexWithDataList()
    })
    
    return {
      indexWithDataList,
      dialogVisible,
      isEdit,
      formRef,
      form,
      rules,
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
.index-with-data-management {
  width: 100%;
}

.toolbar {
  margin-bottom: 20px;
}

.index-link {
  color: #409EFF;
  text-decoration: none;
}

.index-link:hover {
  text-decoration: underline;
}
</style>