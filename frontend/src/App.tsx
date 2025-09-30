import React from 'react';
import { Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import UserManagement from './pages/UserManagement';
import CourseManagement from './pages/CourseManagement';
import DocumentManagement from './pages/DocumentManagement';
import AttendanceManagement from './pages/AttendanceManagement';

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<MainLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="users" element={<UserManagement />} />
        <Route path="courses" element={<CourseManagement />} />
        <Route path="documents" element={<DocumentManagement />} />
        <Route path="attendance" element={<AttendanceManagement />} />
      </Route>
    </Routes>
  );
};

export default App; 