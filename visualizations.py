"""
MES专业可视化模块
创建适合制药行业的专业图表
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class MESVisualizations:
    """MES专业可视化类"""
    
    # 制药行业专业配色
    PHARMA_COLORS = {
        "primary_blue": "#1E3A8A",
        "secondary_blue": "#3B82F6",
        "pharma_green": "#10B981",
        "pharma_teal": "#14B8A6",
        "warning_orange": "#F59E0B",
        "danger_red": "#EF4444",
        "success_green": "#22C55E",
        "dark_bg": "#111827",
        "card_bg": "#1F2937",
        "border_color": "#374151"
    }
    
    @staticmethod
    def create_gmp_process_flow(steps, product_name, width=800, height=500):
        """创建GMP工艺流程图"""
        fig = go.Figure()
        
        num_steps = len(steps)
        if num_steps == 0:
            return fig
        
        # 计算节点位置
        x_positions = np.linspace(0.1, 0.9, num_steps)
        y_position = 0.5
        
        # 添加步骤节点
        for i, step in enumerate(steps):
            step_name = step.get("name", "")
            params = step.get("关键参数", [])
            
            # 确定节点颜色和大小（基于风险）
            is_critical = any(keyword in step_name for keyword in ["灭菌", "无菌", "病毒", "灌装"])
            node_color = MESVisualizations.PHARMA_COLORS["danger_red"] if is_critical else MESVisualizations.PHARMA_COLORS["secondary_blue"]
            node_size = 50 if is_critical else 40
            
            # 节点形状
            node_symbol = "diamond" if is_critical else "circle"
            
            # 添加节点
            fig.add_trace(go.Scatter(
                x=[x_positions[i]],
                y=[y_position],
                mode="markers+text",
                marker=dict(
                    size=node_size,
                    color=node_color,
                    line=dict(width=3, color='white'),
                    symbol=node_symbol
                ),
                text=[f"{i+1}"],
                textposition="middle center",
                textfont=dict(size=14, color="white", family="Arial Black"),
                name=step_name,
                hoverinfo="text",
                hovertext=f"<b>步骤 {i+1}: {step_name}</b><br>" +
                         f"<b>关键参数:</b> {', '.join(params[:3])}<br>" +
                         f"<b>设备:</b> {', '.join(step.get('设备', ['N/A'])[:2])}<br>" +
                         f"<b>时间:</b> {step.get('时间', 'N/A')}",
                customdata=[{"step_num": i+1, "is_critical": is_critical}]
            ))
            
            # 添加步骤标签
            fig.add_annotation(
                x=x_positions[i],
                y=y_position - 0.15,
                text=step_name,
                showarrow=False,
                font=dict(size=11, color="#D1D5DB", family="Arial"),
                yref="y"
            )
        
        # 添加连接线
        for i in range(num_steps - 1):
            fig.add_trace(go.Scatter(
                x=[x_positions[i] + 0.02, x_positions[i+1] - 0.02],
                y=[y_position, y_position],
                mode="lines",
                line=dict(width=3, color=MESVisualizations.PHARMA_COLORS["pharma_teal"], dash='solid'),
                hoverinfo="none",
                showlegend=False
            ))
            
            # 添加流向箭头
            mid_x = (x_positions[i] + x_positions[i+1]) / 2
            fig.add_annotation(
                x=mid_x,
                y=y_position,
                ax=mid_x - 0.015,
                ay=y_position,
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                showarrow=True,
                arrowhead=3,
                arrowsize=1.2,
                arrowwidth=2,
                arrowcolor="#FFFFFF"
            )
        
        # 添加工艺边界
        fig.add_annotation(
            x=0.01,
            y=y_position,
            text="🏁 开始",
            showarrow=False,
            font=dict(size=14, color=MESVisualizations.PHARMA_COLORS["success_green"], family="Arial Black"),
            xref="paper"
        )
        
        fig.add_annotation(
            x=0.99,
            y=y_position,
            text="✅ 完成",
            showarrow=False,
            font=dict(size=14, color=MESVisualizations.PHARMA_COLORS["success_green"], family="Arial Black"),
            xref="paper"
        )
        
        # 更新布局
        fig.update_layout(
            title=dict(
                text=f"<b>{product_name}</b> 工艺流程图<br><sub>红色菱形表示关键步骤</sub>",
                font=dict(size=18, color="white", family="Arial"),
                x=0.5
            ),
            height=height,
            width=width,
            showlegend=False,
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                range=[0, 1]
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                range=[0, 1]
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=80, b=20),
            hoverlabel=dict(
                bgcolor=MESVisualizations.PHARMA_COLORS["card_bg"],
                font_size=12,
                font_color="white",
                bordercolor=MESVisualizations.PHARMA_COLORS["border_color"]
            )
        )
        
        return fig
    
    @staticmethod
    def create_risk_assessment_chart(risk_data, width=600, height=400):
        """创建风险评估图表"""
        if not risk_data:
            return go.Figure()
        
        # 提取数据
        risk_level = risk_data.get("risk_level", "")
        avg_score = risk_data.get("average_risk_score", 0)
        critical_steps = risk_data.get("critical_steps", [])
        
        # 创建仪表盘图
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "工艺风险评分", 'font': {'size': 20}},
            delta={'reference': 3, 'increasing': {'color': "red"}},
            gauge={
                'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "darkblue"},
                'bgcolor': "black",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 2], 'color': '#10B981'},  # 绿色
                    {'range': [2, 4], 'color': '#22C55E'},
                    {'range': [4, 6], 'color': '#F59E0B'},  # 黄色
                    {'range': [6, 8], 'color': '#F97316'},  # 橙色
                    {'range': [8, 10], 'color': '#EF4444'}  # 红色
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': avg_score
                }
            }
        ))
        
        fig.update_layout(
            height=height,
            width=width,
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': "white", 'family': "Arial"}
        )
        
        return fig
    
    @staticmethod
    def create_comparison_radar_chart(products_data, width=700, height=500):
        """创建多产品对比雷达图"""
        if not products_data:
            return go.Figure()
        
        categories = ['步骤复杂度', '参数控制', '设备需求', '时间效率', '风险等级']
        
        fig = go.Figure()
        
        colors = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899']
        
        for idx, product in enumerate(products_data):
            if idx >= 5:  # 最多显示5个产品
                break
                
            # 计算各项得分（简化版）
            steps = product.get("steps", [])
            values = [
                len(steps) / 20 * 10,  # 步骤复杂度
                sum(len(step.get("关键参数", [])) for step in steps) / 50 * 10,  # 参数控制
                len(set(equip for step in steps for equip in step.get("设备", []))) / 15 * 10,  # 设备需求
                10 - (sum(float(str(step.get("时间", "0")).replace("(h)", "")) for step in steps if "时间" in step) / 100),  # 时间效率
                MESVisualizations._estimate_risk_score(steps)  # 风险等级
            ]
            
            # 确保值在合理范围内
            values = [min(max(v, 0), 10) for v in values]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=product.get("name", f"产品{idx+1}"),
                line_color=colors[idx % len(colors)],
                fillcolor=f"rgba{tuple(int(colors[idx % len(colors)][i:i+2], 16) for i in (1, 3, 5)) + (0.3,)}"
            ))
        
        fig.update_layout(
            polar=dict(
                bgcolor=MESVisualizations.PHARMA_COLORS["card_bg"],
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    gridcolor=MESVisualizations.PHARMA_COLORS["border_color"],
                    color="white"
                ),
                angularaxis=dict(
                    gridcolor=MESVisualizations.PHARMA_COLORS["border_color"],
                    color="white"
                )
            ),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.05,
                bgcolor='rgba(0,0,0,0.5)',
                bordercolor=MESVisualizations.PHARMA_COLORS["border_color"]
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="white",
            height=height,
            width=width,
            title=dict(
                text="多产品工艺对比雷达图",
                font=dict(size=16, color="white")
            )
        )
        
        return fig
    
    @staticmethod
    def _estimate_risk_score(steps):
        """估算风险得分"""
        if not steps:
            return 0
        
        risk_score = 0
        for step in steps:
            step_name = step.get("name", "")
            if any(keyword in step_name for keyword in ["灭菌", "无菌", "病毒"]):
                risk_score += 3
            elif any(keyword in step_name for keyword in ["灌装", "过滤", "层析"]):
                risk_score += 2
            else:
                risk_score += 1
        
        avg_risk = risk_score / len(steps)
        return min(avg_risk * 2, 10)  # 转换为0-10分
    
    @staticmethod
    def create_parameter_trend_chart(parameter_data, width=800, height=400):
        """创建参数趋势图表（模拟批记录数据）"""
        if not parameter_data:
            return go.Figure()
        
        # 生成模拟数据
        batches = list(range(1, 21))
        np.random.seed(42)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("温度控制趋势", "pH值趋势", "压力控制趋势", "含量均匀性"),
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        # 温度趋势
        temp_data = 25 + np.random.randn(20) * 2
        fig.add_trace(
            go.Scatter(x=batches, y=temp_data, mode='lines+markers', 
                      name='温度', line=dict(color=MESVisualizations.PHARMA_COLORS["secondary_blue"])),
            row=1, col=1
        )
        fig.add_hline(y=25, line_dash="dash", line_color="green", row=1, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="red", row=1, col=1)
        fig.add_hline(y=20, line_dash="dash", line_color="red", row=1, col=1)
        
        # pH趋势
        ph_data = 7.0 + np.random.randn(20) * 0.3
        fig.add_trace(
            go.Scatter(x=batches, y=ph_data, mode='lines+markers',
                      name='pH', line=dict(color=MESVisualizations.PHARMA_COLORS["pharma_green"])),
            row=1, col=2
        )
        fig.add_hline(y=7.0, line_dash="dash", line_color="green", row=1, col=2)
        fig.add_hline(y=7.5, line_dash="dash", line_color="red", row=1, col=2)
        fig.add_hline(y=6.5, line_dash="dash", line_color="red", row=1, col=2)
        
        # 压力趋势
        pressure_data = 1.0 + np.random.randn(20) * 0.2
        fig.add_trace(
            go.Scatter(x=batches, y=pressure_data, mode='lines+markers',
                      name='压力', line=dict(color=MESVisualizations.PHARMA_COLORS["warning_orange"])),
            row=2, col=1
        )
        fig.add_hline(y=1.0, line_dash="dash", line_color="green", row=2, col=1)
        fig.add_hline(y=1.5, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=0.5, line_dash="dash", line_color="red", row=2, col=1)
        
        # 含量均匀性
        content_data = 100 + np.random.randn(20) * 2
        fig.add_trace(
            go.Scatter(x=batches, y=content_data, mode='lines+markers',
                      name='含量', line=dict(color=MESVisualizations.PHARMA_COLORS["pharma_teal"])),
            row=2, col=2
        )
        fig.add_hline(y=100, line_dash="dash", line_color="green", row=2, col=2)
        fig.add_hline(y=105, line_dash="dash", line_color="red", row=2, col=2)
        fig.add_hline(y=95, line_dash="dash", line_color="red", row=2, col=2)
        
        # 更新布局
        fig.update_layout(
            height=height,
            width=width,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="white",
            title=dict(
                text="关键工艺参数趋势分析 (20批次数据)",
                font=dict(size=16, color="white"),
                x=0.5
            )
        )
        
        # 更新子图标题颜色
        for annotation in fig['layout']['annotations']:
            annotation['font'] = dict(size=12, color="white")
        
        return fig
