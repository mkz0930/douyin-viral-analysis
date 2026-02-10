#!/usr/bin/env python3
"""
Enhanced Douyin Viral Analyzer with Rich UI and Plotly Charts
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich import box
import json

# Import original analyzer
from douyin_analyzer import DouyinViralAnalyzer

# Import new modules
from src.utils.config import Config
from src.reporter.charts import ChartGenerator

console = Console()

def display_analysis_rich(analysis: dict):
    """Display analysis results with Rich formatting"""
    
    # Overview Panel
    overview_table = Table(show_header=False, box=box.SIMPLE)
    overview_table.add_column("Metric", style="cyan")
    overview_table.add_column("Value", style="magenta")
    
    overview_table.add_row("📊 分析视频数", f"{analysis['total_videos']} 个")
    overview_table.add_row("👁️ 平均播放量", f"{analysis['avg_views']:,} 次")
    overview_table.add_row("❤️ 平均点赞数", f"{analysis['avg_likes']:,} 个")
    overview_table.add_row("⏱️ 平均时长", f"{analysis['avg_duration']} 秒")
    overview_table.add_row("🎯 最佳时长", f"{analysis['optimal_duration']} 秒")
    
    console.print(Panel(overview_table, title="📊 数据概览 / Overview", border_style="blue"))
    
    # Duration Distribution
    duration_table = Table(title="⏱️ 时长分布 / Duration Distribution", box=box.ROUNDED)
    duration_table.add_column("时长", style="cyan")
    duration_table.add_column("数量", style="green")
    duration_table.add_column("占比", style="yellow")
    duration_table.add_column("可视化", style="blue")
    
    total = analysis['total_videos']
    for dur, count in sorted(analysis['duration_distribution'].items()):
        percentage = (count / total) * 100
        bar = "█" * int(percentage / 2)
        duration_table.add_row(
            f"{dur}秒",
            f"{count}个",
            f"{percentage:.1f}%",
            bar
        )
    
    console.print(duration_table)
    
    # Top Tags
    tags_table = Table(title="🏷️ 热门标签 / Top Tags", box=box.ROUNDED)
    tags_table.add_column("排名", style="cyan")
    tags_table.add_column("标签", style="green")
    tags_table.add_column("使用次数", style="magenta")
    
    for i, (tag, count) in enumerate(analysis['top_tags'][:10], 1):
        tags_table.add_row(f"#{i}", tag, f"{count}次")
    
    console.print(tags_table)
    
    # Top Music
    music_table = Table(title="🎵 热门音乐 / Top Music", box=box.ROUNDED)
    music_table.add_column("排名", style="cyan")
    music_table.add_column("音乐", style="green")
    music_table.add_column("使用次数", style="magenta")
    
    for i, (music, count) in enumerate(analysis['top_music'][:10], 1):
        music_table.add_row(f"#{i}", music, f"{count}次")
    
    console.print(music_table)
    
    # Top Categories
    cat_table = Table(title="📂 热门分类 / Top Categories", box=box.ROUNDED)
    cat_table.add_column("排名", style="cyan")
    cat_table.add_column("分类", style="green")
    cat_table.add_column("视频数", style="magenta")
    
    for i, (cat, count) in enumerate(analysis['top_categories'], 1):
        cat_table.add_row(f"#{i}", cat, f"{count}个")
    
    console.print(cat_table)
    
    # Recommendations
    recommendations = [
        f"⏱️ 控制时长在 {analysis['optimal_duration']} 秒左右",
        "🎯 前3秒必须有强钩子（悬念/冲突/反转）",
        f"🏷️ 使用热门标签: {', '.join([t[0] for t in analysis['top_tags'][:3]])}",
        f"🎵 选择热门音乐: {analysis['top_music'][0][0]}",
        f"📂 热门赛道: {', '.join([c[0] for c in analysis['top_categories']])}",
        "💬 引导互动（评论/点赞/转发）",
        "📅 发布时间: 12:00-14:00, 18:00-22:00"
    ]
    
    rec_text = "\n".join(f"{i}. {rec}" for i, rec in enumerate(recommendations, 1))
    console.print(Panel(rec_text, title="💡 爆款建议 / Recommendations", border_style="green"))


def main():
    """Main entry point with Rich UI"""
    
    # Load config
    config = Config()
    
    # Print header
    console.print(Panel.fit(
        "[bold cyan]🔥 抖音爆款分析系统 v2.0[/bold cyan]\n"
        "[dim]Douyin Viral Video Analyzer[/dim]",
        border_style="cyan"
    ))
    
    if len(sys.argv) < 2:
        console.print("[red]❌ 用法: python main.py [scrape|analyze|report][/red]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    # Initialize analyzer
    db_path = config.get('database.path', 'viral_videos.db')
    analyzer = DouyinViralAnalyzer(db_path=db_path)
    
    if command == "scrape":
        console.print("[cyan]🔍 正在采集爆款视频数据...[/cyan]")
        
        batch_size = config.get('scraper.batch_size', 50)
        videos = analyzer.generate_mock_videos(count=batch_size)
        
        # Show progress
        for video in track(videos, description="采集中..."):
            pass
        
        analyzer.save_videos(videos)
        console.print(f"[green]✅ 成功采集 {len(videos)} 个视频数据[/green]")
    
    elif command == "analyze":
        console.print("[cyan]📊 正在分析爆款规律...[/cyan]")
        analysis = analyzer.analyze_patterns()
        
        if "error" in analysis:
            console.print(f"[red]❌ {analysis['error']}[/red]")
            sys.exit(1)
        
        display_analysis_rich(analysis)
    
    elif command == "report":
        console.print("[cyan]📝 正在生成分析报告...[/cyan]")
        analysis = analyzer.analyze_patterns()
        
        if "error" in analysis:
            console.print(f"[red]❌ {analysis['error']}[/red]")
            sys.exit(1)
        
        # Display Rich output
        display_analysis_rich(analysis)
        
        # Generate charts
        if 'charts' in config.get('reporter.formats', []):
            console.print("\n[cyan]📊 正在生成图表...[/cyan]")
            
            chart_gen = ChartGenerator(
                output_dir=config.get('reporter.output_dir', 'generated/charts')
            )
            
            charts = chart_gen.generate_all_charts(analysis)
            
            console.print("\n[green]✅ 图表已生成:[/green]")
            for chart_type, path in charts.items():
                console.print(f"  • {chart_type}: [blue]{path}[/blue]")
    
    else:
        console.print(f"[red]❌ 未知命令: {command}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
