# 🔥 抖音爆款分析系统 / TikTok Viral Video Analyzer

[![GitHub](https://img.shields.io/badge/GitHub-mkz0930%2Fdouyin--viral--analysis-blue?logo=github)](https://github.com/mkz0930/douyin-viral-analysis)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

自动分析每天全网最火视频的规律，提供数据驱动的爆款建议。

**🔗 GitHub Repository:** https://github.com/mkz0930/douyin-viral-analysis

## ✨ 功能特性 / Features

- 📊 **数据采集**: 模拟采集热门视频数据（可接入真实API）
- 🔍 **规律分析**: 自动分析时长、标签、音乐、分类等维度
- 📈 **趋势追踪**: SQLite数据库持久化，追踪长期趋势
- 📝 **每日报告**: 生成美观的分析报告
- 🤖 **自动化**: 支持定时任务，每日自动分析

## 🚀 快速开始 / Quick Start

### 1. 采集数据
```bash
python3 douyin_analyzer.py scrape
```

### 2. 生成报告
```bash
python3 douyin_analyzer.py report
```

### 3. 查看原始分析
```bash
python3 douyin_analyzer.py analyze
```

## 📊 分析维度 / Analysis Dimensions

### 1. 时长分析 / Duration Analysis
- 统计不同时长视频的数量分布
- 识别最佳时长（黄金时长）
- 建议: 15-60秒，最优45秒

### 2. 标签分析 / Tag Analysis
- 统计热门标签使用频率
- Top 5 热门标签排行
- 建议: #剧情反转、#流量密码、#好物推荐

### 3. 音乐分析 / Music Analysis
- 统计热门BGM使用频率
- Top 3 热门音乐排行
- 建议: 《孤勇者》、《踏山河》

### 4. 分类分析 / Category Analysis
- 统计热门内容分类
- 识别当前热门赛道
- 建议: 剧情、美食、旅游

### 5. 互动数据 / Engagement Metrics
- 平均播放量
- 平均点赞数
- 点赞率分析

## 🎯 爆款规律 / Viral Patterns

### 黄金3秒法则
- 前3秒必须有强钩子
- 悬念、冲突、反转、惊喜

### 最佳时长
- 15-60秒为最佳区间
- 45秒左右效果最好
- 太短信息不足，太长完播率低

### 热门标签
- 使用3-5个相关标签
- 包含1-2个热门标签
- 包含1-2个精准标签

### 热门音乐
- 选择当前热门BGM
- 音乐与内容匹配
- 注意版权问题

### 发布时间
- 12:00-14:00 (午休时间)
- 18:00-22:00 (晚间黄金时段)
- 避开凌晨时段

## 🤖 自动化 / Automation

### 每日定时分析
```bash
# 添加到 crontab
0 8 * * * cd /home/claw/tests/douyin_viral_analysis && python3 douyin_analyzer.py scrape
30 8 * * * cd /home/claw/tests/douyin_viral_analysis && python3 douyin_analyzer.py report
```

### OpenClaw Cron Job
```javascript
{
  name: "daily-douyin-analysis",
  schedule: { kind: "cron", expr: "0 8 * * *", tz: "Asia/Shanghai" },
  sessionTarget: "isolated",
  payload: {
    kind: "agentTurn",
    message: "Run douyin viral analysis: cd /home/claw/tests/douyin_viral_analysis && python3 douyin_analyzer.py scrape && python3 douyin_analyzer.py report",
    model: "gemini",
    thinking: "low"
  },
  delivery: {
    mode: "announce",
    channel: "feishu",
    to: "ou_2cf905e306a287382df58f01e8b6799e"
  }
}
```

## 📁 数据库结构 / Database Schema

### videos 表
- video_id: 视频ID
- title: 标题
- author: 作者
- views: 播放量
- likes: 点赞数
- comments: 评论数
- shares: 分享数
- duration: 时长（秒）
- tags: 标签（JSON）
- music: 音乐
- hook_time: 钩子出现时间（秒）
- category: 分类
- scraped_at: 采集时间

### daily_reports 表
- report_date: 报告日期
- total_videos: 视频总数
- avg_views: 平均播放量
- avg_duration: 平均时长
- top_tags: 热门标签
- top_music: 热门音乐
- insights: 分析洞察
- created_at: 创建时间

## 🔧 扩展功能 / Extensions

### 接入真实API
替换 `generate_mock_videos()` 为真实抖音API调用：
- 抖音开放平台API
- 第三方数据服务
- 爬虫采集（注意合规）

### 高级分析
- 文案分析（关键词、句式）
- 封面分析（颜色、构图）
- 账号分析（粉丝、垂类）
- 时间序列分析（趋势预测）

### 可视化
- Matplotlib 生成图表
- 导出 HTML 报告
- 数据看板

## 📝 示例输出 / Sample Output

```
╔══════════════════════════════════════════════════════════════╗
║          🔥 抖音爆款视频分析报告 / Viral Video Report          ║
║                  2026-02-10 23:56                      ║
╚══════════════════════════════════════════════════════════════╝

📊 数据概览 / Overview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 分析视频数: 50 个
• 平均播放量: 3,050,657 次
• 平均点赞数: 302,303 个
• 平均时长: 34 秒

⏱️ 最佳时长 / Optimal Duration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 黄金时长: 45 秒
...
```

## 🎓 学习资源 / Learning Resources

- [抖音创作者学院](https://creator.douyin.com/)
- [短视频运营指南](https://example.com)
- [数据分析最佳实践](https://example.com)

## 📄 License

MIT License

## 👨‍💻 Author

Claw - AI Assistant
Date: 2026-02-10
