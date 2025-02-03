import requests
from bs4 import BeautifulSoup
import json
import os
import time

def fetch_feishu_doc(url: str) -> str:
    """从飞书公开文档URL获取内容"""
    try:
        # 添加请求头，模拟浏览器访问
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        
        # 发送GET请求获取页面内容
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 移除不需要的元素
        for element in soup.select('div[class*="header"], div[class*="footer"], div[class*="sidebar"]'):
            element.decompose()
        
        # 查找文档内容
        content_elements = soup.select('div[class*="wiki-content"]') or \
                         soup.select('div[class*="docx-content"]') or \
                         soup.select('div[class*="content"]')
        
        if content_elements:
            # 获取所有段落文本
            paragraphs = []
            for element in content_elements:
                # 移除分享按钮等无关元素
                for btn in element.select('button, .share-btn, .edit-btn'):
                    btn.decompose()
                
                # 获取所有文本节点
                for text in element.stripped_strings:
                    text = text.strip()
                    # 过滤掉一些无用的文本
                    if text and not any(skip in text.lower() for skip in [
                        '分享', '输入"/"', '快速插入', '修改', '创建', 
                        '飞书用户', '复制链接', '编辑'
                    ]):
                        paragraphs.append(text)
            
            # 合并所有段落，使用换行符分隔
            text_content = '\n\n'.join(filter(None, paragraphs))
            return text_content
        else:
            print("未找到文档内容")
            return ""
            
    except Exception as e:
        print(f"获取文档失败: {str(e)}")
        return ""

def save_to_file(content: str, filename: str):
    """保存内容到文件"""
    os.makedirs("docs", exist_ok=True)
    with open(f"docs/{filename}", "w", encoding="utf-8") as f:
        f.write(content)

def main():
    # 飞书文档URL
    url = "https://zhibei-ai.feishu.cn/wiki/M3awwxWQIi5c7ckv78lcvjxknPb"
    
    print("正在获取文档内容...")
    content = fetch_feishu_doc(url)
    
    if content:
        # 保存到文件
        save_to_file(content, "feishu_doc.txt")
        print(f"文档内容已保存到 docs/feishu_doc.txt")
        print(f"文档长度: {len(content)} 字符")
        
        # 预览内容
        preview = content[:500] + "..." if len(content) > 500 else content
        print("\n文档预览:")
        print("-" * 80)
        print(preview)
        print("-" * 80)
    else:
        print("获取文档失败")

if __name__ == "__main__":
    main()
