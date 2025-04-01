import React, { useState } from 'react';
import { Table, Button, Space, Modal, Form, Input, Select, InputNumber, message } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';

interface Course {
  id: number;
  name: string;
  code: string;
  teacher: string;
  credit: number;
  semester: string;
  status: string;
}

const CourseManagement: React.FC = () => {
  const [courses, setCourses] = useState<Course[]>([
    {
      id: 1,
      name: '高等数学',
      code: 'MATH101',
      teacher: '张教授',
      credit: 4,
      semester: '2023-2024-1',
      status: '进行中',
    },
    // 更多课程数据...
  ]);

  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [editingCourse, setEditingCourse] = useState<Course | null>(null);

  const columns = [
    {
      title: '课程名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '课程代码',
      dataIndex: 'code',
      key: 'code',
    },
    {
      title: '授课教师',
      dataIndex: 'teacher',
      key: 'teacher',
    },
    {
      title: '学分',
      dataIndex: 'credit',
      key: 'credit',
    },
    {
      title: '学期',
      dataIndex: 'semester',
      key: 'semester',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Course) => (
        <Space size="middle">
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
          <Button
            type="link"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record)}
          >
            删除
          </Button>
        </Space>
      ),
    },
  ];

  const handleAdd = () => {
    setEditingCourse(null);
    form.resetFields();
    setIsModalVisible(true);
  };

  const handleEdit = (course: Course) => {
    setEditingCourse(course);
    form.setFieldsValue(course);
    setIsModalVisible(true);
  };

  const handleDelete = (course: Course) => {
    Modal.confirm({
      title: '确认删除',
      content: `确定要删除课程 ${course.name} 吗？`,
      onOk: () => {
        setCourses(courses.filter(c => c.id !== course.id));
        message.success('删除成功');
      },
    });
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      if (editingCourse) {
        // 更新课程
        setCourses(courses.map(c =>
          c.id === editingCourse.id ? { ...c, ...values } : c
        ));
        message.success('更新成功');
      } else {
        // 添加课程
        const newCourse = {
          id: courses.length + 1,
          ...values,
          status: '进行中',
        };
        setCourses([...courses, newCourse]);
        message.success('添加成功');
      }
      setIsModalVisible(false);
    } catch (error) {
      console.error('表单验证失败:', error);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleAdd}
        >
          添加课程
        </Button>
      </div>
      <Table columns={columns} dataSource={courses} rowKey="id" />
      <Modal
        title={editingCourse ? '编辑课程' : '添加课程'}
        open={isModalVisible}
        onOk={handleModalOk}
        onCancel={() => setIsModalVisible(false)}
      >
        <Form
          form={form}
          layout="vertical"
        >
          <Form.Item
            name="name"
            label="课程名称"
            rules={[{ required: true, message: '请输入课程名称' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="code"
            label="课程代码"
            rules={[{ required: true, message: '请输入课程代码' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="teacher"
            label="授课教师"
            rules={[{ required: true, message: '请输入授课教师' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="credit"
            label="学分"
            rules={[{ required: true, message: '请输入学分' }]}
          >
            <InputNumber min={1} max={10} />
          </Form.Item>
          <Form.Item
            name="semester"
            label="学期"
            rules={[{ required: true, message: '请输入学期' }]}
          >
            <Select>
              <Select.Option value="2023-2024-1">2023-2024-1</Select.Option>
              <Select.Option value="2023-2024-2">2023-2024-2</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default CourseManagement; 