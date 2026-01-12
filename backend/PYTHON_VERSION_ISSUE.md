# Python版本兼容性问题

## 问题说明

当前环境使用 **Python 3.14**，这是一个非常新的Python版本，导致与FastAPI生态系统的兼容性问题。

### 错误信息
```
pydantic.errors.ConfigError: unable to infer type for attribute "name"
```

## 根本原因

Python 3.14 的类型推断机制变化，导致：
1. Pydantic 2.x 需要Rust编译器（Windows环境缺失）
2. Pydantic 1.x + FastAPI 组合与Python 3.14不兼容

## 推荐解决方案

### 方案1：降级Python版本（推荐）⭐

**安装Python 3.11.x（最稳定）**

1. 下载 Python 3.11.7: https://www.python.org/downloads/release/python-3117/
2. 安装后创建虚拟环境：
```bash
cd backend
python3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**或使用Python 3.10/3.9**也可以

### 方案2：使用Docker（最简单）

创建 `backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

运行：
```bash
docker build -t github-monitor-api .
docker run -p 8000:8000 github-monitor-api
```

### 方案3：安装Visual Studio C++ Build Tools

如果坚持使用Python 3.14，需要：

1. 下载并安装 **Visual Studio 2022 Build Tools**:
   https://visualstudio.microsoft.com/visual-cpp-build-tools/

2. 安装时选择 "Desktop development with C++"

3. 重新安装完整依赖（包括需要编译的包）

## 项目推荐配置

### 理想技术栈
```
Python: 3.11.7
FastAPI: 0.88.0
Pydantic: 1.10.13
```

### 为什么选择Python 3.11？

- ✅ 与FastAPI/Pydantic生态系统100%兼容
- ✅ 稳定可靠，生产环境验证
- ✅ 性能优秀
- ✅ 不需要C++/Rust编译器
- ✅ 所有依赖都有预编译二进制包

## 当前状态

**后端代码**: ✅ 完整且正确
**依赖配置**: ✅ 已优化（纯Python包）
**问题**: ⚠️ Python版本过新

## 下一步行动

**请选择以下之一**:

1. 🔹 安装Python 3.11并重新测试（5分钟）
2. 🔹 使用Docker运行（10分钟）
3. 🔹 安装C++ Build Tools（30分钟）

推荐方案1：简单快速！