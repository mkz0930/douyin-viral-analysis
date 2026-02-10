"""
抖音爆款分析系统 / TikTok Viral Analysis System
Author: Claw
Date: 2026-02-10
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import random

class DouyinViralAnalyzer:
    """抖音爆款视频分析器"""
    
    def __init__(self, db_path: str = "viral_videos.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT UNIQUE,
                title TEXT,
                author TEXT,
                views INTEGER,
                likes INTEGER,
                comments INTEGER,
                shares INTEGER,
                duration INTEGER,
                tags TEXT,
                music TEXT,
                hook_time INTEGER,
                category TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_date DATE UNIQUE,
                total_videos INTEGER,
                avg_views INTEGER,
                avg_duration INTEGER,
                top_tags TEXT,
                top_music TEXT,
                insights TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def generate_mock_videos(self, count: int = 50) -> List[Dict]:
        """生成模拟爆款视频数据"""
        
        categories = ["搞笑", "美食", "旅游", "知识", "剧情", "才艺", "萌宠", "好物"]
        tags_pool = [
            "#抖音热门", "#涨粉", "#必火", "#爆款", "#流量密码",
            "#搞笑日常", "#美食探店", "#旅行vlog", "#干货分享",
            "#剧情反转", "#才艺展示", "#萌宠日常", "#好物推荐"
        ]
        music_pool = [
            "《孤勇者》", "《本草纲目》", "《大风吹》", "《踏山河》",
            "《可可托海的牧羊人》", "《白月光与朱砂痣》", "《星辰大海》"
        ]
        authors = ["小明", "阿强", "美食家王姐", "旅行达人", "知识博主", "剧情号"]
        
        videos = []
        for i in range(count):
            # 爆款特征：高播放、高互动
            views = random.randint(100000, 5000000)
            likes = int(views * random.uniform(0.05, 0.15))  # 5-15% 点赞率
            comments = int(likes * random.uniform(0.1, 0.3))
            shares = int(likes * random.uniform(0.05, 0.15))
            
            # 最佳时长：15-60秒
            duration = random.choice([15, 20, 30, 45, 60])
            
            # 黄金3秒：前3秒必须有钩子
            hook_time = random.randint(1, 3)
            
            category = random.choice(categories)
            tags = random.sample(tags_pool, k=random.randint(3, 5))
            music = random.choice(music_pool)
            author = random.choice(authors)
            
            video = {
                "video_id": f"DY{datetime.now().strftime('%Y%m%d')}{i:04d}",
                "title": f"{category}爆款视频 #{i+1}",
                "author": author,
                "views": views,
                "likes": likes,
                "comments": comments,
                "shares": shares,
                "duration": duration,
                "tags": json.dumps(tags, ensure_ascii=False),
                "music": music,
                "hook_time": hook_time,
                "category": category
            }
            videos.append(video)
        
        return videos
    
    def save_videos(self, videos: List[Dict]):
        """保存视频数据到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for video in videos:
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO videos 
                    (video_id, title, author, views, likes, comments, shares, 
                     duration, tags, music, hook_time, category)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    video["video_id"], video["title"], video["author"],
                    video["views"], video["likes"], video["comments"], video["shares"],
                    video["duration"], video["tags"], video["music"],
                    video["hook_time"], video["category"]
                ))
            except sqlite3.IntegrityError:
                pass  # Skip duplicates
        
        conn.commit()
        conn.close()
    
    def analyze_patterns(self) -> Dict:
        """分析爆款规律"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取最近的视频数据
        cursor.execute("""
            SELECT * FROM videos 
            WHERE scraped_at >= datetime('now', '-1 day')
            ORDER BY views DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return {"error": "No data available"}
        
        # 分析维度
        total_videos = len(rows)
        avg_views = sum(row[4] for row in rows) / total_videos
        avg_likes = sum(row[5] for row in rows) / total_videos
        avg_duration = sum(row[8] for row in rows) / total_videos
        
        # 最佳时长分布
        duration_dist = {}
        for row in rows:
            dur = row[8]
            duration_dist[dur] = duration_dist.get(dur, 0) + 1
        
        optimal_duration = max(duration_dist, key=duration_dist.get)
        
        # 热门标签
        all_tags = []
        for row in rows:
            tags = json.loads(row[9])
            all_tags.extend(tags)
        
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # 热门音乐
        music_counts = {}
        for row in rows:
            music = row[10]
            music_counts[music] = music_counts.get(music, 0) + 1
        
        top_music = sorted(music_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # 分类分布
        category_dist = {}
        for row in rows:
            cat = row[12]
            category_dist[cat] = category_dist.get(cat, 0) + 1
        
        top_categories = sorted(category_dist.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "total_videos": total_videos,
            "avg_views": int(avg_views),
            "avg_likes": int(avg_likes),
            "avg_duration": int(avg_duration),
            "optimal_duration": optimal_duration,
            "duration_distribution": duration_dist,
            "top_tags": top_tags,
            "top_music": top_music,
            "top_categories": top_categories
        }
    
    def generate_report(self) -> str:
        """生成每日分析报告"""
        analysis = self.analyze_patterns()
        
        if "error" in analysis:
            return "❌ 暂无数据，请先运行 scrape 命令采集数据"
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║          🔥 抖音爆款视频分析报告 / Viral Video Report          ║
║                  {datetime.now().strftime('%Y-%m-%d %H:%M')}                      ║
╚══════════════════════════════════════════════════════════════╝

📊 数据概览 / Overview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 分析视频数: {analysis['total_videos']} 个
• 平均播放量: {analysis['avg_views']:,} 次
• 平均点赞数: {analysis['avg_likes']:,} 个
• 平均时长: {analysis['avg_duration']} 秒

⏱️ 最佳时长 / Optimal Duration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 黄金时长: {analysis['optimal_duration']} 秒

时长分布:
"""
        
        for dur, count in sorted(analysis['duration_distribution'].items()):
            bar = "█" * (count * 2)
            report += f"  {dur:2d}秒: {bar} ({count}个)\n"
        
        report += f"""
🏷️ 热门标签 / Top Tags
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for i, (tag, count) in enumerate(analysis['top_tags'], 1):
            report += f"  {i}. {tag} ({count}次)\n"
        
        report += f"""
🎵 热门音乐 / Top Music
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for i, (music, count) in enumerate(analysis['top_music'], 1):
            report += f"  {i}. {music} ({count}次)\n"
        
        report += f"""
📂 热门分类 / Top Categories
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for i, (cat, count) in enumerate(analysis['top_categories'], 1):
            report += f"  {i}. {cat} ({count}个)\n"
        
        report += f"""
💡 爆款建议 / Recommendations
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. ⏱️ 控制时长在 {analysis['optimal_duration']} 秒左右
2. 🎯 前3秒必须有强钩子（悬念/冲突/反转）
3. 🏷️ 使用热门标签: {', '.join([t[0] for t in analysis['top_tags'][:3]])}
4. 🎵 选择热门音乐: {analysis['top_music'][0][0]}
5. 📂 热门赛道: {', '.join([c[0] for c in analysis['top_categories']])}
6. 💬 引导互动（评论/点赞/转发）
7. 📅 发布时间: 12:00-14:00, 18:00-22:00

╚══════════════════════════════════════════════════════════════╝
"""
        
        return report


def main():
    """主函数"""
    import sys
    
    analyzer = DouyinViralAnalyzer()
    
    if len(sys.argv) < 2:
        print("用法: python douyin_analyzer.py [scrape|analyze|report]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "scrape":
        print("🔍 正在采集爆款视频数据...")
        videos = analyzer.generate_mock_videos(count=50)
        analyzer.save_videos(videos)
        print(f"✅ 成功采集 {len(videos)} 个视频数据")
    
    elif command == "analyze":
        print("📊 正在分析爆款规律...")
        analysis = analyzer.analyze_patterns()
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
    
    elif command == "report":
        print(analyzer.generate_report())
    
    else:
        print(f"❌ 未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
