import os
import requests
import json
from typing import List, Dict, Optional
import ast
import astor

class CodeGenius:
    def __init__(self, api_key: str):
        """初始化CodeGenius
        
        Args:
            api_key: DeepSeek API密钥
        """
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/v1/chat/completions"  # 示例URL
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def optimize_code(self, code: str) -> str:
        """优化代码结构和性能
        
        Args:
            code: 源代码字符串
        
        Returns:
            优化后的代码
        """
        prompt = f"""请优化以下代码，重点关注：
1. 代码结构优化
2. 性能提升
3. 最佳实践遵循
4. 可读性提升

源代码：
```python
{code}
```"""

        response = self._call_api(prompt)
        return self._extract_code(response)

    def generate_tests(self, code: str) -> str:
        """生成单元测试
        
        Args:
            code: 源代码字符串
        
        Returns:
            生成的单元测试代码
        """
        prompt = f"""请为以下代码生成完整的单元测试，包括：
1. 基本功能测试
2. 边界条件测试
3. 异常情况测试
4. 测试用例说明

源代码：
```python
{code}
```"""

        response = self._call_api(prompt)
        return self._extract_code(response)

    def generate_docs(self, code: str) -> str:
        """生成代码文档
        
        Args:
            code: 源代码字符串
        
        Returns:
            生成的文档字符串
        """
        prompt = f"""请为以下代码生成详细的文档，包括：
1. 功能说明
2. 参数描述
3. 返回值说明
4. 使用示例
5. 注意事项

源代码：
```python
{code}
```"""

        response = self._call_api(prompt)
        return response

    def analyze_performance(self, code: str) -> List[Dict]:
        """分析代码性能
        
        Args:
            code: 源代码字符串
        
        Returns:
            性能分析结果列表
        """
        prompt = f"""请分析以下代码的性能，指出：
1. 潜在的性能瓶颈
2. 优化建议
3. 复杂度分析
4. 资源使用评估

源代码：
```python
{code}
```"""

        response = self._call_api(prompt)
        return json.loads(response)

    def generate_api_docs(self, code: str) -> str:
        """生成API文档
        
        Args:
            code: 源代码字符串
        
        Returns:
            生成的API文档
        """
        try:
            # 解析代码为AST
            tree = ast.parse(code)
            
            # 收集API信息
            api_info = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    api_info.append({
                        'type': 'class' if isinstance(node, ast.ClassDef) else 'function',
                        'name': node.name,
                        'docstring': ast.get_docstring(node) or '',
                        'code': astor.to_source(node)
                    })

            # 生成API文档
            prompt = f"""请为以下API生成标准的API文档：
{json.dumps(api_info, indent=2)}

要求：
1. 使用标准的API文档格式
2. 包含详细的参数说明
3. 提供使用示例
4. 说明注意事项"""

            response = self._call_api(prompt)
            return response

        except Exception as e:
            return f"生成API文档时出错: {str(e)}"

    def _call_api(self, prompt: str) -> str:
        """调用DeepSeek API
        
        Args:
            prompt: 提示词
        
        Returns:
            API响应内容
        """
        try:
            payload = {
                "model": "deepseek-coder",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                raise Exception(f"API调用失败: {response.status_code}")
                
        except Exception as e:
            raise Exception(f"API调用出错: {str(e)}")

    def _extract_code(self, response: str) -> str:
        """从API响应中提取代码
        
        Args:
            response: API响应内容
        
        Returns:
            提取的代码字符串
        """
        # 简单的代码提取逻辑，可以根据需要优化
        try:
            code_start = response.find("```python")
            code_end = response.find("```", code_start + 8)
            
            if code_start != -1 and code_end != -1:
                return response[code_start + 8:code_end].strip()
            return response
            
        except Exception:
            return response
