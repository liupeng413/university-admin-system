import React from 'react';
import { Layout, Menu } from 'antd';
import { Outlet, useNavigate } from 'react-router-dom';
import {
  DashboardOutlined,
  UserOutlined,
  BookOutlined,
  FileOutlined,
  ClockCircleOutlined,
} from '@ant-design/icons';

const { Header, Sider, Content } = Layout;

const MainLayout: React.FC = () => {
  const navigate = useNavigate();

  const menuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: '仪表盘',
    },
    {
      key: '/users',
      icon: <UserOutlined />,
      label: '用户管理',
    },
    {
      key: '/courses',
      icon: <BookOutlined />,
      label: '课程管理',
    },
    {
      key: '/documents',
      icon: <FileOutlined />,
      label: '公文管理',
    },
    {
      key: '/attendance',
      icon: <ClockCircleOutlined />,
      label: '考勤管理',
    },
  ];

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider width={200} theme="dark">
        <div style={{ height: 32, margin: 16, background: 'rgba(255, 255, 255, 0.2)' }} />
        <Menu
          theme="dark"
          mode="inline"
          defaultSelectedKeys={['/']}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
        />
      </Sider>
      <Layout>
        <Header style={{ padding: 0, background: '#fff' }} />
        <Content style={{ margin: '24px 16px', padding: 24, background: '#fff' }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout; 