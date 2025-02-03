'use client';

import { useState } from 'react';

export default function Home() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      const data = await response.json();
      setAnswer(data.answer);
      setSources(data.sources);
    } catch (error) {
      console.error('搜索失败:', error);
      setAnswer('抱歉，搜索过程中出现错误。');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-8 max-w-4xl mx-auto">
      <div className="space-y-8">
        {/* 标题 */}
        <h1 className="text-3xl font-bold text-center text-gray-800">
          飞书文档智能问答系统
        </h1>

        {/* 搜索框 */}
        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="输入您的问题..."
            className="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSearch}
            disabled={loading}
            className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400"
          >
            {loading ? '搜索中...' : '搜索'}
          </button>
        </div>

        {/* 答案区域 */}
        {answer && (
          <div className="space-y-4">
            <div className="p-6 bg-white rounded-lg shadow">
              <h2 className="text-xl font-semibold mb-4">回答：</h2>
              <p className="text-gray-700 whitespace-pre-wrap">{answer}</p>
            </div>

            {/* 来源文档 */}
            <div className="space-y-4">
              <h2 className="text-xl font-semibold">参考来源：</h2>
              {sources.map((source, index) => (
                <div
                  key={index}
                  className="p-4 bg-gray-50 rounded-lg border border-gray-200"
                >
                  <div className="text-sm text-gray-500 mb-2">
                    来源：{source.metadata.source}
                  </div>
                  <p className="text-gray-700">{source.content}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
