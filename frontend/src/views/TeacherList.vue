<template>
  <div class="teacher-list">
    <div class="filter-container">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="专业">
          <el-select v-model="filterForm.subject" placeholder="全部" clearable>
            <el-option label="全部" value=""></el-option>
            <el-option v-for="subject in subjects" :key="subject" :label="subject" :value="subject"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="职称">
          <el-select v-model="filterForm.title" placeholder="全部" clearable>
            <el-option label="全部" value=""></el-option>
            <el-option v-for="title in titles" :key="title" :label="title" :value="title"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="applyFilter">应用筛选</el-button>
          <el-button @click="resetFilter">取消</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-table :data="filteredTeachers" style="width: 100%">
      <el-table-column prop="employee_number" label="工号" width="100">
        <template slot-scope="scope">
          <el-input v-if="isAdmin" v-model.number="scope.row.employee_number" size="small" @change="handleEmployeeNumberChange(scope.row)"></el-input>
          <span v-else>{{ scope.row.employee_number }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="name" label="姓名" width="120"></el-table-column>
      <el-table-column prop="gender" label="性别" width="80"></el-table-column>
      <el-table-column label="民族" width="100">
        <template slot-scope="scope">
          {{ formatEthnicity(scope.row.ethnicity) }}
        </template>
      </el-table-column>
      <el-table-column prop="birth_date" label="出生年月" width="120"></el-table-column>
      <el-table-column prop="work_start_date" label="入校时间" width="120"></el-table-column>
      <el-table-column prop="major" label="学科类别" width="150"></el-table-column>
      <el-table-column prop="title" label="职称" width="120"></el-table-column>
      <el-table-column prop="research_direction" label="研究方向" width="200"></el-table-column>
      <el-table-column prop="address" label="地址" width="200"></el-table-column>
      <el-table-column prop="phone" label="电话" width="150"></el-table-column>
      <el-table-column fixed="right" label="操作" width="120">
        <template slot-scope="scope">
          <el-button @click="handleView(scope.row)" type="text" size="small">查看</el-button>
          <el-button @click="handleEdit(scope.row)" type="text" size="small">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      teachers: [],
      filterForm: {
        subject: '',
        title: ''
      },
      subjects: [],
      titles: [],
      isAdmin: false
    }
  },
  computed: {
    filteredTeachers() {
      return this.teachers.filter(teacher => {
        const subjectMatch = !this.filterForm.subject || teacher.major === this.filterForm.subject;
        const titleMatch = !this.filterForm.title || teacher.title === this.filterForm.title;
        return subjectMatch && titleMatch;
      });
    }
  },
  methods: {
    formatEthnicity(ethnicity) {
      if (!ethnicity) return '';
      if (ethnicity.endsWith('族')) {
        return ethnicity;
      }
      return ethnicity + '族';
    },
    async fetchTeachers() {
      try {
        const response = await this.$axios.get('/api/teachers')
        this.teachers = response.data
        // 提取所有不重复的学科类别和职称
        this.subjects = [...new Set(this.teachers.map(t => t.major).filter(Boolean))];
        this.titles = [...new Set(this.teachers.map(t => t.title).filter(Boolean))];
      } catch (error) {
        console.error('获取教师列表失败:', error)
      }
    },
    async handleEmployeeNumberChange(teacher) {
      try {
        await this.$axios.put(`/api/teachers/${teacher.id}`, {
          employee_number: teacher.employee_number
        })
        this.$message.success('工号更新成功')
      } catch (error) {
        console.error('更新工号失败:', error)
        this.$message.error('更新工号失败')
      }
    },
    handleView(row) {
      this.$router.push(`/teacher/${row.id}`)
    },
    handleEdit(row) {
      this.$router.push(`/teacher/${row.id}/edit`)
    },
    applyFilter() {
      // 筛选功能通过计算属性 filteredTeachers 自动实现
    },
    resetFilter() {
      this.filterForm.subject = '';
      this.filterForm.title = '';
    },
    async checkRole() {
      try {
        const response = await this.$axios.get('/api/user/role')
        this.isAdmin = response.data.role === 'admin'
      } catch (error) {
        console.error('获取用户角色失败:', error)
      }
    }
  },
  created() {
    this.fetchTeachers()
    this.checkRole()
  }
}
</script>

<style scoped>
.filter-container {
  margin-bottom: 20px;
}
.filter-form {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
}
</style> 