"""
UI组件模块 - 为MES专业人员设计的专业组件
"""

import streamlit as st
from typing import List, Dict, Any, Tuple
import pandas as pd

class PharmaComponents:
    """制药行业专业UI组件"""
    
    @staticmethod
    def create_header():
        """创建专业页眉"""
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1E3A8A 0%, #111827 100%);
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 6px solid #10B981;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <h1 style="
                    margin: 0;
                    background: linear-gradient(135deg, #3B82F6, #14B8A6);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    font-size: 2.5rem;
                ">🧬 制药工艺流程MES系统</h1>
            </div>
            <div style="
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
                margin-top: 10px;
            ">
                <span style="
                    background: rgba(59, 130, 246, 0.2);
                    padding: 5px 12px;
                    border-radius: 20px;
                    font-size: 0.9rem;
                    color: #93C5FD;
                    border: 1px solid #3B82F6;
                ">GMP合规</span>
                <span style="
                    background: rgba(16, 185, 129, 0.2);
                    padding: 5px 12px;
                    border-radius: 20px;
                    font-size: 0.9rem;
                    color: #A7F3D0;
                    border: 1px solid #10B981;
                ">质量风险管理</span>
                <span style="
                    background: rgba(245, 158, 11, 0.2);
                    padding: 5px 12px;
                    border-radius: 20px;
                    font-size: 0.9rem;
                    color: #FDE68A;
                    border: 1px solid #F59E0B;
                ">工艺验证</span>
                <span style="
                    background: rgba(239, 68, 68, 0.2);
                    padding: 5px 12px;
                    border-radius: 20px;
                    font-size: 0.9rem;
                    color: #FCA5A5;
                    border: 1px solid #EF4444;
                ">批记录管理</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_kpi_dashboard(metrics: Dict[str, Any]):
        """创建KPI仪表板"""
        if not metrics:
            return
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="kpi-card" style="text-align: center; padding: 15px; border-radius: 8px; 
                     background: linear-gradient(135deg, #1F2937 0%, #374151 100%); 
                     border: 1px solid #4B5563;">
                <div style="font-size: 1.8rem; font-weight: bold; color: #3B82F6; margin: 10px 0;">
                    {metrics.get('total_steps', 0)}
                </div>
                <div style="color: #9CA3AF; font-size: 0.9rem;">
                    工艺步骤数
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="kpi-card" style="text-align: center; padding: 15px; border-radius: 8px;
                     background: linear-gradient(135deg, #1F2937 0%, #374151 100%); 
                     border: 1px solid #4B5563;">
                <div style="font-size: 1.8rem; font-weight: bold; color: #10B981; margin: 10px 0;">
                    {metrics.get('total_parameters', 0)}
                </div>
                <div style="color: #9CA3AF; font-size: 0.9rem;">
                    关键参数
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="kpi-card" style="text-align: center; padding: 15px; border-radius: 8px;
                     background: linear-gradient(135deg, #1F2937 0%, #374151 100%); 
                     border: 1px solid #4B5563;">
                <div style="font-size: 1.8rem; font-weight: bold; color: #F59E0B; margin: 10px 0;">
                    {metrics.get('unique_equipment', 0)}
                </div>
                <div style="color: #9CA3AF; font-size: 0.9rem;">
                    设备种类
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            complexity = metrics.get('complexity_score', 0)
            color = "#10B981" if complexity < 5 else "#F59E0B" if complexity < 8 else "#EF4444"
            st.markdown(f"""
            <div class="kpi-card" style="text-align: center; padding: 15px; border-radius: 8px;
                     background: linear-gradient(135deg, #1F2937 0%, #374151 100%); 
                     border: 1px solid #4B5563;">
                <div style="font-size: 1.8rem; font-weight: bold; color: {color}; margin: 10px 0;">
                    {complexity}
                </div>
                <div style="color: #9CA3AF; font-size: 0.9rem;">
                    复杂度评分
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def create_sidebar():
        """创建专业侧边栏"""
        with st.sidebar:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #1E293B 0%, #111827 100%);
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                border: 1px solid #374151;
            ">
                <h3 style="color: white; margin-bottom: 20px;">⚙️ MES系统配置</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # 模式选择
            mode = st.radio(
                "选择分析模式",
                ["单一产品分析", "多产品对比", "风险评估", "合规性检查", "批记录分析"],
                index=0,
                key="analysis_mode"
            )
            
            st.markdown("---")
            
            # 根据模式显示不同选项
            if mode == "单一产品分析":
                PharmaComponents._render_single_product_sidebar()
            elif mode == "多产品对比":
                PharmaComponents._render_multi_product_sidebar()
            elif mode == "风险评估":
                PharmaComponents._render_risk_assessment_sidebar()
            elif mode == "合规性检查":
                PharmaComponents._render_compliance_sidebar()
            else:  # 批记录分析
                PharmaComponents._render_batch_record_sidebar()
            
            st.markdown("---")
            
            # 系统配置
            with st.expander("⚡ 高级设置"):
                sampling_rate = st.slider("数据采样频率", 1, 60, 5, help="数据采集频率（分钟）")
                alert_threshold = st.slider("报警阈值", 1, 100, 80, help="参数偏离目标值的百分比")
                auto_save = st.checkbox("自动保存配置", value=True)
            
            return mode
    
    @staticmethod
    def _render_single_product_sidebar():
        """渲染单一产品分析的侧边栏内容"""
        st.markdown("#### 选择产品")
        
        # 导入数据库
        from database import PharmaceuticalProcesses
        
        categories = PharmaceuticalProcesses.get_main_categories()
        selected_category = st.selectbox(
            "选择药品分类",
            categories,
            index=0,
            key="product_category"
        )
        
        if selected_category:
            products = PharmaceuticalProcesses.get_products(selected_category)
            selected_product = st.selectbox(
                "选择具体产品",
                products,
                index=0,
                key="product_name"
            )
            
            if selected_product:
                product_info = PharmaceuticalProcesses.get_product_info(selected_category, selected_product)
                if product_info:
                    with st.expander("📋 产品信息"):
                        st.write(f"**描述**: {product_info.get('description', '')}")
                        st.write(f"**GMP分类**: {product_info.get('GMP分类', '未分类')}")
                        
                        features = product_info.get("关键特征", [])
                        if features:
                            st.write("**关键特征**:")
                            for feature in features:
                                st.write(f"• {feature}")
    
    @staticmethod
    def _render_multi_product_sidebar():
        """渲染多产品对比的侧边栏内容"""
        st.markdown("#### 选择对比产品")
        
        from database import PharmaceuticalProcesses
        
        # 获取所有产品
        all_products = []
        for category in PharmaceuticalProcesses.get_main_categories():
            products = PharmaceuticalProcesses.get_products(category)
            for product in products:
                all_products.append(f"{category} | {product}")
        
        # 多选
        selected_products = st.multiselect(
            "选择要对比的产品（最多5个）",
            all_products,
            default=all_products[:2] if len(all_products) >= 2 else all_products,
            key="compare_products"
        )
        
        # 对比维度选择
        st.markdown("#### 对比维度")
        compare_dimensions = st.multiselect(
            "选择对比指标",
            ["工艺步骤数", "关键参数数量", "设备复杂度", "时间效率", "风险等级", "合规性"],
            default=["工艺步骤数", "关键参数数量", "风险等级"],
            key="compare_dimensions"
        )
    
    @staticmethod
    def _render_risk_assessment_sidebar():
        """渲染风险评估的侧边栏内容"""
        st.markdown("#### 风险评估设置")
        
        risk_methodology = st.selectbox(
            "风险评估方法",
            ["ICH Q9", "FMEA", "HACCP", "自定义"],
            index=0,
            key="risk_method"
        )
        
        risk_tolerance = st.slider(
            "风险容忍度",
            1, 10, 6,
            help="风险容忍度等级（1=非常严格，10=相对宽松）",
            key="risk_tolerance"
        )
        
        if risk_methodology == "FMEA":
            st.checkbox("考虑严重度", value=True, key="consider_severity")
            st.checkbox("考虑发生度", value=True, key="consider_occurrence")
            st.checkbox("考虑探测度", value=True, key="consider_detection")
        
        st.markdown("---")
        st.markdown("#### 评估范围")
        include_steps = st.checkbox("包括工艺步骤风险", value=True)
        include_params = st.checkbox("包括参数控制风险", value=True)
        include_equipment = st.checkbox("包括设备风险", value=True)
    
    @staticmethod
    def _render_compliance_sidebar():
        """渲染合规性检查的侧边栏内容"""
        st.markdown("#### 合规标准")
        
        standards = st.multiselect(
            "选择合规标准",
            ["中国GMP", "FDA cGMP", "EU GMP", "ICH Q7", "ISO 9001", "ISO 13485"],
            default=["中国GMP", "FDA cGMP"],
            key="compliance_standards"
        )
        
        st.markdown("#### 检查项目")
        check_critical = st.checkbox("关键参数控制", value=True)
        check_documentation = st.checkbox("文件记录", value=True)
        check_validation = st.checkbox("工艺验证", value=True)
        check_training = st.checkbox("人员培训", value=True)
        check_equipment = st.checkbox("设备校准", value=True)
    
    @staticmethod
    def _render_batch_record_sidebar():
        """渲染批记录分析的侧边栏内容"""
        st.markdown("#### 批记录设置")
        
        batch_range = st.slider(
            "分析批次范围",
            1, 100, (1, 50),
            key="batch_range"
        )
        
        parameters = st.multiselect(
            "分析参数",
            ["温度", "压力", "pH", "含量", "纯度", "收率", "时间"],
            default=["温度", "pH", "含量"],
            key="batch_params"
        )
        
        analysis_type = st.radio(
            "分析类型",
            ["趋势分析", "稳定性分析", "相关性分析", "异常检测"],
            index=0,
            key="batch_analysis_type"
        )
    
    @staticmethod
    def create_process_step_card(step: Dict, step_number: int):
        """创建工艺步骤卡片"""
        step_name = step.get("name", "")
        critical_params = step.get("关键参数", [])
        equipment = step.get("设备", [])
        time_required = step.get("时间", "")
        
        # 判断是否为关键步骤
        is_critical = any(keyword in step_name for keyword in ["灭菌", "无菌", "病毒", "灌装"])
        border_color = "#EF4444" if is_critical else "#10B981"
        
        with st.expander(f"步骤 {step_number}: {step_name}", expanded=(step_number == 1)):
            # 步骤信息布局
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("**关键参数:**")
                for param in critical_params:
                    param_color = "#EF4444" if any(keyword in param for keyword in ["无菌", "病毒"]) else "#3B82F6"
                    st.markdown(f'<span style="color:{param_color}">• {param}</span>', unsafe_allow_html=True)
                
                st.markdown("**主要设备:**")
                for equip in equipment:
                    st.markdown(f"• {equip}")
            
            with col2:
                if time_required:
                    st.metric("工艺时间", time_required)
                
                if is_critical:
                    st.markdown(f"""
                    <div style="
                        background-color: rgba(239, 68, 68, 0.2);
                        color: #FCA5A5;
                        padding: 8px;
                        border-radius: 5px;
                        border-left: 4px solid #EF4444;
                        margin-top: 10px;
                    ">
                        <strong>⚠️ 关键步骤</strong>
                    </div>
                    """, unsafe_allow_html=True)
    
    @staticmethod
    def create_risk_indicator(risk_level: str, score: float):
        """创建风险指示器"""
        risk_colors = {
            "极高风险 (红色)": "#EF4444",
            "高风险 (橙色)": "#F97316",
            "中风险 (黄色)": "#F59E0B",
            "低风险 (蓝色)": "#3B82F6",
            "可接受风险 (绿色)": "#10B981"
        }
        
        color = risk_colors.get(risk_level, "#6B7280")
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1F2937 0%, #2D3748 100%);
            padding: 20px;
            border-radius: 10px;
            border-left: 6px solid {color};
            margin: 10px 0;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: white;">风险评估结果</h4>
                    <p style="margin: 5px 0 0 0; color: #9CA3AF;">当前工艺风险状态</p>
                </div>
                <div style="
                    background-color: {color}20;
                    color: {color};
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-weight: bold;
                    border: 1px solid {color};
                ">
                    {risk_level}
                </div>
            </div>
            <div style="margin-top: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="color: #D1D5DB;">风险评分</span>
                    <span style="color: white; font-weight: bold;">{score}/10</span>
                </div>
                <div style="
                    height: 8px;
                    background-color: #374151;
                    border-radius: 4px;
                    overflow: hidden;
                ">
                    <div style="
                        height: 100%;
                        width: {score*10}%;
                        background-color: {color};
                        border-radius: 4px;
                    "></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_compliance_status(status_data: Dict):
        """创建合规性状态卡片"""
        overall_status = status_data.get("overall_status", "未知")
        gmp_class = status_data.get("gmp_classification", "未分类")
        severity_counts = status_data.get("severity_counts", {})
        
        status_color = "#10B981" if overall_status == "合规" else "#F59E0B"
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1F2937 0%, #2D3748 100%);
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid {status_color};
                text-align: center;
            ">
                <div style="font-size: 1.5rem; font-weight: bold; color: {status_color}; margin: 5px 0;">
                    {overall_status}
                </div>
                <div style="color: #9CA3AF; font-size: 0.9rem;">
                    合规状态
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1F2937 0%, #2D3748 100%);
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #3B82F6;
                text-align: center;
            ">
                <div style="font-size: 1.5rem; font-weight: bold; color: #3B82F6; margin: 5px 0;">
                    {gmp_class}
                </div>
                <div style="color: #9CA3AF; font-size: 0.9rem;">
                    GMP分类
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            critical_count = severity_counts.get("严重", 0)
            critical_color = "#EF4444" if critical_count > 0 else "#10B981"
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1F2937 0%, #2D3748 100%);
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid {critical_color};
                text-align: center;
            ">
                <div style="font-size: 1.5rem; font-weight: bold; color: {critical_color}; margin: 5px 0;">
                    {critical_count}
                </div>
                <div style="color: #9CA3AF; font-size: 0.9rem;">
                    严重问题
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def create_footer():
        """创建专业页脚"""
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #111827 0%, #1E293B 100%);
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
            border-top: 1px solid #374151;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="color: white; margin: 0 0 10px 0;">🧬 制药工艺流程MES系统</h4>
                    <p style="color: #9CA3AF; margin: 0; font-size: 0.9rem;">
                        GMP合规 | 质量风险管理 | 工艺验证 | 批记录管理
                    </p>
                </div>
                <div style="text-align: right;">
                    <p style="color: #6B7280; margin: 0; font-size: 0.8rem;">
                        版本 3.0 | 专为制药行业MES设计
                    </p>
                    <p style="color: #6B7280; margin: 5px 0 0 0; font-size: 0.8rem;">
                        © 2024 制药工艺MES系统 - 数据来源：行业标准整理
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
