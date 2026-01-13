# 启动指南 - 重要！

## ⚠️ 当前问题

您仍在使用 **Python 3.14**，这导致Pydantic兼容性错误。

错误信息中可以看到：
```
File "C:\Users\heihu\AppData\Local\Programs\Python\Python314\Lib\..."
```

## ✅ 解决方案

### 步骤1：确认Python 3.11安装位置

```bash
# 查找Python 3.11
where python
where python3.11
```

### 步骤2：使用Python 3.11创建虚拟环境

```bash
cd G:\学习\github_monitor\backend

# 使用完整路径创建虚拟环境（替换为您的Python 3.11实际路径）
C:\Users\heihu\AppData\Local\Programs\Python\Python311\python.exe -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 验证Python版本（必须显示3.11.x）
python --version
```

### 步骤3：安装依赖

```bash
# 确保在虚拟环境中
pip install -r requirements.txt
```

### 步骤4：启动服务器

```bash
uvicorn app.main:app --reload
```

### 步骤5：验证

访问: http://localhost:8000/docs

应该能看到Swagger API文档！

## 📝 常见问题

### Q: 如何确认使用的是Python 3.11？

```bash
# 激活虚拟环境后
python --version
# 应该显示: Python 3.11.x

# 查看Python路径
where python
# 应该显示虚拟环境路径，如: G:\学习\github_monitor\backend\venv\Scripts\python.exe
```

### Q: 虚拟环境激活失败？

使用PowerShell：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

### Q: 仍然使用Python 3.14？

关闭所有终端窗口，打开新终端，重新激活虚拟环境

## 🎯 检查清单

在运行uvicorn之前确认：
- [ ] 已创建Python 3.11虚拟环境
- [ ] 已激活虚拟环境（命令行前缀显示(venv)）
- [ ] python --version 显示 3.11.x
- [ ] pip install成功完成
- [ ] 无Pydantic错误

**关键**：必须在虚拟环境中运行！