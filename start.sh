#!/bin/bash

echo "========================================"
echo "  验证码识别系统启动脚本"
echo "========================================"
echo ""

echo "[1/3] 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python，请先安装Python 3.9+"
    exit 1
fi
python3 --version

echo ""
echo "[2/3] 安装依赖包..."
pip3 install -r requirements.txt

echo ""
echo "[3/3] 启动服务..."
echo ""
echo "========================================"
echo "  服务已启动！"
echo "  前端界面: http://localhost:7777/"
echo "  API文档: http://localhost:7777/docs"
echo "  使用示例: http://localhost:7777/examples"
echo "========================================"
echo ""

python3 run.py
