<template>
  <div class="five-one-container">
    <div class="header">
      <h2>五个一工程</h2>
      <div class="year-selector">
        <el-select v-model="selectedYear" placeholder="选择年份" @change="loadData">
          <el-option
            v-for="year in years"
            :key="year"
            :label="year + '年'"
            :value="year"
          />
        </el-select>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <el-skeleton :rows="10" animated />
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else class="content">
      <!-- 读书笔记 -->
      <el-card class="section">
        <template #header>
          <div class="card-header">
            <span>读书笔记</span>
            <el-button type="primary" @click="showAddDialog('book')">添加记录</el-button>
          </div>
        </template>
        <div v-if="data.book_records && data.book_records.length > 0">
          <el-table :data="data.book_records" style="width: 100%">
            <el-table-column prop="book_title" label="书名" />
            <el-table-column prop="book_number" label="书号" />
            <el-table-column prop="publish_date" label="出版日期" />
            <el-table-column prop="publisher" label="出版社" />
            <el-table-column prop="author" label="作者" />
            <el-table-column prop="has_notes" label="是否有笔记">
              <template #default="scope">
                {{ scope.row.has_notes ? '是' : '否' }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="scope">
                <el-button type="danger" size="small" @click="deleteRecord('book', scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div v-else class="empty-data">暂无数据</div>
      </el-card>

      <!-- 教学成果 -->
      <el-card class="section">
        <template #header>
          <div class="card-header">
            <span>教学成果</span>
            <el-button type="primary" @click="showAddDialog('teaching')">添加记录</el-button>
          </div>
        </template>
        <div v-if="data.teaching_records && data.teaching_records.length > 0">
          <el-table :data="data.teaching_records" style="width: 100%">
            <el-table-column prop="achievement_name" label="成果名称" />
            <el-table-column prop="achievement_type" label="成果类型" />
            <el-table-column prop="achievement_date" label="获得日期" />
            <el-table-column prop="achievement_ranking" label="排名" />
            <el-table-column label="操作" width="120">
              <template #default="scope">
                <el-button type="danger" size="small" @click="deleteRecord('teaching', scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div v-else class="empty-data">暂无数据</div>
      </el-card>

      <!-- 研究成果 -->
      <el-card class="section">
        <template #header>
          <div class="card-header">
            <span>研究成果</span>
            <el-button type="primary" @click="showAddDialog('research')">添加记录</el-button>
          </div>
        </template>
        <div v-if="data.research_records && data.research_records.length > 0">
          <el-table :data="data.research_records" style="width: 100%">
            <el-table-column prop="achievement_name" label="成果名称" />
            <el-table-column prop="research_type" label="研究类型" />
            <el-table-column prop="research_date" label="获得日期" />
            <el-table-column prop="research_ranking" label="排名" />
            <el-table-column label="操作" width="120">
              <template #default="scope">
                <el-button type="danger" size="small" @click="deleteRecord('research', scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div v-else class="empty-data">暂无数据</div>
      </el-card>

      <!-- 竞赛指导 -->
      <el-card class="section">
        <template #header>
          <div class="card-header">
            <span>竞赛指导</span>
            <el-button type="primary" @click="showAddDialog('competition')">添加记录</el-button>
          </div>
        </template>
        <div v-if="data.competition_records && data.competition_records.length > 0">
          <el-table :data="data.competition_records" style="width: 100%">
            <el-table-column prop="competition_name" label="竞赛名称" />
            <el-table-column prop="competition_organizer" label="主办单位" />
            <el-table-column prop="competition_type" label="竞赛类型" />
            <el-table-column prop="competition_date" label="竞赛日期" />
            <el-table-column prop="award_level" label="获奖等级" />
            <el-table-column prop="student_names" label="学生名单" />
            <el-table-column label="操作" width="120">
              <template #default="scope">
                <el-button type="danger" size="small" @click="deleteRecord('competition', scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div v-else class="empty-data">暂无数据</div>
      </el-card>

      <!-- 培训讲座 -->
      <el-card class="section">
        <template #header>
          <div class="card-header">
            <span>培训讲座</span>
            <el-button type="primary" @click="showAddDialog('training')">添加记录</el-button>
          </div>
        </template>
        <div v-if="data.training_records && data.training_records.length > 0">
          <el-table :data="data.training_records" style="width: 100%">
            <el-table-column prop="training_name" label="培训名称" />
            <el-table-column prop="training_organizer" label="主办单位" />
            <el-table-column prop="training_date" label="培训日期" />
            <el-table-column prop="training_location" label="培训地点" />
            <el-table-column prop="training_description" label="培训内容" />
            <el-table-column label="操作" width="120">
              <template #default="scope">
                <el-button type="danger" size="small" @click="deleteRecord('training', scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div v-else class="empty-data">暂无数据</div>
      </el-card>
    </div>

    <!-- 添加记录对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="50%"
    >
      <el-form :model="form" label-width="120px">
        <!-- 读书笔记表单 -->
        <template v-if="currentType === 'book'">
          <el-form-item label="书名">
            <el-input v-model="form.book_title" />
          </el-form-item>
          <el-form-item label="书号">
            <el-input v-model="form.book_number" />
          </el-form-item>
          <el-form-item label="出版日期">
            <el-date-picker
              v-model="form.publish_date"
              type="date"
              placeholder="选择日期"
              format="YYYY-MM-DD"
            />
          </el-form-item>
          <el-form-item label="出版社">
            <el-input v-model="form.publisher" />
          </el-form-item>
          <el-form-item label="作者">
            <el-input v-model="form.author" />
          </el-form-item>
          <el-form-item label="是否有笔记">
            <el-switch v-model="form.has_notes" />
          </el-form-item>
        </template>

        <!-- 教学成果表单 -->
        <template v-if="currentType === 'teaching'">
          <el-form-item label="成果名称">
            <el-input v-model="form.achievement_name" />
          </el-form-item>
          <el-form-item label="成果类型">
            <el-input v-model="form.achievement_type" />
          </el-form-item>
          <el-form-item label="获得日期">
            <el-date-picker
              v-model="form.achievement_date"
              type="date"
              placeholder="选择日期"
              format="YYYY-MM-DD"
            />
          </el-form-item>
          <el-form-item label="排名">
            <el-input v-model="form.achievement_ranking" />
          </el-form-item>
        </template>

        <!-- 研究成果表单 -->
        <template v-if="currentType === 'research'">
          <el-form-item label="成果名称">
            <el-input v-model="form.achievement_name" />
          </el-form-item>
          <el-form-item label="研究类型">
            <el-input v-model="form.research_type" />
          </el-form-item>
          <el-form-item label="获得日期">
            <el-date-picker
              v-model="form.research_date"
              type="date"
              placeholder="选择日期"
              format="YYYY-MM-DD"
            />
          </el-form-item>
          <el-form-item label="排名">
            <el-input v-model="form.research_ranking" />
          </el-form-item>
        </template>

        <!-- 竞赛指导表单 -->
        <template v-if="currentType === 'competition'">
          <el-form-item label="竞赛名称">
            <el-input v-model="form.competition_name" />
          </el-form-item>
          <el-form-item label="主办单位">
            <el-input v-model="form.competition_organizer" />
          </el-form-item>
          <el-form-item label="竞赛类型">
            <el-input v-model="form.competition_type" />
          </el-form-item>
          <el-form-item label="竞赛日期">
            <el-date-picker
              v-model="form.competition_date"
              type="date"
              placeholder="选择日期"
              format="YYYY-MM-DD"
            />
          </el-form-item>
          <el-form-item label="获奖等级">
            <el-input v-model="form.award_level" />
          </el-form-item>
          <el-form-item label="学生名单">
            <el-input v-model="form.student_names" />
          </el-form-item>
        </template>

        <!-- 培训讲座表单 -->
        <template v-if="currentType === 'training'">
          <el-form-item label="培训名称">
            <el-input v-model="form.training_name" />
          </el-form-item>
          <el-form-item label="主办单位">
            <el-input v-model="form.training_organizer" />
          </el-form-item>
          <el-form-item label="培训日期">
            <el-date-picker
              v-model="form.training_date"
              type="date"
              placeholder="选择日期"
              format="YYYY-MM-DD"
            />
          </el-form-item>
          <el-form-item label="培训地点">
            <el-input v-model="form.training_location" />
          </el-form-item>
          <el-form-item label="培训内容">
            <el-input
              v-model="form.training_description"
              type="textarea"
              :rows="3"
            />
          </el-form-item>
        </template>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

export default {
  name: 'FiveOne',
  setup() {
    const selectedYear = ref(new Date().getFullYear())
    const years = ref([])
    const data = ref({})
    const loading = ref(false)
    const error = ref('')
    const dialogVisible = ref(false)
    const currentType = ref('')
    const form = ref({})

    // 生成年份选项
    const generateYears = () => {
      const currentYear = new Date().getFullYear()
      years.value = Array.from({ length: 5 }, (_, i) => currentYear - i)
    }

    // 加载数据
    const loadData = async () => {
      loading.value = true
      error.value = ''
      try {
        const response = await axios.get(`/api/five_one/${selectedYear.value}`)
        if (response.data.success) {
          data.value = response.data.data
        } else {
          error.value = response.data.message
        }
      } catch (err) {
        error.value = '加载数据失败'
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    // 显示添加对话框
    const showAddDialog = (type) => {
      currentType.value = type
      form.value = {}
      dialogVisible.value = true
    }

    // 提交表单
    const submitForm = async () => {
      try {
        const formData = new FormData()
        formData.append('year', selectedYear.value)
        
        // 根据不同类型添加表单数据
        Object.keys(form.value).forEach(key => {
          if (form.value[key] instanceof Date) {
            formData.append(key, form.value[key].toISOString().split('T')[0])
          } else {
            formData.append(key, form.value[key])
          }
        })

        const response = await axios.post(`/api/five_one/records/${currentType.value}`, formData)
        if (response.data.success) {
          ElMessage.success('添加成功')
          dialogVisible.value = false
          loadData()
        } else {
          ElMessage.error(response.data.message)
        }
      } catch (err) {
        ElMessage.error('添加失败')
        console.error(err)
      }
    }

    // 删除记录
    const deleteRecord = async (type, id) => {
      try {
        const response = await axios.delete(`/api/five_one/records/${type}/${id}`)
        if (response.data.success) {
          ElMessage.success('删除成功')
          loadData()
        } else {
          ElMessage.error(response.data.message)
        }
      } catch (err) {
        ElMessage.error('删除失败')
        console.error(err)
      }
    }

    onMounted(() => {
      generateYears()
      loadData()
    })

    return {
      selectedYear,
      years,
      data,
      loading,
      error,
      dialogVisible,
      currentType,
      form,
      loadData,
      showAddDialog,
      submitForm,
      deleteRecord
    }
  }
}
</script>

<style scoped>
.five-one-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.empty-data {
  text-align: center;
  color: #909399;
  padding: 20px;
}

.loading {
  padding: 20px;
}

.error {
  color: #f56c6c;
  text-align: center;
  padding: 20px;
}
</style> 