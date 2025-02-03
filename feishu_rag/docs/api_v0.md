# 文档检索系统 API 文档 (v0)

## API 概览

基础 URL: `http://localhost:8000`

### API 版本
- 当前版本: v0
- 最后更新: 2025-01-12

## 接口列表

### 1. 文档搜索接口

#### 1.1 基本信息
- 接口路径: `/search`
- 请求方法: `POST`
- 接口描述: 根据用户输入的问题，返回相关的答案和来源文档

#### 1.2 请求参数
```json
{
    "query": "问题内容"
}
```

| 参数名 | 类型   | 必填 | 描述     | 示例                    |
|--------|--------|------|----------|-------------------------|
| query  | string | 是   | 查询问题 | "指北AI的目标是什么？" |

#### 1.3 响应参数
```json
{
    "answer": "生成的答案内容",
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

| 参数名                | 类型   | 描述                 | 示例                                    |
|----------------------|--------|---------------------|----------------------------------------|
| answer              | string | 生成的答案           | "指北AI的目标是成为国内最活跃的AI社区" |
| sources             | array  | 相关文档来源列表     | -                                      |
| sources[].content   | string | 文档片段内容         | "指北AI的目标是..."                    |
| sources[].metadata  | object | 文档元数据           | -                                      |
| sources[].metadata.source | string | 文档来源文件名 | "feishu_doc.txt"                      |
| sources[].metadata.chunk_id | number | 文档块ID    | 0                                      |

#### 1.4 错误码
| 错误码 | 描述           | 解决方案                     |
|--------|----------------|------------------------------|
| 400    | 请求参数错误   | 检查请求参数格式是否正确     |
| 500    | 服务器内部错误 | 联系管理员或稍后重试         |

#### 1.5 示例

请求示例：
```bash
curl -X POST http://localhost:8000/search \
     -H "Content-Type: application/json" \
     -d '{"query": "指北AI的目标是什么？"}'
```

成功响应示例：
```json
{
    "answer": "指北AI的目标是成为国内最活跃和垂直的AI爱好者/从业者社区。",
    "sources": [
        {
            "content": "🎒指北AI："你的AGI社区大学" 💡指北AI的目标和愿景 ​ 🚅 目标：成为国内最活跃和垂直的AI爱好者/从业者社区。",
            "metadata": {
                "source": "feishu_doc.txt",
                "chunk_id": 0
            }
        }
    ]
}
```

错误响应示例：
```json
{
    "detail": "Internal server error"
}
```

## 前端实现建议

### 1. 页面布局

```html
<div class="container">
    <!-- 搜索框 -->
    <div class="search-box">
        <input type="text" placeholder="请输入您的问题...">
        <button>搜索</button>
    </div>
    
    <!-- 答案展示区 -->
    <div class="answer-box">
        <h3>答案</h3>
        <div class="answer-content"></div>
    </div>
    
    <!-- 来源展示区 -->
    <div class="sources-box">
        <h3>来源文档</h3>
        <div class="sources-list"></div>
    </div>
</div>
```

### 2. 样式建议

```css
.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.search-box {
    margin-bottom: 20px;
}

.search-box input {
    width: 80%;
    padding: 10px;
    font-size: 16px;
}

.search-box button {
    padding: 10px 20px;
    background-color: #1890ff;
    color: white;
    border: none;
    cursor: pointer;
}

.answer-box, .sources-box {
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #e8e8e8;
    border-radius: 4px;
}
```

### 3. 接口调用示例

```javascript
async function searchDocument(query) {
    try {
        const response = await fetch('http://localhost:8000/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query })
        });
        
        if (!response.ok) {
            throw new Error('请求失败');
        }
        
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Error:', error);
        showError('搜索失败，请稍后重试');
    }
}

function displayResults(data) {
    // 显示答案
    document.querySelector('.answer-content').innerHTML = data.answer;
    
    // 显示来源
    const sourcesList = document.querySelector('.sources-list');
    sourcesList.innerHTML = data.sources.map(source => `
        <div class="source-item">
            <div class="source-content">${source.content}</div>
            <div class="source-meta">来源：${source.metadata.source}</div>
        </div>
    `).join('');
}
```

### 4. 错误处理

```javascript
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.querySelector('.container').prepend(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 3000);
}
```

## 开发建议

1. **响应式设计**
   - 使用 flex/grid 布局
   - 适配移动端设备
   - 合理使用媒体查询

2. **用户体验**
   - 添加加载状态提示
   - 实现防抖处理
   - 添加错误提示
   - 支持按回车键搜索

3. **性能优化**
   - 实现请求缓存
   - 添加加载动画
   - 实现结果分页

4. **代码组织**
   - 使用 TypeScript
   - 遵循组件化开发
   - 添加单元测试
   - 使用状态管理

## 测试用例

1. 基础功能测试
```javascript
// 测试搜索功能
const testQueries = [
    "指北AI的目标是什么？",
    "如何联系投稿AI每日头条？",
    "有哪些AI爆款文章？"
];

// 运行测试
testQueries.forEach(query => {
    searchDocument(query);
});
```

2. 错误处理测试
```javascript
// 测试网络错误
searchDocument("").catch(err => {
    console.assert(err instanceof Error, "应该抛出错误");
});
```

## 部署说明

1. 本地开发
```bash
# 启动后端服务
uvicorn app:app --reload

# 启动前端开发服务器（如使用 Vue/React）
npm run dev
```

2. 生产环境
```bash
# 构建前端
npm run build

# 启动后端服务
uvicorn app:app --host 0.0.0.0 --port 8000
```
