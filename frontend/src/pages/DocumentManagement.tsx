import React, { useState } from 'react';
import { Table, Button, Space, Modal, Form, Input, Select, DatePicker, message } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, UploadOutlined } from '@ant-design/icons';
import type { Dayjs } from 'dayjs';

interface Document {
  id: number;
  title: string;
  type: string;
  department: string;
  author: string;
  createTime: string;
  status: string;
}

const DocumentManagement: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([
    {
      id: 1,
      title: '关于2024年寒假放假安排的通知',
      type: '通知',
      department: '教务处',
      author: '张主任',
      createTime: '2024-01-15',
      status: '已发布',
    },
    // 更多公文数据...
  ]);

  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [editingDocument, setEditingDocument] = useState<Document | null>(null);

  const columns = [
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
    },
    {
      title: '部门',
      dataIndex: 'department',
      key: 'department',
    },
    {
      title: '作者',
      dataIndex: 'author',
      key: 'author',
    },
    {
      title: '创建时间',
      dataIndex: 'createTime',
      key: 'createTime',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Document) => (
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
    setEditingDocument(null);
    form.resetFields();
    setIsModalVisible(true);
  };

  const handleEdit = (document: Document) => {
    setEditingDocument(document);
    form.setFieldsValue({
      ...document,
      createTime: dayjs(document.createTime),
    });
    setIsModalVisible(true);
  };

  const handleDelete = (document: Document) => {
    Modal.confirm({
      title: '确认删除',
      content: `确定要删除公文 ${document.title} 吗？`,
      onOk: () => {
        setDocuments(documents.filter(d => d.id !== document.id));
        message.success('删除成功');
      },
    });
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      if (editingDocument) {
        // 更新公文
        setDocuments(documents.map(d =>
          d.id === editingDocument.id ? { ...d, ...values, createTime: values.createTime.format('YYYY-MM-DD') } : d
        ));
        message.success('更新成功');
      } else {
        // 添加公文
        const newDocument = {
          id: documents.length + 1,
          ...values,
          createTime: values.createTime.format('YYYY-MM-DD'),
          status: '待审核',
        };
        setDocuments([...documents, newDocument]);
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
        <Space>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={handleAdd}
          >
            新建公文
          </Button>
          <Button
            icon={<UploadOutlined />}
          >
            导入公文
          </Button>
        </Space>
      </div>
      <Table columns={columns} dataSource={documents} rowKey="id" />
      <Modal
        title={editingDocument ? '编辑公文' : '新建公文'}
        open={isModalVisible}
        onOk={handleModalOk}
        onCancel={() => setIsModalVisible(false)}
      >
        <Form
          form={form}
          layout="vertical"
        >
          <Form.Item
            name="title"
            label="标题"
            rules={[{ required: true, message: '请输入标题' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="type"
            label="类型"
            rules={[{ required: true, message: '请选择类型' }]}
          >
            <Select>
              <Select.Option value="通知">通知</Select.Option>
              <Select.Option value="公告">公告</Select.Option>
              <Select.Option value="报告">报告</Select.Option>
              <Select.Option value="请示">请示</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="department"
            label="部门"
            rules={[{ required: true, message: '请输入部门' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="author"
            label="作者"
            rules={[{ required: true, message: '请输入作者' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="createTime"
            label="创建时间"
            rules={[{ required: true, message: '请选择创建时间' }]}
          >
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default DocumentManagement; 