import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from model.data_processing_L import (
    load_data,
    preprocess_data,
    calculate_monthly_revenue,
    identify_peak_low_months,
    analyze_trend
)
from model.marketing_strategies_model import get_marketing_strategy, display_marketing_recommendations
from components.charts import plot_monthly_revenue, plot_monthly_revenue_matplotlib
from view.revenue_analysis_view import RevenueAnalysisView

class RevenueAnalysisController:
    """Controller cho chức năng phân tích doanh thu theo tháng"""
    
    def __init__(self):
        self.view = RevenueAnalysisView()
        self.uploaded_file = None
        self.data = None
        
    def run(self):
        """Chạy chức năng phân tích doanh thu"""
        self.view.render_header()
        
        uploaded_file = self.view.render_file_uploader()
        
        if uploaded_file is not None:
            self._process_uploaded_file(uploaded_file)
        else:
            self._handle_no_file_uploaded()
    
    def _process_uploaded_file(self, uploaded_file):
        """Xử lý file đã upload"""
        try:
            data = load_data(uploaded_file)
            data.columns = data.columns.str.strip()
            data = preprocess_data(data)

            product_list = sorted(data['Description'].dropna().unique())
            min_date = data['InvoiceDate'].min().date()
            max_date = data['InvoiceDate'].max().date()

            # Render controls
            product, start_date, end_date = self.view.render_controls(
                product_list, min_date, max_date
            )
            
            if product:
                self._analyze_product(data, product, start_date, end_date)
                
        except Exception as e:
            st.error(f"❌ Lỗi xử lý dữ liệu: {str(e)}")
    
    def _analyze_product(self, data, product, start_date, end_date):
        """Phân tích sản phẩm được chọn"""
        df = data[
            (data['Description'] == product) &
            (data['InvoiceDate'].dt.date >= start_date) &
            (data['InvoiceDate'].dt.date <= end_date)
        ]
        
        if df.empty:
            st.warning("⚠️ Không có dữ liệu cho lựa chọn này.")
            return
            
        monthly_revenue = calculate_monthly_revenue(df)
        if monthly_revenue.empty:
            st.warning("⚠️ Không có dữ liệu doanh thu theo tháng.")
            return
            
        self._display_analysis_results(monthly_revenue)
    
    def _display_analysis_results(self, monthly_revenue):
        """Hiển thị kết quả phân tích"""
        peak_month, low_month = identify_peak_low_months(monthly_revenue)

        # Hiển thị biểu đồ
        st.subheader("📈 Biểu Đồ Doanh Thu Theo Tháng")
        plot_monthly_revenue(monthly_revenue)

        # Tính toán các tháng đặc biệt
        revenues = monthly_revenue['Revenue'].tolist()
        months = monthly_revenue['Month'].astype(int).tolist()
        
        # Tháng biến động mạnh
        max_pct = 0
        max_idx = None
        for i in range(1, len(revenues)):
            if revenues[i-1] == 0:
                continue
            diff = revenues[i] - revenues[i-1]
            pct = abs(diff) / revenues[i-1]
            if pct > max_pct:
                max_pct = pct
                max_idx = i
        
        max_var_month = months[max_idx] if max_idx is not None and max_pct > 0.3 else None

        # Tháng ổn định
        avg = monthly_revenue['Revenue'].mean()
        lower = avg * 0.85
        upper = avg * 1.15
        stable_months = monthly_revenue[
            (monthly_revenue['Revenue'] >= lower) & (monthly_revenue['Revenue'] <= upper)
        ]['Month'].astype(int).tolist()

        # Hiển thị các tháng đặc biệt
        self.view.render_special_months(
            peak_month, low_month, max_var_month, stable_months
        )

        # Hiển thị phân tích xu hướng
        st.subheader("📉 Phân tích xu hướng")
        trend_analysis = analyze_trend(monthly_revenue)
        for paragraph in trend_analysis:
            st.write(paragraph)

        # Hiển thị gợi ý chiến lược marketing
        st.subheader("💡 Gợi ý chiến lược marketing")
        recommendations = display_marketing_recommendations(
            peak_month, low_month, stable_months, max_var_month
        )
        for rec in recommendations:
            st.markdown(f"- {rec}")
    
    def _handle_no_file_uploaded(self):
        """Xử lý khi chưa có file upload"""
        st.info("👆 Vui lòng chọn file CSV để bắt đầu phân tích doanh thu!")
        
        sample_data_path = 'data/online_retail.csv'
        if os.path.exists(sample_data_path):
            st.info("💡 Hoặc sử dụng dữ liệu mẫu có sẵn")
            if st.button("📂 Tải dữ liệu mẫu"):
                st.session_state['use_sample_data'] = True
                st.rerun()
        
        if st.session_state.get('use_sample_data', False):
            try:
                data = load_data(sample_data_path)
                st.success("✅ Đã tải dữ liệu mẫu thành công!")
                st.session_state['sample_data'] = data
                st.rerun()
            except Exception as e:
                st.error(f"❌ Không thể tải dữ liệu mẫu: {str(e)}") 