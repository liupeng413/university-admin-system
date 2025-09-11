# 教师管理系统

一个基于 Flask 和 SQLite 的教师信息管理系统。

## 功能特点

- 教师信息管理（增删改查）
- 用户角色管理（管理员/普通用户）
- 文件上传下载
- 教师数据统计
- 响应式界面设计

## 技术栈

- 后端：Python Flask
- 数据库：SQLite
- 前端：HTML, CSS, JavaScript
- UI 框架：Bootstrap

## 安装步骤

1. 克隆项目
```bash
git clone [repository URL]
cd university-admin-system
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 初始化数据库
```bash
python init_teachers.py
```

5. 运行项目
```bash
python backend/app.py
```

## 系统要求

- Python 3.8+
- pip
- 虚拟环境（推荐）

## 目录结构

```
university-admin-system/
├── backend/
│   ├── app.py
│   └── init_teachers.py
├── frontend/
│   ├── static/
│   └── templates/
├── requirements.txt
└── README.md
```

## 默认账户

- 管理员账户：admin/admin123
- 教师账户：[姓名拼音]/123456

## 部署说明

详细的部署步骤请参考 `deployment_guide.md`。

## 许可证

MIT License 