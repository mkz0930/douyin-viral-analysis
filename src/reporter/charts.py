"""
Chart generation module using Plotly
"""
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from typing import Dict, List, Tuple
import json

class ChartGenerator:
    """Generate interactive charts for viral video analysis"""
    
    def __init__(self, output_dir: str = "generated/charts"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_duration_chart(self, duration_dist: Dict[int, int]) -> str:
        """Generate duration distribution bar chart"""
        durations = sorted(duration_dist.keys())
        counts = [duration_dist[d] for d in durations]
        
        fig = go.Figure(data=[
            go.Bar(
                x=[f"{d}秒" for d in durations],
                y=counts,
                marker_color='rgb(55, 83, 109)',
                text=counts,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='视频时长分布 / Duration Distribution',
            xaxis_title='时长 / Duration',
            yaxis_title='视频数量 / Count',
            template='plotly_white',
            height=500
        )
        
        output_path = self.output_dir / 'duration_distribution.html'
        fig.write_html(str(output_path))
        return str(output_path)
    
    def generate_tag_chart(self, top_tags: List[Tuple[str, int]]) -> str:
        """Generate tag frequency chart"""
        tags = [t[0] for t in top_tags]
        counts = [t[1] for t in top_tags]
        
        fig = go.Figure(data=[
            go.Bar(
                y=tags,
                x=counts,
                orientation='h',
                marker_color='rgb(26, 118, 255)',
                text=counts,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='热门标签 Top 10 / Top Tags',
            xaxis_title='使用次数 / Count',
            yaxis_title='标签 / Tag',
            template='plotly_white',
            height=600
        )
        
        output_path = self.output_dir / 'top_tags.html'
        fig.write_html(str(output_path))
        return str(output_path)
    
    def generate_music_chart(self, top_music: List[Tuple[str, int]]) -> str:
        """Generate music trend chart"""
        music = [m[0] for m in top_music]
        counts = [m[1] for m in top_music]
        
        fig = go.Figure(data=[
            go.Bar(
                x=music,
                y=counts,
                marker_color='rgb(255, 127, 14)',
                text=counts,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='热门音乐 / Top Music',
            xaxis_title='音乐 / Music',
            yaxis_title='使用次数 / Count',
            template='plotly_white',
            height=500,
            xaxis_tickangle=-45
        )
        
        output_path = self.output_dir / 'top_music.html'
        fig.write_html(str(output_path))
        return str(output_path)
    
    def generate_category_chart(self, top_categories: List[Tuple[str, int]]) -> str:
        """Generate category pie chart"""
        categories = [c[0] for c in top_categories]
        counts = [c[1] for c in top_categories]
        
        fig = go.Figure(data=[
            go.Pie(
                labels=categories,
                values=counts,
                hole=0.3,
                marker_colors=px.colors.qualitative.Set3
            )
        ])
        
        fig.update_layout(
            title='分类分布 / Category Distribution',
            template='plotly_white',
            height=500
        )
        
        output_path = self.output_dir / 'category_distribution.html'
        fig.write_html(str(output_path))
        return str(output_path)
    
    def generate_all_charts(self, analysis: Dict) -> Dict[str, str]:
        """Generate all charts from analysis data"""
        charts = {}
        
        if 'duration_distribution' in analysis:
            charts['duration'] = self.generate_duration_chart(
                analysis['duration_distribution']
            )
        
        if 'top_tags' in analysis:
            charts['tags'] = self.generate_tag_chart(
                analysis['top_tags'][:10]  # Top 10
            )
        
        if 'top_music' in analysis:
            charts['music'] = self.generate_music_chart(
                analysis['top_music'][:10]  # Top 10
            )
        
        if 'top_categories' in analysis:
            charts['categories'] = self.generate_category_chart(
                analysis['top_categories']
            )
        
        return charts
