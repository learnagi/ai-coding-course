# CodeGenius用户指南

## 快速入门

### 安装配置
1. 通过pip安装CodeGenius：
   ```bash
   pip install codegenius
   ```

2. 配置API密钥：
   ```bash
   export DEEPSEEK_API_KEY="your-api-key"
   ```

3. 初始化配置：
   ```python
   from codegenius import CodeGenius
   
   genius = CodeGenius()
   genius.initialize()
   ```

### 基本使用

#### 代码优化
```python
# 优化单个文件
genius.optimize_file("path/to/file.py")

# 优化整个项目
genius.optimize_project("path/to/project")
```

#### 生成测试
```python
# 为特定函数生成测试
genius.generate_tests("path/to/file.py", "function_name")

# 为整个模块生成测试
genius.generate_module_tests("path/to/module")
```

#### 生成文档
```python
# 生成API文档
genius.generate_docs("path/to/file.py")

# 生成项目文档
genius.generate_project_docs("path/to/project")
```

## 最佳实践

### 代码优化
1. 在提交代码前运行优化
2. 关注性能警告
3. 遵循建议的重构方案
4. 定期进行全项目扫描

### 测试生成
1. 优先测试核心功能
2. 保持测试用例的独立性
3. 定期更新测试套件
4. 关注边界条件测试

### 文档维护
1. 及时更新API文档
2. 添加使用示例
3. 保持文档风格统一
4. 多语言文档同步更新

## 故障排除

### 常见问题

1. API连接失败
   - 检查网络连接
   - 验证API密钥
   - 确认服务状态

2. 性能问题
   - 减少批处理大小
   - 增加系统资源
   - 优化缓存配置

3. 文档生成失败
   - 检查文件权限
   - 验证文件格式
   - 确保空间充足

### 获取支持

- 技术支持邮箱：support@codegenius.ai
- 文档中心：docs.codegenius.ai
- 社区论坛：forum.codegenius.ai
