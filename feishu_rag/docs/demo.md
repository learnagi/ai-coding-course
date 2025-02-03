# 飞书文档检索系统演示文档

## 1. 系统架构

### 1.1 核心组件
- **文档爬虫**：使用 `requests` 和 `BeautifulSoup4` 抓取飞书公开文档
- **向量生成**：使用 `sentence-transformers` 的 `all-MiniLM-L6-v2` 模型生成文本向量
- **向量存储**：使用 `ChromaDB` 存储和检索文档向量
- **问答生成**：使用 `Deepseek` API 生成答案

### 1.2 技术栈
- 后端：FastAPI
- 向量数据库：ChromaDB
- 文本向量模型：sentence-transformers (all-MiniLM-L6-v2)
- 大语言模型：Deepseek Chat
- 文档解析：BeautifulSoup4

## 2. 系统功能

### 2.1 文档抓取
- 支持抓取公开的飞书文档
- 自动过滤无关内容（如页眉页脚）
- 保存原始文档到本地

### 2.2 文本向量化
- 使用 sentence-transformers 生成文本向量
- 支持文本分块，默认块大小为 1000 字符
- 向量维度：384（由 all-MiniLM-L6-v2 模型决定）

### 2.3 语义检索
- 基于 ChromaDB 的相似度检索
- 支持设置返回结果数量
- 返回相关文档片段及其元数据

### 2.4 问答生成
- 使用 Deepseek API 生成答案
- 支持上下文注入
- 返回答案及相关文档来源

## 3. API 接口

### 3.1 搜索接口
```bash
POST /search
Content-Type: application/json

{
    "query": "问题内容"
}
```

响应示例：
```json
{
    "answer": "生成的答案",
    "sources": [
        {
            "content": "相关文档内容",
            "metadata": {
                "source": "文档来源",
                "chunk_id": "文档块ID"
            }
        }
    ]
}
```

## 4. 测试用例

### 4.1 基础问答测试
1. **查询指北AI的目标**
```bash
curl -X POST http://localhost:8000/search \
     -H "Content-Type: application/json" \
     -d '{"query": "指北AI的目标是什么？"}'
```
响应：
```json
{
    "answer": "指北AI的目标是成为国内最活跃和垂直的AI爱好者/从业者社区。"
}
```

2. **查询大模型ToB相关内容**
```bash
curl -X POST http://localhost:8000/search \
     -H "Content-Type: application/json" \
     -d '{"query": "文档中提到了哪些关于大模型ToB的内容？"}'
```
响应：
```json
{
    "answer": "文档中提到了关于大模型ToB的内容，具体如下：\n\n1. **西二旗生活指北 |《大模型ToB，拼的还是茅台？》**  \n   这篇文章的链接是：https://mp.weixin.qq.com/s/zxdLYZGhJUvitxScGdMtQg  \n   从标题来看，这篇文章探讨了大模型在ToB市场中的竞争情况。"
}
```

### 4.2 推荐测试问题
1. "指北AI的目标是什么？"
2. "指北AI的愿景是什么？"
3. "如何联系投稿AI每日头条？"
4. "有哪些AI爆款文章？"
5. "2024年大模型从业者面临什么问题？"
6. "文档中提到了哪些关于大模型ToB的内容？"
7. "AI圈有哪些黑话？"
8. "AI从业者目前的就业情况如何？"

## 5. 部署说明

### 5.1 环境要求
- Python 3.8+
- pip 包管理器
- 足够的磁盘空间（用于存储向量数据库）

### 5.2 安装步骤
1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量：
```bash
# .env 文件
DEEPSEEK_API_KEY=your_api_key
```

3. 构建索引：
```bash
python build_index.py
```

4. 启动服务：
```bash
uvicorn app:app --reload
```

### 5.3 注意事项
- 确保 Deepseek API Key 已正确设置
- 首次运行时需要下载 sentence-transformers 模型
- 服务默认运行在 http://localhost:8000

## 6. 未来改进计划

### 6.1 功能增强
- [ ] 支持多文档源
- [ ] 添加文档更新机制
- [ ] 实现文档版本控制
- [ ] 添加用户反馈机制

### 6.2 性能优化
- [ ] 优化文本分块策略
- [ ] 添加向量缓存机制
- [ ] 实现批量处理
- [ ] 优化检索算法

### 6.3 用户体验
- [ ] 添加Web界面
- [ ] 提供API文档
- [ ] 添加示例代码
- [ ] 完善错误处理
