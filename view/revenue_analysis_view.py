import streamlit as st
from model.marketing_strategies_model import get_marketing_strategy

class RevenueAnalysisView:
    """View cho chức năng phân tích doanh thu theo tháng"""
    
    def render_header(self):
        """Render header của trang"""
        st.title("📊 Phân Tích Doanh Thu Theo Tháng")
    
    def render_file_uploader(self):
        """Render file uploader"""
        return st.file_uploader("📁 Chọn file CSV để phân tích", type=['csv'])
    
    def render_controls(self, product_list, min_date, max_date):
        """Render các controls để chọn sản phẩm và thời gian"""
        product = st.selectbox(
            "🛒 Chọn sản phẩm",
            product_list,
            index=None,
            placeholder="Nhập tên sản phẩm để tìm kiếm..."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "📅 Tháng bắt đầu phân tích", 
                min_value=min_date, 
                max_value=max_date, 
                value=min_date
            )
        with col2:
            end_date = st.date_input(
                "📅 Tháng kết thúc phân tích", 
                min_value=min_date, 
                max_value=max_date, 
                value=max_date
            )
        
        return product, start_date, end_date
    
    def render_special_months(self, peak_month, low_month, max_var_month, stable_months):
        """Render các tháng đặc biệt với buttons"""
        st.subheader("🌟 Các tháng đặc biệt")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button(f"🔥 Tháng cao điểm: {int(peak_month['Month'])}", key="peak"):
                st.info(get_marketing_strategy("peak", int(peak_month['Month'])))

        with col2:
            if st.button(f"❄️ Tháng thấp điểm: {int(low_month['Month'])}", key="low"):
                st.info(get_marketing_strategy("low", int(low_month['Month'])))

        with col3:
            if max_var_month is not None:
                if st.button(f"⚡ Biến động mạnh: {max_var_month}", key="strong_var"):
                    st.info(get_marketing_strategy("volatile", max_var_month))
            else:
                st.write("Không có tháng biến động mạnh.")

        with col4:
            if stable_months:
                for sm in stable_months:
                    if st.button(f"✅ Ổn định: {sm}", key=f"stable_{sm}"):
                        st.info(get_marketing_strategy("stable", sm))
            else:
                st.write("Không có tháng ổn định.")
    
    def render_trend_analysis(self, trend_analysis):
        """Render phân tích xu hướng"""
        st.subheader("📉 Phân tích xu hướng")
        for paragraph in trend_analysis:
            st.write(paragraph)
    
    def render_marketing_recommendations(self, recommendations):
        """Render gợi ý chiến lược marketing"""
        st.subheader("💡 Gợi ý chiến lược marketing")
        for rec in recommendations:
            st.markdown(f"- {rec}")
    
    def render_error_message(self, message):
        """Render error message"""
        st.error(f"❌ {message}")
    
    def render_warning_message(self, message):
        """Render warning message"""
        st.warning(f"⚠️ {message}")
    
    def render_success_message(self, message):
        """Render success message"""
        st.success(f"✅ {message}")
    
    def render_info_message(self, message):
        """Render info message"""
        st.info(f"💡 {message}") 