import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import openpyxl

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 对于macOS
plt.rcParams['axes.unicode_minus'] = False

def load_channel_data():
    """加载渠道数据"""
    df = pd.read_excel('SampleData.xlsx', sheet_name='Channel_Data')
    # 将ROI从百分比字符串转换为浮点数
    df['ROI'] = df['ROI'].str.rstrip('%').astype(float) / 100
    return df

def plot_roi_trends(df):
    """绘制各渠道ROI趋势"""
    plt.figure(figsize=(12, 6))
    for channel in df['Channel'].unique():
        channel_data = df[df['Channel'] == channel]
        plt.plot(channel_data['Date'], channel_data['ROI'], marker='o', label=channel)
    
    plt.title('各营销渠道ROI趋势')
    plt.xlabel('日期')
    plt.ylabel('ROI')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('roi_trends.png')
    plt.close()

def compare_media_types(df):
    """对比新媒体和传统渠道"""
    new_media = ['Xiaohongshu', 'Douyin', 'Bilibili']
    df['Channel_Type'] = df['Channel'].apply(lambda x: '新媒体' if x in new_media else '传统渠道')
    
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='Channel_Type', y='ROI')
    plt.title('新媒体 vs 传统渠道 ROI对比')
    plt.xlabel('渠道类型')
    plt.ylabel('ROI')
    plt.savefig('media_comparison.png')
    plt.close()
    
    # 计算平均ROI
    avg_roi = df.groupby('Channel_Type')['ROI'].mean()
    return avg_roi

def top_performing_channels(df):
    """找出ROI最高的渠道"""
    top_channels = df.groupby('Channel')['ROI'].mean().sort_values(ascending=False).head(3)
    
    plt.figure(figsize=(10, 6))
    top_channels.plot(kind='bar')
    plt.title('ROI最高的前三个渠道')
    plt.xlabel('渠道')
    plt.ylabel('平均ROI')
    plt.tight_layout()
    plt.savefig('top_channels.png')
    plt.close()
    
    return top_channels

def generate_report(avg_roi, top_channels):
    """生成分析报告"""
    report = f"""# 营销渠道ROI分析报告

## 1. 新媒体vs传统渠道对比
- 新媒体平均ROI: {avg_roi['新媒体']:.2%}
- 传统渠道平均ROI: {avg_roi['传统渠道']:.2%}
- 差异分析: 新媒体渠道的ROI {'高于' if avg_roi['新媒体'] > avg_roi['传统渠道'] else '低于'}传统渠道

## 2. 表现最佳的前三个渠道
1. {top_channels.index[0]}: {top_channels.iloc[0]:.2%}
2. {top_channels.index[1]}: {top_channels.iloc[1]:.2%}
3. {top_channels.index[2]}: {top_channels.iloc[2]:.2%}

## 3. 优化建议
1. {'加大新媒体投入' if avg_roi['新媒体'] > avg_roi['传统渠道'] else '优化新媒体策略'}
2. 重点关注{top_channels.index[0]}和{top_channels.index[1]}的成功经验
3. 考虑调整投资组合，将更多资源分配给高ROI渠道
4. 定期监控ROI变化，及时调整营销策略

## 4. 风险提示
- 需要综合考虑渠道的用户质量和长期价值
- 建议进行A/B测试验证优化方案
- 关注竞品动向，保持竞争优势
"""
    with open('marketing_roi_report.md', 'w', encoding='utf-8') as f:
        f.write(report)

def main():
    # 加载数据
    df = load_channel_data()
    
    # 生成分析图表
    plot_roi_trends(df)
    avg_roi = compare_media_types(df)
    top_channels = top_performing_channels(df)
    
    # 生成报告
    generate_report(avg_roi, top_channels)
    
    print("分析完成！请查看生成的图表和报告：")
    print("1. roi_trends.png - ROI趋势图")
    print("2. media_comparison.png - 新媒体vs传统渠道对比")
    print("3. top_channels.png - 最佳渠道分析")
    print("4. marketing_roi_report.md - 详细分析报告")

if __name__ == "__main__":
    main()
