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
        data_path = st.session_state.get('uploaded_data_path', None)
        if data_path is not None and os.path.exists(data_path):
            self._process_uploaded_file(data_path)
        else:
            st.warning("⚠️ Vui lòng upload file dữ liệu ở dashboard để sử dụng các chức năng phân tích!")
    
    def _process_uploaded_file(self, file_path):
        """Xử lý file đã upload (file_path)"""
        try:
            data = load_data(file_path)
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

        # Hiển thị các tháng đặc biệt (chỉ nút và giải thích ngắn)
        self.view.render_special_months(
            peak_month, low_month, max_var_month, stable_months
        )

        # Hiển thị phân tích xu hướng
        trend_analysis = analyze_trend(monthly_revenue)
        self.view.render_trend_analysis(trend_analysis)

        # Hiển thị gợi ý chiến lược marketing (nội dung chi tiết)
        recommendations = display_marketing_recommendations(
            peak_month, low_month, stable_months, max_var_month
        )
        self.view.render_marketing_recommendations(recommendations)
    
    def _handle_no_file_uploaded(self):
        """Không còn dùng nữa vì đã gom upload về dashboard"""
        pass 