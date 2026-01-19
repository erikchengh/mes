    @staticmethod
    def create_comparison_bar_chart(products_data, width=400, height=400):
        """创建多产品对比柱状图"""
        if not products_data:
            return go.Figure()
        
        product_names = [data["name"] for data in products_data]
        step_counts = [len(data["steps"]) for data in products_data]
        
        fig = go.Figure(data=[
            go.Bar(
                x=product_names,
                y=step_counts,
                marker_color=MESVisualizations.PHARMA_COLORS["secondary_blue"],
                text=step_counts,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="工艺步骤数对比",
            xaxis_title="产品名称",
            yaxis_title="步骤数",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="white",
            height=height,
            width=width
        )
        
        return fig
