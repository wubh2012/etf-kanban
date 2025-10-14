<template>
  <div class="index-with-data-management">
    <div >
      <el-button type="primary" @click="handleAdd">添加指数</el-button>
    </div>
    
    <el-table
      :data="tableData"
      style="width: 100%"
      border
      stripe
      max-width="1600px"
      margin="0 auto"
    >
      <!-- <el-table-column prop="id" label="ID" width="70" /> -->
      <el-table-column prop="order_no" label="排序" width="80" />
      <el-table-column prop="name" label="指数名称" width="120" />
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
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加指数' : '编辑指数'"
      width="900px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        label-position="right"
      >
        <el-row :gutter="20">
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
        
        <el-row :gutter="20">
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
        
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="涨跌幅(%)" prop="change_percent">
              <el-input-number v-model="form.change_percent" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="进度(%)" prop="progress">
              <el-input-number v-model="form.progress" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="场内基金" prop="etf_code">
              <el-input v-model="form.etf_code" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="场外基金" prop="mutual_code">
              <el-input v-model="form.mutual_code" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="支撑点位笔记" prop="support_level">
              <el-input v-model="form.support_level" type="textarea" :rows="2" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="正常区间笔记" prop="normal_level">
              <el-input v-model="form.normal_level" type="textarea" :rows="2" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="正常区间2" prop="other_level">
              <el-input v-model="form.other_level" type="textarea" :rows="2" />
            </el-form-item>
          </el-col>
          
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="压力点位笔记" prop="pressure_level">
              <el-input v-model="form.pressure_level" type="textarea" :rows="2" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="卖出点位笔记" prop="sell_level">
              <el-input v-model="form.sell_level" type="textarea" :rows="2" />
            </el-form-item>
          </el-col>
          
        </el-row>
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
import { getIndices, createIndex, updateIndex, deleteIndex } from '@/api/index'

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
        other_level: ''
      }
    }
    
    // 添加指数
    const handleAdd = () => {
      resetForm()
      dialogType.value = 'add'
      dialogVisible.value = true
    }
    
    // 编辑指数
    const handleEdit = (row) => {
      form.value = { ...row }
      dialogType.value = 'edit'
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
              await createIndex(form.value)
              ElMessage.success('添加成功')
            } else {
              await updateIndex(form.value.code, form.value)
              ElMessage.success('更新成功')
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
  margin: 0 auto;
}


.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>