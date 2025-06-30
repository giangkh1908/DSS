import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import time
from model.data_processing_L import load_and_clean_data, load_and_clean_data_from_upload, filter_data, calculate_total_revenue, calculate_percentage_change, compare_total_revenue, analyze_seasonality, analyze_country_performance
from model.analysis_L import *
from view.plots_L import plot_results, plot_revenue_comparison_ratios

def main():
    st.title("📈 Phân tích Doanh thu các Quốc gia theo thời gian")
    data_path = st.session_state.get('uploaded_data_path', None)
    if data_path is None or not os.path.exists(data_path):
        st.warning("⚠️ Vui lòng upload file dữ liệu ở dashboard để sử dụng các chức năng phân tích!")
        st.markdown("""
        ### 📋 Định dạng dữ liệu yêu cầu:
        File cần có các cột:
        - **InvoiceDate**: Ngày bán hàng
        - **Country**: Quốc gia
        - **Revenue**: Doanh thu (hoặc Quantity + UnitPrice)
        """)
        return
    try:
        with st.spinner("Đang load và làm sạch dữ liệu..."):
            if data_path.endswith('.csv'):
                df = load_and_clean_data_from_upload(open(data_path, 'rb'), 'csv')
            else:
                df = load_and_clean_data_from_upload(open(data_path, 'rb'), 'excel')
    except Exception as e:
        st.error(f"❌ Lỗi khi đọc file: {str(e)}")
        return
    st.sidebar.header("Cài đặt Phân tích")
    min_date = df['InvoiceDate'].min()
    max_date = df['InvoiceDate'].max()
    start_date = st.sidebar.date_input("Chọn ngày bắt đầu", min_date, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("Chọn ngày kết thúc", max_date, min_value=min_date, max_value=max_date)
    countries = df['Country'].unique().tolist()
    selected_countries = st.sidebar.multiselect("Chọn quốc gia (bỏ trống để chọn tất cả)", countries, default=countries[:1])
    analysis_type = st.sidebar.selectbox(
        "Chọn loại phân tích",
        ['Tổng doanh thu', 'Tốc độ tăng trưởng', 'So sánh doanh thu'],
        index=0
    )
    revenue_threshold = st.sidebar.number_input("Ngưỡng doanh thu (£)", min_value=0.0, value=0.0, step=1000.0)
    with st.spinner("Đang lọc dữ liệu..."):
        df_filtered = filter_data(df, start_date, end_date, selected_countries, revenue_threshold)
    if df_filtered.empty:
        st.warning("Không có dữ liệu phù hợp với các tiêu chí đã chọn.")
        return
    with st.spinner("Đang tính toán kết quả..."):
        pivot_table = calculate_total_revenue(df_filtered)
        growth_rate = calculate_percentage_change(pivot_table)
        total_revenue = compare_total_revenue(pivot_table)
        monthly_revenue, peak_months, quarterly_proportion = analyze_seasonality(df_filtered)
        country_metrics = analyze_country_performance(df_filtered)
    st.header("Kết quả Phân tích")
    if analysis_type == 'Tổng doanh thu':
        st.subheader("Tổng Doanh thu Theo Thời gian")
        st.write(pivot_table)
        plot_results(pivot_table, None, None, None, None, None, ['Tổng doanh thu'])
        st.write(comment_total_revenue(pivot_table))
        st.info(recommend_total_revenue(pivot_table))
        st.markdown("---")
        with st.expander(":moneybag: GỢI Ý ĐẦU TƯ", expanded=False):
            country, benefit, total_revenue, stability = suggest_investment_total_revenue(pivot_table, country_metrics)
            st.write(benefit)
            st.write("**HÀNH ĐỘNG ĐỀ XUẤT:**")
            for act in action_suggestions_total_revenue():
                st.write(f"  - {act}")
        # st.markdown("---")
        with st.expander(":chart_with_upwards_trend: DỰ BÁO", expanded=False):
            base_forecast, enhanced_forecast, explanation, top_country, monthly_revenue = estimate_profit_increase_total_revenue_one_year(pivot_table, country_metrics)
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="Giữ nguyên ngân sách",
                    value=f"{base_forecast:.2f}%",
                    delta=f"{base_forecast:.2f}% tăng trưởng"
                )
            with col2:
                st.metric(
                    label="Tăng ngân sách 20%",
                    value=f"{enhanced_forecast:.2f}%",
                    delta=f"{enhanced_forecast - base_forecast:.2f}% so với giữ nguyên"
                )
            st.write(explanation)
    elif analysis_type == 'Tốc độ tăng trưởng':
        st.subheader("Tốc độ Tăng trưởng Doanh thu (%)")
        st.write(growth_rate)
        plot_results(None, growth_rate, None, None, None, None, ['Tốc độ tăng trưởng'])
        st.write(comment_growth_rate(growth_rate))
        st.info(recommend_growth_rate(growth_rate))
        st.markdown("---")
        with st.expander(":moneybag: GỢI Ý ĐẦU TƯ", expanded=False):
            country, benefit, growth, stability = suggest_investment_growth_rate(growth_rate, country_metrics)
            st.write(benefit)
            st.write("**HÀNH ĐỘNG ĐỀ XUẤT:**")
            for act in action_suggestions_growth_rate():
                st.write(f"  - {act}")
        # st.markdown("---")
        with st.expander(":chart_with_upwards_trend: DỰ BÁO", expanded=False):
            trend, base_forecast, enhanced_forecast, explanation, top_country = estimate_growth_trend_growth_rate_one_year(growth_rate, country_metrics)
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="Giữ nguyên tình trạng hiện tại",
                    value=f"{base_forecast:.2f}%",
                    delta=f"{base_forecast - growth_rate[top_country].iloc[-1]:+.2f}% so với hiện tại"
                )
            with col2:
                st.metric(
                    label="Tăng cường đầu tư 20%",
                    value=f"{enhanced_forecast:.2f}%",
                    delta=f"{enhanced_forecast - base_forecast:+.2f}% so với giữ nguyên"
                )
            st.write(f"**Xu hướng tổng thể: {trend}**")
            st.write(explanation)
    elif analysis_type == 'So sánh doanh thu':
        st.subheader("So sánh Tổng Doanh thu")
        st.write(total_revenue)
        plot_results(None, None, total_revenue, country_metrics, monthly_revenue, quarterly_proportion, ['So sánh doanh thu'])
        st.subheader("📊 Phân tích Tỷ lệ Doanh thu")
        plot_revenue_comparison_ratios(total_revenue)
        st.write(comment_compare_revenue(total_revenue))
        st.info(recommend_compare_revenue(total_revenue))
        st.markdown("---")
        with st.expander(":moneybag: GỢI Ý TĂNG CƯỜNG ĐẦU TƯ", expanded=False):
            country, benefit, revenue, stability = suggest_investment_compare_revenue(total_revenue, country_metrics)
            st.write(benefit)
            st.write("**HÀNH ĐỘNG ĐỀ XUẤT:**")
            for act in action_suggestions_compare_revenue():
                st.write(f"  - {act}")

if __name__ == "__main__":
    main() 