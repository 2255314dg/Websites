# 个人作品集网站

## 项目简介

这是一个基于Django框架开发的个人作品集网站，用于展示个人项目、作品和技能。网站支持中英文双语切换，包含首页、关于我、作品集和联系方式等页面。

## 项目结构

```
Profile_Enzo/
├── portfolio/              # 主要应用目录
│   ├── migrations/         # 数据库迁移文件
│   ├── static/             # 应用静态文件
│   │   └── portfolio/      # 静态文件分类
│   │       ├── css/        # CSS文件
│   │       ├── js/         # JavaScript文件
│   │       └── images/     # 图片文件
│   ├── templates/          # 应用模板文件
│   │   └── portfolio/      # 模板文件分类
│   │       ├── about.html  # 关于我页面
│   │       ├── base.html   # 基础模板
│   │       ├── contact.html # 联系方式页面
│   │       ├── home.html   # 首页
│   │       ├── portfolio.html # 作品集页面
│   │       └── project_detail.html # 项目详情页面
│   ├── __init__.py         # 应用初始化文件
│   ├── admin.py            # 后台管理配置
│   ├── apps.py             # 应用配置
│   ├── models.py           # 数据模型
│   ├── tests.py            # 测试文件
│   ├── urls.py             # 应用路由
│   └── views.py            # 视图函数
├── profile_website/        # 项目配置目录
│   ├── __init__.py         # 项目初始化文件
│   ├── asgi.py             # ASGI配置
│   ├── settings.py         # 项目设置
│   ├── urls.py             # 项目路由
│   └── wsgi.py             # WSGI配置
├── media/                  # 媒体文件目录
│   ├── icons/              # 图标文件
│   ├── music/              # 音乐文件
│   └── pictures/           # 图片文件
├── .venv/                  # 虚拟环境目录
├── db.sqlite3              # SQLite数据库文件
└── README.md               # 项目说明文件
```

## 安装和运行

### 1. 环境要求

- Python 3.10+
- Django 5.2+

### 2. 安装步骤

1. 克隆或下载项目到本地
2. 创建并激活虚拟环境
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```
3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```
4. 运行数据库迁移
   ```bash
   python manage.py migrate
   ```
5. 创建超级用户（用于后台管理）
   ```bash
   python manage.py createsuperuser
   ```
6. 启动开发服务器
   ```bash
   python manage.py runserver
   ```

### 3. 访问网站

- 前台：http://127.0.0.1:8000
- 后台管理：http://127.0.0.1:8000/admin

## 功能说明

### 1. 首页
- 个人简介
- 最新项目展示
- 快速导航

### 2. 关于我
- 个人信息
- 教育背景
- 技能展示
- 证书展示

### 3. 作品集
- 项目分类浏览
- 项目列表展示
- 分页功能

### 4. 项目详情
- 项目详细信息
- 视频展示
- 视频 gallery

### 5. 联系方式
- 联系表单
- 社交媒体链接

### 6. 其他功能
- 中英文双语切换
- 背景音乐控制
- 响应式设计，支持移动端

## 技术栈

- **后端**：Django 5.2+
- **前端**：HTML5, CSS3, JavaScript, Bootstrap 5
- **数据库**：SQLite
- **国际化**：Django内置i18n
- **静态文件管理**：Django静态文件系统
- **媒体文件管理**：Django媒体文件系统

## 开发说明

### 1. 添加新页面

1. 在 `portfolio/templates/portfolio/` 目录下创建新的HTML模板文件
2. 在 `portfolio/views.py` 中添加对应的视图函数
3. 在 `portfolio/urls.py` 中添加路由

### 2. 添加新静态文件

1. 在 `portfolio/static/portfolio/` 目录下对应的子目录中添加文件
2. 在模板文件中使用 `{% static 'portfolio/路径/文件名' %}` 引用

### 3. 添加新模型

1. 在 `portfolio/models.py` 中定义新模型
2. 运行 `python manage.py makemigrations` 创建迁移文件
3. 运行 `python manage.py migrate` 应用迁移
4. 在 `portfolio/admin.py` 中注册模型，以便在后台管理

### 4. 翻译管理

1. 在 `locale/` 目录下创建语言文件夹（如 `zh_CN/LC_MESSAGES/`）
2. 运行 `python manage.py makemessages -l zh_CN` 生成翻译文件
3. 编辑生成的 `.po` 文件，添加翻译
4. 运行 `python manage.py compilemessages` 编译翻译文件

## 部署说明

### 1. 收集静态文件

在部署前，需要收集所有静态文件到 `staticfiles` 目录：

```bash
python manage.py collectstatic
```

### 2. 生产环境配置

1. 修改 `settings.py` 文件中的 `DEBUG` 为 `False`
2. 设置 `ALLOWED_HOSTS` 为你的域名
3. 配置 `STATIC_ROOT` 和 `MEDIA_ROOT` 为合适的路径

### 3. 部署选项

- **Django内置服务器**：仅用于开发环境
- **Gunicorn + Nginx**：推荐的生产环境部署方案
- **Docker**：容器化部署

## 许可证

本项目采用 MIT 许可证。

## 作者

Enzo

---

感谢使用本项目！如有任何问题或建议，欢迎联系。