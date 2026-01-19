"""
制药工艺流程MES系统 - 主应用程序
专为制药行业MES专业人员设计
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 导入自定义模块
from database import PharmaceuticalProcesses
from analytics import MESAnalyzer
from visualizations import MESVisualizations
from components import PharmaComponents
from mes_features import MESFeatures

# 页面配置
st.set_page_config(
    page_title="制药工艺流程MES系统",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用自定义CSS
st.markdown("""
<style>
    /* 全局样式 */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    }
    
    /* 主要容器 */
    .main .block-container {
        padding-top: 2rem;
    }
    
    /* 标题样式 */
    h1, h2, h3 {
        color: white !important;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    }
    
    /* 卡片样式 */
    .card {
        background: linear-gradient(135deg, #1F2937 0%, #2D3748 100%);
        border: 1px solid #374151;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* 表格样式 */
    .dataframe {
        background-color: #1F2937 !important;
        color: white !important;
    }
    
    .dataframe th {
        background-color: #374151 !important;
        color: white !important;
    }
    
    .dataframe td {
        background-color: #1F2937 !important;
        color: #D1D5DB !important;
        border-color: #374151 !important;
    }
    
    /* 侧边栏 */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #1E3A8A, #3B82F6);
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3B82F6, #2563EB);
        transform: translateY(-2px);
    }
    
    /* 选项卡样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #1F2937;
        padding: 4px;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #374151;
        border-radius: 6px;
        padding: 8px 16px;
        border: 1px solid #4B5563;
        color: #9CA3AF;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1E3A8A, #3B82F6);
        color: white !important;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

def main():
    """主函数"""
    # 创建页眉
    PharmaComponents.create_header()
    
    # 创建侧边栏并获取模式
    mode = PharmaComponents.create_sidebar()
    
    # 根据模式显示内容
    if mode == "单一产品分析":
        display_single_product_analysis()
    elif mode == "多产品对比":
        display_multi_product_comparison()
    elif mode == "风险评估":
        display_risk_assessment()
    elif mode == "合规性检查":
        display_compliance_check()
    elif mode == "批记录分析":
        display_batch_record_analysis()
    
    # 创建页脚
    PharmaComponents.create_footer()

def display_single_product_analysis():
    """显示单一产品分析"""
    st.markdown("## 🔬 单一产品工艺分析")
    
    # 获取侧边栏选择
    from database import PharmaceuticalProcesses
    
    categories = PharmaceuticalProcesses.get_main_categories()
    selected_category = st.session_state.get("product_category", categories[0] if categories else None)
    
    if selected_category:
        products = PharmaceuticalProcesses.get_products(selected_category)
        selected_product = st.session_state.get("product_name", products[0] if products else None)
        
        if selected_product:
            product_info = PharmaceuticalProcesses.get_product_info(selected_category, selected_product)
            
            if product_info:
                # 显示产品信息
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="card">
                        <h3 style="color: white; margin-bottom: 10px;">{selected_product}</h3>
                        <p style="color: #D1D5DB;">{product_info.get('description', '')}</p>
                        <div style="margin-top: 15px;">
                            <span style="
                                background-color: rgba(59, 130, 246, 0.2);
                                color: #93C5FD;
                                padding: 5px 12px;
                                border-radius: 20px;
                                margin-right: 10px;
                                border: 1px solid #3B82F6;
                            ">{selected_category}</span>
                            <span style="
                                background-color: rgba(16, 185, 129, 0.2);
                                color: #A7F3D0;
                                padding: 5px 12px;
                                border-radius: 20px;
                                border: 1px solid #10B981;
                            ">GMP分类: {product_info.get('GMP分类', '未分类')}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # 计算工艺指标
                    steps = product_info.get("工艺步骤", [])
                    metrics = MESAnalyzer.calculate_process_metrics(steps)
                    
                    st.markdown(f"""
                    <div class="card" style="text-align: center;">
                        <div style="font-size: 2rem; font-weight: bold; color: #3B82F6; margin: 10px 0;">
                            {len(steps)}
                        </div>
                        <div style="color: #9CA3AF; font-size: 0.9rem;">
                            工艺步骤
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 显示KPI仪表板
                PharmaComponents.create_kpi_dashboard(metrics)
                
                # 创建选项卡
                tab1, tab2, tab3, tab4 = st.tabs(["📋 工艺步骤", "🔧 风险分析", "📊 可视化", "📑 批记录模板"])
                
                with tab1:
                    display_process_steps(product_info)
                
                with tab2:
                    display_risk_analysis(product_info)
                
                with tab3:
                    display_visualizations(product_info)
                
                with tab4:
                    display_batch_template(product_info)

def display_process_steps(product_info):
    """显示工艺步骤"""
    steps = product_info.get("工艺步骤", [])
    
    if not steps:
        st.info("该产品暂无工艺步骤信息")
        return
    
    st.markdown("### 工艺步骤详情")
    
    for i, step in enumerate(steps, 1):
        PharmaComponents.create_process_step_card(step, i)

def display_risk_analysis(product_info):
    """显示风险分析"""
    steps = product_info.get("工艺步骤", [])
    
    if not steps:
        st.info("无法进行风险分析：缺少工艺步骤信息")
        return
    
    # 执行风险评估
    with st.spinner("正在进行风险评估..."):
        risk_data = MESAnalyzer.assess_process_risk(steps)
    
    # 显示风险指示器
    PharmaComponents.create_risk_indicator(
        risk_data.get("risk_level", "未知"),
        risk_data.get("average_risk_score", 0)
    )
    
    # 显示风险详情
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 关键步骤识别")
        critical_steps = risk_data.get("critical_steps", [])
        if critical_steps:
            for step in critical_steps[:5]:  # 只显示前5个
                st.info(f"**步骤{step['step_number']}: {step['step']}** - {step['risk_level']}步骤")
        else:
            st.success("未识别到关键步骤")
    
    with col2:
        st.markdown("#### 高风险因素")
        risk_factors = risk_data.get("high_risk_factors", [])
        if risk_factors:
            for factor in risk_factors[:3]:  # 只显示前3个
                st.warning(f"**{factor['step']}**: {', '.join(factor['factors'])}")
        else:
            st.success("未发现高风险因素")
    
    # 显示建议
    st.markdown("#### 风险控制建议")
    recommendations = risk_data.get("recommendations", [])
    for rec in recommendations:
        st.markdown(f"- {rec}")

def display_visualizations(product_info):
    """显示可视化图表"""
    steps = product_info.get("工艺步骤", [])
    product_name = st.session_state.get("product_name", "当前产品")
    
    if not steps:
        st.info("无法生成可视化：缺少工艺步骤信息")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 工艺流程图
        st.markdown("#### 工艺流程图")
        flow_chart = MESVisualizations.create_gmp_process_flow(steps, product_name, width=500, height=400)
        st.plotly_chart(flow_chart, use_container_width=True)
    
    with col2:
        # 风险评估图表
        st.markdown("#### 风险评估")
        risk_data = MESAnalyzer.assess_process_risk(steps)
        risk_chart = MESVisualizations.create_risk_assessment_chart(risk_data, width=400, height=400)
        st.plotly_chart(risk_chart, use_container_width=True)
    
    # 参数趋势图
    st.markdown("#### 参数趋势分析")
    param_chart = MESVisualizations.create_parameter_trend_chart({}, width=800, height=500)
    st.plotly_chart(param_chart, use_container_width=True)

def display_batch_template(product_info):
    """显示批记录模板"""
    st.markdown("### 批记录模板")
    
    # 生成批记录模板
    template = MESAnalyzer.generate_batch_record_template(product_info)
    
    # 显示批记录头信息
    with st.expander("批记录头信息", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.text_input("产品名称", value=st.session_state.get("product_name", ""))
            st.text_input("批号", value="")
            st.date_input("生产日期", value=datetime.now())
        
        with col2:
            st.date_input("有效期至", value=datetime.now() + pd.DateOffset(years=2))
            st.number_input("批量", value=100, min_value=1)
            st.text_input("生产线", value="Line-1")
        
        with col3:
            st.selectbox("班次", ["A", "B", "C"])
            st.text_input("操作员", value="")
            st.text_input("复核人", value="")
    
    # 显示步骤记录
    st.markdown("### 工艺步骤记录")
    steps = product_info.get("工艺步骤", [])
    
    for i, step in enumerate(steps, 1):
        with st.expander(f"步骤 {i}: {step.get('name', '')}", expanded=(i==1)):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**目标值**")
                for param in step.get("关键参数", [])[:3]:
                    st.text_input(f"{param} (目标)", value="", key=f"target_{i}_{param}")
            
            with col2:
                st.markdown("**实际值**")
                for param in step.get("关键参数", [])[:3]:
                    st.text_input(f"{param} (实际)", value="", key=f"actual_{i}_{param}")
            
            with col3:
                st.markdown("**检查项**")
                st.checkbox("参数符合要求", key=f"check_param_{i}")
                st.checkbox("设备运行正常", key=f"check_equip_{i}")
                st.text_area("备注", key=f"remark_{i}", height=80)
            
            st.markdown("---")
            col_sig1, col_sig2, col_sig3 = st.columns(3)
            with col_sig1:
                st.text_input("操作员签名", key=f"op_sign_{i}")
            with col_sig2:
                st.text_input("班组长签名", key=f"super_sign_{i}")
            with col_sig3:
                st.text_input("QA检查", key=f"qa_check_{i}")

def display_multi_product_comparison():
    """显示多产品对比"""
    st.markdown("## 📊 多产品工艺对比")
    
    # 获取选中的产品
    from database import PharmaceuticalProcesses
    
    selected_products = st.session_state.get("compare_products", [])
    
    if not selected_products:
        st.info("请在侧边栏选择要对比的产品")
        return
    
    # 限制最多5个产品
    selected_products = selected_products[:5]
    
    # 收集产品数据
    products_data = []
    for product_path in selected_products:
        if " | " in product_path:
            category, product_name = product_path.split(" | ")
            product_info = PharmaceuticalProcesses.get_product_info(category, product_name)
            if product_info:
                products_data.append({
                    "name": product_name,
                    "category": category,
                    "info": product_info,
                    "steps": product_info.get("工艺步骤", [])
                })
    
    if not products_data:
        st.error("未找到选中的产品信息")
        return
    
    # 显示对比摘要
    st.markdown("### 对比摘要")
    
    # 创建对比表格
    comparison_data = []
    for data in products_data:
        steps = data["steps"]
        metrics = MESAnalyzer.calculate_process_metrics(steps)
        risk_data = MESAnalyzer.assess_process_risk(steps)
        
        comparison_data.append({
            "产品名称": data["name"],
            "分类": data["category"],
            "工艺步骤数": len(steps),
            "关键参数数": metrics.get("total_parameters", 0),
            "设备种类数": metrics.get("unique_equipment", 0),
            "总时间(小时)": metrics.get("total_time_hours", 0),
            "复杂度评分": metrics.get("complexity_score", 0),
            "风险等级": risk_data.get("risk_level", "未知"),
            "GMP分类": data["info"].get("GMP分类", "未分类")
        })
    
    df_comparison = pd.DataFrame(comparison_data)
    
    # 显示对比表格
    st.dataframe(
        df_comparison,
        use_container_width=True,
        column_config={
            "产品名称": st.column_config.TextColumn("产品名称"),
            "分类": st.column_config.TextColumn("分类"),
            "工艺步骤数": st.column_config.NumberColumn("工艺步骤数"),
            "关键参数数": st.column_config.NumberColumn("关键参数数"),
            "设备种类数": st.column_config.NumberColumn("设备种类数"),
            "总时间(小时)": st.column_config.NumberColumn("总时间(小时)", format="%.1f"),
            "复杂度评分": st.column_config.NumberColumn("复杂度评分", format="%.2f"),
            "风险等级": st.column_config.TextColumn("风险等级"),
            "GMP分类": st.column_config.TextColumn("GMP分类")
        }
    )
    
    # 创建对比图表
    st.markdown("### 可视化对比")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 雷达图对比
        radar_chart = MESVisualizations.create_comparison_radar_chart(products_data, width=400, height=400)
        st.plotly_chart(radar_chart, use_container_width=True)
    
    with col2:
        # 柱状图对比
        fig = go.Figure()
        
        for i, data in enumerate(products_data):
            product_name = data["name"]
            steps = len(data["steps"])
            
            fig.add_trace(go.Bar(
                x=[product_name],
                y=[steps],
                name=product_name,
                marker_color=MESVisualizations.PHARMA_COLORS["secondary_blue"] if i % 2 == 0 
                             else MESVisualizations.PHARMA_COLORS["pharma_teal"]
            ))
        
        fig.update_layout(
            title="工艺步骤数对比",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="white",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 详细对比
    st.markdown("### 详细对比")
    tabs = st.tabs([data["name"] for data in products_data])
    
    for idx, tab in enumerate(tabs):
        with tab:
            data = products_data[idx]
            product_info = data["info"]
            
            # 显示产品信息
            st.markdown(f"**描述**: {product_info.get('description', '')}")
            st.markdown(f"**GMP分类**: {product_info.get('GMP分类', '未分类')}")
            
            # 显示关键特征
            features = product_info.get("关键特征", [])
            if features:
                st.markdown("**关键特征**:")
                for feature in features:
                    st.markdown(f"- {feature}")
            
            # 显示风险评估
            steps = data["steps"]
            risk_data = MESAnalyzer.assess_process_risk(steps)
            
            st.markdown("**风险评估**:")
            col_risk1, col_risk2 = st.columns(2)
            with col_risk1:
                st.metric("风险等级", risk_data.get("risk_level", "未知"))
            with col_risk2:
                st.metric("平均风险分", f"{risk_data.get('average_risk_score', 0):.2f}")

def display_risk_assessment():
    """显示风险评估"""
    st.markdown("## ⚠️ 工艺风险评估")
    
    # 获取风险评估设置
    risk_method = st.session_state.get("risk_method", "ICH Q9")
    risk_tolerance = st.session_state.get("risk_tolerance", 6)
    
    st.markdown(f"**评估方法**: {risk_method}")
    st.markdown(f"**风险容忍度**: {risk_tolerance}/10")
    
    # 选择要评估的产品
    from database import PharmaceuticalProcesses
    
    categories = PharmaceuticalProcesses.get_main_categories()
    selected_category = st.selectbox("选择药品分类", categories, key="risk_category")
    
    if selected_category:
        products = PharmaceuticalProcesses.get_products(selected_category)
        selected_product = st.selectbox("选择产品", products, key="risk_product")
        
        if selected_product:
            product_info = PharmaceuticalProcesses.get_product_info(selected_category, selected_product)
            
            if product_info:
                steps = product_info.get("工艺步骤", [])
                
                # 执行详细风险评估
                risk_data = MESAnalyzer.assess_process_risk(steps)
                
                # 显示风险评估结果
                PharmaComponents.create_risk_indicator(
                    risk_data.get("risk_level", "未知"),
                    risk_data.get("average_risk_score", 0)
                )
                
                # 显示风险矩阵
                st.markdown("### 风险矩阵")
                
                # 创建风险矩阵可视化
                fig = go.Figure()
                
                # 添加风险点
                critical_steps = risk_data.get("critical_steps", [])
                for step in critical_steps:
                    fig.add_trace(go.Scatter(
                        x=[step.get("risk_score", 0)],
                        y=[step.get("step_number", 0)],
                        mode="markers",
                        marker=dict(
                            size=20,
                            color="#EF4444",
                            symbol="diamond"
                        ),
                        name=step.get("step", "")
                    ))
                
                fig.update_layout(
                    title="风险矩阵分布",
                    xaxis_title="风险得分",
                    yaxis_title="步骤编号",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color="white",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 显示详细风险信息
                st.markdown("### 详细风险信息")
                
                high_risk_factors = risk_data.get("high_risk_factors", [])
                if high_risk_factors:
                    for factor in high_risk_factors:
                        with st.expander(f"高风险: {factor['step']}"):
                            st.markdown(f"**风险得分**: {factor['risk_score']:.2f}")
                            st.markdown("**风险因素**:")
                            for risk_factor in factor.get("factors", []):
                                st.markdown(f"- {risk_factor}")
                else:
                    st.success("未发现高风险因素")

def display_compliance_check():
    """显示合规性检查"""
    st.markdown("## ✅ GMP合规性检查")
    
    # 获取合规标准
    standards = st.session_state.get("compliance_standards", ["中国GMP", "FDA cGMP"])
    
    st.markdown("**检查标准**: " + ", ".join(standards))
    
    # 选择要检查的产品
    from database import PharmaceuticalProcesses
    
    categories = PharmaceuticalProcesses.get_main_categories()
    selected_category = st.selectbox("选择药品分类", categories, key="compliance_category")
    
    if selected_category:
        products = PharmaceuticalProcesses.get_products(selected_category)
        selected_product = st.selectbox("选择产品", products, key="compliance_product")
        
        if selected_product:
            product_info = PharmaceuticalProcesses.get_product_info(selected_category, selected_product)
            
            if product_info:
                # 执行合规性检查
                compliance_data = MESAnalyzer.check_gmp_compliance(product_info)
                
                # 显示合规状态
                PharmaComponents.create_compliance_status(compliance_data)
                
                # 显示检查项目
                st.markdown("### 检查项目详情")
                
                compliance_items = compliance_data.get("compliance_items", [])
                if compliance_items:
                    for item in compliance_items:
                        severity_color = "#EF4444" if item["severity"] == "严重" else "#F59E0B" if item["severity"] == "中等" else "#3B82F6"
                        
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #1F2937 0%, #2D3748 100%);
                            padding: 15px;
                            border-radius: 8px;
                            border-left: 4px solid {severity_color};
                            margin-bottom: 10px;
                        ">
                            <div style="display: flex; justify-content: space-between;">
                                <div>
                                    <strong style="color: white;">{item['step']}</strong>
                                    <p style="color: #D1D5DB; margin: 5px 0;">{item['issue']}</p>
                                </div>
                                <div style="
                                    background-color: {severity_color}20;
                                    color: {severity_color};
                                    padding: 5px 12px;
                                    border-radius: 20px;
                                    border: 1px solid {severity_color};
                                ">
                                    {item['severity']}
                                </div>
                            </div>
                            <div style="margin-top: 10px; color: #9CA3AF; font-size: 0.9rem;">
                                <strong>建议:</strong> {item['recommendation']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("所有检查项目均符合要求！")
                
                # 显示建议
                st.markdown("### 改进建议")
                recommendations = compliance_data.get("recommendations", [])
                if recommendations:
                    for rec in recommendations:
                        st.markdown(f"- {rec}")
                else:
                    st.info("无改进建议")

def display_batch_record_analysis():
    """显示批记录分析"""
    st.markdown("## 📈 批记录分析")
    
    # 获取分析设置
    batch_range = st.session_state.get("batch_range", (1, 50))
    parameters = st.session_state.get("batch_params", ["温度", "pH", "含量"])
    analysis_type = st.session_state.get("batch_analysis_type", "趋势分析")
    
    st.markdown(f"**分析批次**: {batch_range[0]} - {batch_range[1]}")
    st.markdown(f"**分析参数**: {', '.join(parameters)}")
    st.markdown(f"**分析类型**: {analysis_type}")
    
    # 选择产品
    from database import PharmaceuticalProcesses
    
    categories = PharmaceuticalProcesses.get_main_categories()
    selected_category = st.selectbox("选择药品分类", categories, key="batch_category")
    
    if selected_category:
        products = PharmaceuticalProcesses.get_products(selected_category)
        selected_product = st.selectbox("选择产品", products, key="batch_product")
        
        if selected_product:
            product_info = PharmaceuticalProcesses.get_product_info(selected_category, selected_product)
            
            if product_info:
                # 生成模拟批记录数据
                num_batches = batch_range[1] - batch_range[0] + 1
                batch_data = MESFeatures.generate_batch_records(product_info, num_batches)
                
                if not batch_data.empty:
                    # 显示批记录数据
                    with st.expander("查看批记录数据", expanded=False):
                        st.dataframe(batch_data, use_container_width=True)
                    
                    # 执行趋势分析
                    if analysis_type == "趋势分析":
                        st.markdown("### 趋势分析结果")
                        
                        # 显示趋势图表
                        trend_chart = MESVisualizations.create_parameter_trend_chart({}, width=800, height=500)
                        st.plotly_chart(trend_chart, use_container_width=True)
                        
                        # 显示统计分析
                        st.markdown("### 统计分析")
                        analysis_results = MESFeatures.analyze_batch_trends(batch_data, parameters)
                        
                        if analysis_results:
                            for param, stats in analysis_results.items():
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.metric(f"{param}均值", f"{stats['mean']:.2f}")
                                
                                with col2:
                                    st.metric(f"{param}标准差", f"{stats['std']:.3f}")
                                
                                with col3:
                                    st.metric(f"{param}趋势", stats['trend'])
                    
                    # 生成质量报告
                    st.markdown("### 质量报告")
                    quality_report = MESFeatures.generate_quality_report(batch_data)
                    
                    if quality_report:
                        summary = quality_report.get("summary", {})
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("总批次数", summary.get("total_batches", 0))
                        
                        with col2:
                            st.metric("合格批次", summary.get("passed_batches", 0))
                        
                        with col3:
                            st.metric("平均收率", f"{summary.get('yield_average', 0)}%")
                    
                    # 计算OEE
                    st.markdown("### 设备综合效率(OEE)")
                    oee_data = MESFeatures.calculate_oee(batch_data)
                    
                    if oee_data:
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("可用率", f"{oee_data['availability_percent']}%")
                        
                        with col2:
                            st.metric("性能率", f"{oee_data['performance_percent']}%")
                        
                        with col3:
                            st.metric("质量率", f"{oee_data['quality_percent']}%")
                        
                        with col4:
                            st.metric("OEE", f"{oee_data['oee_percent']}%")
                        
                        st.info(f"OEE等级: **{oee_data['oee_level']}**")

if __name__ == "__main__":
    main()
