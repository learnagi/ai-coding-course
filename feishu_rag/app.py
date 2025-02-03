from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import chromadb
import requests
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# 加载环境变量
load_dotenv()

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化Chroma客户端
client = chromadb.PersistentClient(path="db")
collection = client.get_collection("feishu_docs")

# 初始化模型
model = SentenceTransformer('all-MiniLM-L6-v2')

class Query(BaseModel):
    query: str

def get_embedding(text: str) -> list:
    """使用sentence-transformers生成文本的embedding"""
    try:
        # 生成embedding
        embedding = model.encode(text)
        # 转换为列表并返回
        return embedding.tolist()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成embedding失败: {str(e)}")

def get_completion(messages: list) -> str:
    """使用deepseek API生成回答"""
    try:
        api_key = os.getenv("DEEPSEEK_API_KEY", "")
        if not api_key:
            raise HTTPException(status_code=500, detail="未设置DEEPSEEK_API_KEY环境变量")
            
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成回答失败: {str(e)}")

@app.post("/search")
def search(query: Query):
    try:
        # 获取查询的embedding
        query_embedding = get_embedding(query.query)
        
        # 使用Chroma搜索相关文档
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
        
        # 构建上下文
        context = "\n\n".join(results["documents"][0])
        
        # 构建提示
        messages = [
            {"role": "system", "content": "你是一个智能助手。请基于给定的上下文信息，回答用户的问题。如果问题无法从上下文中得到答案，请说明无法回答。"},
            {"role": "user", "content": f"上下文信息：\n\n{context}\n\n问题：{query.query}"}
        ]
        
        # 生成回答
        answer = get_completion(messages)
        
        return {
            "answer": answer,
            "sources": [
                {
                    "content": doc,
                    "metadata": meta
                }
                for doc, meta in zip(results["documents"][0], results["metadatas"][0])
            ]
        }
    except Exception as e:
        import traceback
        error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)  # 打印到服务器日志
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
