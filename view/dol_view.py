import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from typing import Any, Dict, List

class DolView:
    """View for DOL (Degree of Operating Leverage) analysis interface"""
    
    def render_header(self):
        """Render main header"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                    padding: 2rem; border-radius: 15px; margin-bottom: 2rem; color: white; text-align: center;">
            <h2>🔢 Phân tích DOL - Degree of Operating Leverage</h2>
            <p>Dự đoán và phân tích độ nhạy cảm hoạt động của doanh nghiệp</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_navigation(self, current_page: str, has_results: bool) -> str:
        """Render navigation sidebar"""
        page = st.sidebar.selectbox(
            "Chọn trang",
            ["input", "results"],
            index=0 if current_page == "input" else 1,
            format_func=lambda x: "Nhập liệu" if x == "input" else "Kết quả",
            disabled=not has_results if current_page == "input" else False
        )
        return page
    
    def render_input_header(self):
        """Render input page header"""
        st.header("Nhập thông tin để tính DOL")
    
    def render_input_form(self, available_products: List[str], available_years: List[int]) -> Dict[str, Any]:
        """Render input form and return collected data"""
        # Create three columns for better layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Thông tin chi phí")
            
            # Variable Cost Input
            variable_cost = st.number_input(
                "Chi phí biến đổi($):",
                min_value=0.0,
                value=10.0,
                step=0.1,
                help="Chi phí biến đổi trên mỗi đơn vị sản phẩm"
            )
            
            # Fixed Cost Input
            fixed_cost = st.number_input(
                "Chi phí cố định($):",
                min_value=0.0,
                value=1000.0,
                step=10.0,
                help="Chi phí cố định tổng thể"
            )
        
        with col2:
            st.subheader("Thông tin thời gian")
            
            # Time Period Selection
            time_period = st.selectbox(
                "Khoảng thời gian:",
                ["1 tháng tới", "2 tháng tới", "3 tháng tới"],
                index=0
            )
            
            # Year Selection for Monthly Analysis
            if available_years:
                selected_year = st.selectbox(
                    "Năm phân tích theo tháng:",
                    available_years,
                    index=len(available_years)-1,
                    help="Chọn năm để xem phân tích DOL theo từng tháng"
                )
            else:
                selected_year = None
                st.warning("Không có dữ liệu theo năm")
        
        with col3:
            st.subheader("Chọn sản phẩm")
            
            # Product Search
            search_term = st.text_input(
                "Tìm kiếm sản phẩm:",
                placeholder="Nhập mã sản phẩm...",
                help="Tìm kiếm theo mã sản phẩm"
            )
            
            # Filter products based on search term
            if search_term:
                filtered_products = [p for p in available_products if search_term.lower() in str(p).lower()]
            else:
                filtered_products = available_products[:100]  # Limit for performance
            
            # Product Selection
            if filtered_products:
                product_code = st.selectbox(
                    "Chọn mã sản phẩm:",
                    filtered_products,
                    index=0
                )
            else:
                if search_term:
                    st.warning("Không tìm thấy sản phẩm nào phù hợp.")
                else:
                    st.warning("Không có sản phẩm nào.")
                product_code = None
        
        return {
            'variable_cost': variable_cost,
            'fixed_cost': fixed_cost,
            'time_period': time_period,
            'selected_year': selected_year,
            'product_code': product_code
        }
    
    def render_calculate_button(self) -> bool:
        """Render calculate button and return if clicked"""
        return st.button("Tính DOL", type="primary", use_container_width=True)
    
    def render_results_header(self):
        """Render results page header"""
        st.header("Kết quả phân tích DOL")
    
    def render_summary_table(self, results: Dict[str, Any], model: Any):
        """Render summary table with DOL forecasts"""
        st.subheader("📋 Bảng tóm tắt DOL")
        
        time_period = results.get('time_period', '1 tháng tới')
        base_dol = results.get('dol', 0)
        product_code = results.get('product_code', '')
        variable_cost = results.get('variable_cost', 0)
        fixed_cost = results.get('fixed_cost', 0)
        selected_year = results.get('selected_year', 2011)
        
        # Get monthly DOL data for reference
        monthly_dol_data = model.get_monthly_dol_data(product_code, variable_cost, fixed_cost, selected_year)
        
        # Display reference information
        if monthly_dol_data:
            available_months = sorted(monthly_dol_data.keys())
            if available_months:
                most_recent_month = available_months[-1]
                most_recent_dol = monthly_dol_data[most_recent_month]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(f"📅 **Tháng gần nhất có dữ liệu:** {most_recent_month}")
                with col2:
                    st.info(f"📊 **DOL tháng {most_recent_month}:** {most_recent_dol:.3f}")
                with col3:
                    st.info(f"📈 **Năm phân tích:** {selected_year}")
        
        # Determine number of months to show
        months_to_show = 1
        if '3' in time_period:
            months_to_show = 3
        elif '2' in time_period:
            months_to_show = 2
        
        # Create table data
        table_data = []
        for month in range(1, months_to_show + 1):
            time_text = f"{month} tháng tới"
            dol_value = base_dol * (1 + (month - 1) * 0.1)
            sensitivity = self._get_sensitivity_level(dol_value)
            comparison = self._get_comparison_text(month, dol_value, model, product_code, variable_cost, fixed_cost, selected_year)
            
            # Get strategic focus based on DOL
            if dol_value > 0.5:
                analysis = "Tăng trưởng mạnh - Mở rộng thị phần, quảng cáo tích cực"
            elif dol_value == 0.5:
                analysis = "Cân bằng - Kết hợp giữ chân KH cũ và mở rộng mới"
            else:
                analysis = "Bền vững - Marketing tiết kiệm, tập trung giá trị cốt lõi"
            
            table_data.append({
                "Thời gian": time_text,
                "DOL": f"{dol_value:.2f}",
                "Độ nhạy cảm": sensitivity,
                "So với tháng gần nhất": comparison,
                "Định hướng chiến lược": analysis
            })
        
        # Display table
        df_table = pd.DataFrame(table_data)
        st.dataframe(df_table, use_container_width=True)
    
    def render_dol_chart(self, results: Dict[str, Any]):
        """Render DOL chart showing monthly data"""
        st.subheader("📈 Biểu đồ DOL theo từng tháng")
        
        try:
            monthly_dol_data = results.get('monthly_dol_data', {})
            product_code = results.get('product_code', '')
            selected_year = results.get('selected_year', 'N/A')
            
            if not monthly_dol_data:
                st.warning("Không có dữ liệu DOL theo tháng để hiển thị.")
                st.info("💡 Lưu ý: Dữ liệu có thể không có đủ thông tin theo tháng hoặc sản phẩm không có hoạt động trong năm được chọn.")
                return
            
            # Create the chart
            months = list(monthly_dol_data.keys())
            dol_values = list(monthly_dol_data.values())
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=months,
                y=dol_values,
                mode='lines+markers',
                name='DOL',
                line=dict(color='blue', width=3),
                marker=dict(size=8, color='blue')
            ))
            
            fig.update_layout(
                title=f'DOL theo từng tháng năm {selected_year} - Sản phẩm: {product_code}',
                xaxis_title='Tháng',
                yaxis_title='DOL',
                xaxis=dict(tickmode='array', tickvals=list(range(1, 13)), ticktext=[
                    'T1', 'T2', 'T3', 'T4', 'T5', 'T6',
                    'T7', 'T8', 'T9', 'T10', 'T11', 'T12'
                ]),
                height=500,
                showlegend=False
            )
            
            # Add horizontal lines for sensitivity levels
            fig.add_hline(y=0.5, line_dash="dash", line_color="orange", 
                        annotation_text="Ngưỡng trung bình (0.5)")
            fig.add_hline(y=0.3, line_dash="dash", line_color="green", 
                        annotation_text="Ngưỡng thấp (< 0.5)")
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show summary statistics
            if dol_values:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("DOL trung bình", f"{np.mean(dol_values):.2f}")
                with col2:
                    st.metric("DOL cao nhất", f"{max(dol_values):.2f}")
                with col3:
                    st.metric("DOL thấp nhất", f"{min(dol_values):.2f}")
                
                st.info(f"📊 Dữ liệu hiển thị cho năm {selected_year} - {len(months)} tháng có dữ liệu")
            
        except Exception as e:
            st.error(f"Lỗi khi tạo biểu đồ: {str(e)}")
    
    def render_detailed_analysis(self, results: Dict[str, Any], model: Any):
        """Render detailed analysis sections"""
        st.subheader("🔍 Phân tích chi tiết")
        
        time_period = results.get('time_period', '1 tháng tới')
        base_dol = results.get('dol', 0)
        product_code = results.get('product_code', '')
        variable_cost = results.get('variable_cost', 0)
        fixed_cost = results.get('fixed_cost', 0)
        selected_year = results.get('selected_year', 2011)
        
        # Determine number of months to analyze
        months_to_analyze = 1
        if '3' in time_period:
            months_to_analyze = 3
        elif '2' in time_period:
            months_to_analyze = 2
        
        for month in range(1, months_to_analyze + 1):
            with st.expander(f"Phân tích tháng {month}", expanded=(month == 1)):
                dol_value = base_dol * (1 + (month - 1) * 0.1)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Thông tin DOL:**")
                    st.write(f"- Giá trị DOL: {dol_value:.2f}")
                    st.write(f"- Độ nhạy cảm: {self._get_sensitivity_level(dol_value)}")
                    st.write(f"- So với tháng gần nhất: {self._get_comparison_text(month, dol_value, model, product_code, variable_cost, fixed_cost, selected_year)}")
                
                with col2:
                    st.markdown("**Khuyến nghị chiến lược:**")
                    strategies = self._get_strategies_text(dol_value)
                    st.write(strategies)
                
                st.markdown("**Ghi chú:**")
                st.write(self._get_note_text(dol_value))
    
    def _get_sensitivity_level(self, dol_value: float) -> str:
        """Determine sensitivity level based on DOL value"""
        if dol_value > 0.5:
            return "Cao"
        elif dol_value == 0.5:
            return "Trung bình"
        else:
            return "Thấp"
    
    def _get_comparison_text(self, month: int, dol_value: float, model: Any, product_code: str, variable_cost: float, fixed_cost: float, selected_year: int) -> str:
        """Get comparison text by comparing with actual DOL from previous month"""
        try:
            monthly_dol_data = model.get_monthly_dol_data(product_code, variable_cost, fixed_cost, selected_year)
            
            if not monthly_dol_data:
                return "Không đổi"
            
            available_months = sorted(monthly_dol_data.keys())
            if len(available_months) < 2:
                return "Không đổi"
            
            previous_month = available_months[-2]
            actual_previous_dol = monthly_dol_data[previous_month]
            
            if dol_value > actual_previous_dol * 1.1:
                return "Cao hơn"
            elif dol_value < actual_previous_dol * 0.9:
                return "Thấp hơn"
            else:
                return "Không đổi"
                
        except Exception:
            if dol_value > 0.5:
                return "Cao hơn"
            elif dol_value < 0.5:
                return "Thấp hơn"
            else:
                return "Không đổi"
    
    def _get_strategies_text(self, dol_value: float) -> str:
        """Get strategic recommendations based on DOL"""
        if dol_value > 0.5:
            return """**DOL Cao (> 0.5):**

• Tăng tốc độ mở rộng thị phần
• Đầu tư mạnh vào quảng cáo (Facebook Ads, Google, Influencer)
• Tạo sự khác biệt sản phẩm
• Hỗ trợ hậu mãi tốt để giữ chân khách hàng"""
        elif dol_value == 0.5:
            return """**DOL Trung bình (= 0.5):**

• Kết hợp giữa giữ chân khách hàng cũ và mở rộng mới
• Chạy các chiến dịch khuyến mãi nhẹ theo mùa
• Tập trung trải nghiệm người dùng và sự hài lòng
• Tăng phân tích hành vi khách hàng"""
        else:
            return """**DOL Thấp (< 0.5):**

• Marketing tiết kiệm, dựa trên truyền miệng, cộng đồng, TikTok, Zalo, fanpage
• Chăm sóc khách hàng, tạo lòng trung thành
• Tập trung vào giá trị truyền thống, nguồn gốc nguyên liệu, câu chuyện sản phẩm"""
    
    def _get_note_text(self, dol_value: float) -> str:
        """Get additional notes"""
        if dol_value > 0.5:
            return "DOL cao cho thấy doanh nghiệp rất nhạy cảm với thay đổi doanh số. Cần thận trọng trong quản lý rủi ro và tập trung vào chiến lược tăng trưởng mạnh mẽ."
        elif dol_value == 0.5:
            return "DOL ở mức trung bình, phù hợp cho hoạt động kinh doanh ổn định với chiến lược cân bằng giữa tăng trưởng và ổn định."
        else:
            return "DOL thấp cho thấy doanh nghiệp ít nhạy cảm với thay đổi doanh số, phù hợp với chiến lược bền vững và tập trung vào giá trị cốt lõi." 