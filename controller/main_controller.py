import streamlit as st
from model.data_model import DataModel, AIModel
from view.ui_components import UIComponents, MainPanelComponents
import os

class MainController:
    """Controller chính điều khiển luồng ứng dụng"""
    
    def __init__(self):
        self.data_model = DataModel()
        self.ai_model = AIModel()
        
    def run_application(self):
        """Chạy ứng dụng chính (standalone mode)"""
        UIComponents.setup_page_config()
        UIComponents.load_custom_css()
        UIComponents.display_main_header()
        
        self._handle_main_logic()
    
    def _handle_main_logic(self):
        """Xử lý logic chính của ứng dụng"""
        data_path = st.session_state.get('uploaded_data_path', None)
        if data_path is not None and os.path.exists(data_path):
            self._handle_file_uploaded(data_path)
        else:
            st.warning("⚠️ Vui lòng upload file dữ liệu ở dashboard để sử dụng các chức năng phân tích!")
    
    def _handle_file_uploaded(self, data_path):
        """Xử lý khi file được upload (data_path)"""
        time_frame_months = MainPanelComponents.display_time_frame_selector()
        df_clean = DataModel.load_and_clean_data(data_path, time_frame_months)
        if df_clean is not None:
            self._process_data_analysis(df_clean, time_frame_months)
    
    def _process_data_analysis(self, df_clean, time_frame_months):
        """Xử lý phân tích dữ liệu"""
        available_countries = sorted(df_clean['Country'].unique())
        excluded_countries, excluded_products = MainPanelComponents.display_exclusion_lists(available_countries)
        
        self._display_exclusion_info(excluded_countries, excluded_products)
        
        df_clean = DataModel.filter_excluded_items(df_clean, excluded_countries, excluded_products)
        
        country_stats = DataModel.get_country_selection_options(df_clean, time_frame_months)
        
        country_criteria, num_countries = MainPanelComponents.display_country_selection()
        total_budget, expected_roi = MainPanelComponents.display_budget_parameters()
        min_per_country, max_per_country = MainPanelComponents.display_budget_constraints(total_budget, num_countries)
        
        if MainPanelComponents.display_analyze_button():
            self._run_analysis(
                df_clean, country_stats, country_criteria, num_countries, 
                time_frame_months, total_budget, expected_roi, 
                min_per_country, max_per_country,
                excluded_countries, excluded_products
            )
    
    def _display_exclusion_info(self, excluded_countries, excluded_products):
        """Hiển thị thông tin về các item bị loại trừ"""
        if excluded_countries:
            st.info(f"🚫 Đã loại trừ {len(excluded_countries)} quốc gia: {', '.join(excluded_countries)}")
        
        if excluded_products:
            st.info(f"🚫 Đã loại trừ {len(excluded_products)} sản phẩm")
    
    def _run_analysis(self, df_clean, country_stats, country_criteria, num_countries, 
                     time_frame_months, total_budget, expected_roi, 
                     min_per_country, max_per_country,
                     excluded_countries, excluded_products):
        """Chạy phân tích và hiển thị kết quả"""
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Bước 1: Lọc quốc gia
            status_text.text("🔍 Đang lọc quốc gia theo tiêu chí...")
            progress_bar.progress(20)
            
            selected_countries = DataModel.filter_countries_by_criteria(
                country_stats, country_criteria, num_countries
            )
            
            # Bước 2: Phân tích chi tiết
            status_text.text("🌍 Đang phân tích chi tiết các quốc gia...")
            progress_bar.progress(40)
            
            country_analysis_with_products, top_products_by_country = DataModel.analyze_countries_with_products(
                df_clean, selected_countries, time_frame_months
            )
            
            # Bước 3: Phân bổ ngân sách
            status_text.text("💰 Đang phân bổ ngân sách...")
            progress_bar.progress(60)
            
            allocation_df = DataModel.allocate_budget_by_country(
                country_analysis_with_products, total_budget, min_per_country, max_per_country, expected_roi
            )
            
            # Bước 4: Tạo khuyến nghị chiến lược
            status_text.text("Đang tạo khuyến nghị chiến lược...")
            progress_bar.progress(80)
            
            ai_recommendations = AIModel.generate_static_strategy_recommendations(
                allocation_df, total_budget, expected_roi, time_frame_months
            )
            
            progress_bar.progress(100)
            progress_bar.empty()
            status_text.empty()
            
            st.success("✅ Phân tích hoàn thành!")
            
            # Hiển thị kết quả
            self._display_results(
                time_frame_months, selected_countries, total_budget, expected_roi,
                excluded_countries, excluded_products, country_stats, allocation_df,
                min_per_country, max_per_country, ai_recommendations
            )
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Lỗi trong quá trình phân tích: {str(e)}")
    
    def _display_results(self, time_frame_months, selected_countries, total_budget, expected_roi,
                        excluded_countries, excluded_products, country_stats, allocation_df,
                        min_per_country, max_per_country, ai_recommendations):
        """Hiển thị tất cả kết quả phân tích"""
        
        # Hiển thị thông tin cấu hình
        UIComponents.display_config_info(
            time_frame_months, selected_countries, total_budget, expected_roi,
            excluded_countries, excluded_products
        )
        
        # Hiển thị danh sách quốc gia được chọn
        UIComponents.display_selected_countries(selected_countries, country_stats)
        
        # Hiển thị metrics tổng quan
        UIComponents.display_budget_metrics(selected_countries, total_budget, allocation_df)
        
        # Hiển thị bảng phân tích chi tiết
        UIComponents.display_detailed_analysis_table(allocation_df, time_frame_months)
        
        # Hiển thị bảng phân bổ ngân sách
        UIComponents.display_budget_allocation_table(
            allocation_df, min_per_country, max_per_country, expected_roi
        )
        
        # Hiển thị khuyến nghị chiến lược
        UIComponents.display_ai_recommendations(ai_recommendations)
        
        # Hiển thị section download
        UIComponents.display_download_section(allocation_df, time_frame_months, ai_recommendations) 