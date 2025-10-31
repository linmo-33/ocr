# CAPTCHA 识别 API

基于 ddddocr 的验证码识别服务，支持多种验证码类型识别。

## 功能特性

### 核心功能
- 🔐 滑块验证码识别
- 📝 OCR文字识别（支持批量）
- 🎯 目标检测
- 🧮 计算类验证码
- ✂️ 图片分割
- 👆 点选验证码

### 系统功能
- 🎨 现代化Web界面
- 📊 实时统计分析
- 🚀 速率限制保护
- 📖 Swagger API文档
- 🖼️ 图片预处理增强
- 💡 丰富的代码示例

## 项目结构

```
.
├── app/
│   ├── __init__.py          # 应用工厂
│   ├── config.py            # 配置文件
│   ├── routes/              # 路由模块
│   │   ├── __init__.py
│   │   ├── captcha_routes.py   # 验证码识别路由
│   │   └── system_routes.py    # 系统路由
│   ├── services/            # 业务逻辑
│   │   ├── __init__.py
│   │   └── captcha_service.py  # 验证码服务
│   └── utils/               # 工具函数
│       ├── __init__.py
│       ├── image_processor.py  # 图片处理
│       ├── logger.py           # 日志配置
│       └── stats.py            # 统计功能
├── run.py                   # 应用入口
├── requirements.txt         # 依赖包
├── Dockerfile              # Docker配置
└── README.md               # 项目文档
```

## 快速开始

### 本地运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行服务：
```bash
python run.py
```

3. 访问服务：
```
前端界面: http://localhost:7777/
使用示例: http://localhost:7777/examples
API文档: http://localhost:7777/docs
健康检查: http://localhost:7777/health
统计信息: http://localhost:7777/stats
```

### Docker 运行

```bash
docker build -t captcha-api .
docker run -p 7777:7777 captcha-api
```

## API 端点

### 系统端点
- `GET /` - API首页
- `GET /health` - 健康检查
- `GET /stats` - 统计信息
- `GET /docs` - API文档

### 识别端点
- `POST /classification` - OCR文字识别
- `POST /batch/classification` - 批量OCR识别
- `POST /capcode` - 滑块验证码识别
- `POST /slideComparison` - 滑块对比
- `POST /detection` - 目标检测
- `POST /calculate` - 计算类验证码
- `POST /crop` - 图片分割
- `POST /select` - 点选验证码

## 使用方式

### 方式一：Web界面（推荐）

1. 访问 `http://localhost:7777/`
2. 选择识别类型（OCR、滑块、检测等）
3. 上传图片或粘贴Base64/URL
4. 点击"开始识别"查看结果
5. 查看实时统计信息

### 方式二：API调用

#### OCR识别
```bash
curl -X POST http://localhost:7777/classification \
  -H "Content-Type: application/json" \
  -d '{
    "image": "base64_string_or_url",
    "preprocess": true
  }'
```

#### 滑块识别
```bash
curl -X POST http://localhost:7777/capcode \
  -H "Content-Type: application/json" \
  -d '{
    "slidingImage": "base64_or_url",
    "backImage": "base64_or_url",
    "simpleTarget": true,
    "preprocess": false
  }'
```

#### 批量识别
```bash
curl -X POST http://localhost:7777/batch/classification \
  -H "Content-Type: application/json" \
  -d '{
    "images": ["image1", "image2"],
    "preprocess": false
  }'
```

更多示例请访问：http://localhost:7777/examples

## 配置说明

在 `app/config.py` 中可以修改：
- 日志级别和格式
- API速率限制
- 批量处理最大数量
- 服务器端口和主机

## 技术栈

- Flask - Web框架
- ddddocr - 验证码识别
- OpenCV - 图像处理
- Pillow - 图像增强
- Flask-Limiter - 速率限制
- Flasgger - API文档

## 项目截图

### Web界面
- 现代化的渐变背景设计
- 响应式布局，支持移动端
- 实时统计面板
- 多标签功能切换

### 功能特点
- 📱 响应式设计，支持各种屏幕尺寸
- 🎨 美观的UI界面
- ⚡ 快速的识别响应
- 📊 实时统计展示
- 💡 丰富的代码示例

## 快速启动

### Windows
双击运行 `start.bat`

### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

## 常见问题

### 1. 端口被占用
修改 `app/config.py` 中的 `PORT` 配置

### 2. 识别率低
- 尝试启用"图片预处理"选项
- 确保图片清晰度足够
- 检查图片格式是否支持

### 3. 请求被限制
- 检查速率限制配置
- 等待一段时间后重试
- 考虑部署多个实例

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License
