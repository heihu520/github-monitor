# 后端依赖安装指南

## 问题诊断

当前环境：
- **Python**: 3.14 (最新版)
- **系统**: Windows
- **问题**: pydantic-core需要Rust编译器

## 推荐解决方案

### 方案1：使用预编译包（最简单）⭐

直接从清华镜像下载预编译的wheel文件：

```bash
cd backend

# 下载预编译的pydantic-core (Python 3.14)
pip install https://pypi.tuna.tsinghua.edu.cn/packages/py3/p/pydantic-core/pydantic_core-2.14.6-cp314-cp314-win_amd64.whl

# 然后安装其他依赖
pip install -r requirements.txt
```

如果上述链接不工作，尝试从官方PyPI下载：
```bash
pip install --only-binary=:all: pydantic-core==2.14.6
pip install -r requirements.txt
```

### 方案2：降级到Python 3.11（推荐）

**这是最稳定的方案！**

1. 下载Python 3.11.7: https://www.python.org/downloads/release/python-3117/
2. 安装后：
```bash
cd backend
python3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 方案3：使用conda（如果有）

```bash
conda create -n github-monitor python=3.11
conda activate github-monitor
cd backend
pip install -r requirements.txt
```

## 为什么这么复杂？

**Python 3.14太新了！**
- Pydantic 2.x的pydantic-core需要Rust编译
- Windows上Rust环境配置很复杂
- 很多包还没有Python 3.14的预编译版本

## 我的建议

**使用Python 3.11.7**

原因：
- ✅ 完全兼容FastAPI/Pydantic
- ✅ 所有包都有预编译版本
- ✅ 不需要任何编译器
- ✅ 5分钟搞定
- ✅ 生产环境稳定

## 后续步骤

安装好依赖后：
```bash
uvicorn app.main:app --reload
```

访问 http://localhost:8000/docs 查看API文档