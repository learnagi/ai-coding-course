# AI 辅助开发文档检索系统的 Prompt 指南

## 项目概述
我需要开发一个基于 Python 的文档检索系统，用于检索和回答关于飞书文档的问题。系统需要支持文档抓取、向量化、语义检索和问答生成功能。

## 技术要求
- 使用 FastAPI 构建后端服务
- 使用 ChromaDB 作为向量数据库
- 使用 sentence-transformers 生成文本向量
- 使用 Deepseek API 生成答案
- 使用 BeautifulSoup4 解析文档

## 开发步骤

### 第一步：环境设置
请帮我创建一个 `requirements.txt` 文件，包含以下依赖：
- chromadb
- fastapi
- uvicorn
- python-dotenv
- requests
- beautifulsoup4
- sentence-transformers
- torch

### 第二步：文档爬虫实现
请帮我实现一个 `feishu_crawler.py` 文件，需要：
1. 使用 requests 获取飞书文档内容
2. 使用 BeautifulSoup4 解析 HTML
3. 实现内容清理，去除无关元素
4. 保存文档到本地文件

示例代码结构：
```python
def fetch_feishu_doc(url: str) -> str:
    # 实现文档获取逻辑
    pass

def save_to_file(content: str, filename: str):
    # 实现文件保存逻辑
    pass
```

### 第三步：向量索引构建
请帮我实现一个 `build_index.py` 文件，需要：
1. 使用 sentence-transformers 生成文本向量
2. 实现文本分块功能
3. 使用 ChromaDB 存储向量和文档
4. 添加错误处理和日志

示例代码结构：
```python
def get_embedding(text: str) -> list:
    # 实现向量生成逻辑
    pass

def chunk_text(text: str, chunk_size: int = 1000) -> list:
    # 实现文本分块逻辑
    pass

def main():
    # 实现主流程
    pass
```

### 第四步：后端服务实现
请帮我实现一个 `app.py` 文件，需要：
1. 使用 FastAPI 创建 Web 服务
2. 实现搜索接口
3. 集成向量检索和问答生成
4. 添加错误处理和日志

示例代码结构：
```python
@app.post("/search")
def search(query: Query):
    # 实现搜索逻辑
    pass
```

## 具体要求

### 1. 文档爬虫
- 支持抓取公开的飞书文档
- 需要处理 HTML 特殊字符
- 去除页眉页脚等无关内容
- 保存为纯文本格式

### 2. 向量生成
- 使用 all-MiniLM-L6-v2 模型
- 文本块大小设为 1000 字符
- 保留段落完整性
- 添加重试机制

### 3. 检索服务
- 支持相似度检索
- 返回前 3 个最相关结果
- 包含文档来源信息
- 支持中文查询

### 4. 答案生成
- 使用 Deepseek API
- 支持上下文注入
- 生成简洁准确的答案
- 包含来源引用

## 测试用例
请提供以下测试用例的实现：
1. "指北AI的目标是什么？"
2. "文档中提到了哪些关于大模型ToB的内容？"
3. "如何联系投稿AI每日头条？"

## 错误处理
请处理以下错误情况：
1. 文档抓取失败
2. 向量生成失败
3. API 调用失败
4. 数据库操作失败

## 性能要求
1. 响应时间控制在 3 秒内
2. 支持并发请求
3. 内存占用合理
4. 磁盘使用优化

## 代码风格
1. 使用类型注解
2. 添加详细注释
3. 遵循 PEP 8 规范
4. 模块化设计

## 文档要求
1. 添加 README.md
2. 包含安装说明
3. 提供 API 文档
4. 包含示例代码

## 部署说明
1. 环境变量配置
2. 依赖安装步骤
3. 服务启动命令
4. 注意事项说明

## 预期输出
请按照以下格式返回每个文件的代码：

1. requirements.txt
2. .env
3. feishu_crawler.py
4. build_index.py
5. app.py
6. README.md

对于每个文件，请提供：
- 完整的代码实现
- 关键部分的注释说明
- 使用说明和示例

## 注意事项
1. 代码需要可以直接运行
2. 包含必要的错误处理
3. 遵循最佳实践
4. 考虑安全性

## 评估标准
1. 代码质量
2. 功能完整性
3. 性能表现
4. 可维护性

## 时间估计
- 环境搭建：30分钟
- 核心开发：2-3小时
- 测试调优：1-2小时
- 文档编写：1小时

## 后续支持
请说明如何处理：
1. 代码优化建议
2. 功能扩展方向
3. 性能提升方案
4. 维护更新计划
