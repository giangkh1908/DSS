import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from model.decision_model import DecisionModel
from view.dol_view import DolView

class DolController:
    """Controller for DOL (Degree of Operating Leverage) analysis"""
    
    def __init__(self):
        self.view = DolView()
        self.model = self._load_model()
        
        # Initialize session state for DOL
        if 'dol_results_data' not in st.session_state:
            st.session_state.dol_results_data = None
        if 'dol_current_page' not in st.session_state:
            st.session_state.dol_current_page = "input"
    
    @st.cache_resource
    def _load_model(_self):
        """Load the decision model with caching"""
        return DecisionModel()
    
    def run(self):
        """Main method to run DOL analysis"""
        self.view.render_header()
        data_path = st.session_state.get('uploaded_data_path', None)
        if data_path is None or not os.path.exists(data_path):
            st.warning("⚠️ Vui lòng upload file dữ liệu ở dashboard để sử dụng các chức năng phân tích!")
            return
        
        # Navigation
        page = self.view.render_navigation(
            st.session_state.dol_current_page,
            has_results=(st.session_state.dol_results_data is not None)
        )
        
        # Update current page
        st.session_state.dol_current_page = page
        
        # Route to appropriate page
        if page == "input":
            self._show_input_page()
        elif page == "results":
            self._show_results_page()
    
    def _show_input_page(self):
        """Display input page for DOL parameters"""
        self.view.render_input_header()
        
        # Get input data from view
        input_data = self.view.render_input_form(
            available_products=self.model.get_available_products(),
            available_years=self.model.get_available_years()
        )
        
        # Calculate button
        if self.view.render_calculate_button():
            if input_data['product_code']:
                self._calculate_dol(input_data)
            else:
                st.error("Vui lòng chọn một sản phẩm.")
    
    def _show_results_page(self):
        """Display results page"""
        if st.session_state.dol_results_data is None:
            st.warning("Không có dữ liệu kết quả. Vui lòng quay lại trang nhập liệu.")
            if st.button("Quay lại nhập liệu"):
                st.session_state.dol_current_page = "input"
                st.rerun()
            return
        
        results = st.session_state.dol_results_data
        
        # Back button
        if st.button("← Quay lại nhập liệu"):
            st.session_state.dol_current_page = "input"
            st.rerun()
        
        # Render results using view
        self.view.render_results_header()
        self.view.render_summary_table(results, self.model)
        self.view.render_dol_chart(results)
        self.view.render_detailed_analysis(results, self.model)
    
    def _calculate_dol(self, input_data):
        """Calculate DOL with the given input data"""
        with st.spinner("Đang tính toán DOL..."):
            try:
                results = self.model.calculate_dol(
                    variable_cost=input_data['variable_cost'],
                    fixed_cost=input_data['fixed_cost'],
                    time_period=input_data['time_period'],
                    product_code=input_data['product_code'],
                    selected_year=input_data['selected_year']
                )
                st.session_state.dol_results_data = results
                st.session_state.dol_current_page = "results"
                st.success("Tính toán hoàn tất!")
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi khi tính toán: {str(e)}")
                
                # Show debug info
                with st.expander("🔧 Thông tin Debug", expanded=False):
                    st.code(f"Chi tiết lỗi: {str(e)}")
                    st.markdown("""
                    **Có thể do:**
                    1. Sản phẩm không có dữ liệu trong khoảng thời gian đã chọn
                    2. File dữ liệu không tồn tại hoặc bị lỗi
                    3. Thông số đầu vào không hợp lệ
                    4. Lỗi tính toán DOL (chia cho 0)
                    """)
    
    def reset_session(self):
        """Reset DOL session data"""
        st.session_state.dol_results_data = None
        st.session_state.dol_current_page = "input" 