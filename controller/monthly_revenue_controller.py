import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from controller.revenue_analysis_controller import RevenueAnalysisController

class MonthlyRevenueController:
    """Controller cho phân tích doanh thu theo tháng/sản phẩm"""
    
    def __init__(self):
        self.revenue_controller = RevenueAnalysisController()
    
    def run(self):
        """Chạy chức năng phân tích doanh thu theo tháng"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 2rem; border-radius: 15px; margin-bottom: 2rem; color: white; text-align: center;">
            <h2>📅 Phân tích Doanh thu theo Tháng</h2>
            <p>Phân tích xu hướng doanh thu theo tháng và chiến lược marketing</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Delegate to revenue analysis controller
        self.revenue_controller.run()
