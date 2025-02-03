import os
import requests
import chromadb
import tiktoken
from dotenv import load_dotenv
from feishu_crawler import fetch_feishu_doc, save_to_file
from sentence_transformers import SentenceTransformer

# 加载环境变量
load_dotenv()

# 初始化模型
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str) -> list:
    """使用sentence-transformers生成文本的embedding"""
    try:
        # 生成embedding
        embedding = model.encode(text)
        # 转换为列表并返回
        return embedding.tolist()
    except Exception as e:
        print(f"生成embedding失败: {str(e)}")
        return None

def num_tokens(text: str) -> int:
    """计算文本的token数量"""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(text))

def chunk_text(text: str, chunk_size: int = 1000) -> list:
    """将文本分割成更小的块"""
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0
    
    for word in words:
        current_chunk.append(word)
        current_size += len(word) + 1  # +1 for space
        
        if current_size >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_size = 0
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def main():
    """主函数：读取文档、生成embedding并存储到Chroma"""
    # 初始化Chroma客户端
    client = chromadb.PersistentClient(path="db")
    
    # 创建或获取集合
    collection = client.get_or_create_collection(name="feishu_docs")
    
    # 飞书文档URL
    url = "https://zhibei-ai.feishu.cn/wiki/M3awwxWQIi5c7ckv78lcvjxknPb"
    
    # 获取文档内容
    print("从飞书获取文档...")
    content = fetch_feishu_doc(url)
    
    if content:
        # 保存到本地
        save_to_file(content, "feishu_doc.txt")
        
        # 分块
        chunks = chunk_text(content)
        print(f"文档被分成 {len(chunks)} 块")
        
        # 为每块生成embedding并存储
        for idx, chunk in enumerate(chunks):
            print(f"处理第 {idx + 1}/{len(chunks)} 块...")
            embedding = get_embedding(chunk)
            if embedding:
                collection.add(
                    documents=[chunk],
                    metadatas=[{"source": "feishu_doc.txt", "chunk_id": idx}],
                    ids=[f"chunk_{idx}"],
                    embeddings=[embedding]
                )
        
        print("文档处理完成！")
    else:
        print("获取文档失败")

if __name__ == "__main__":
    main()
