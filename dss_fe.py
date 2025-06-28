"""
DSS - Decision Support System - Comprehensive Business Analytics Platform
Kiến trúc MVC (Model-View-Controller) thuần túy

Main Entry Point cho ứng dụng DSS với 4 chức năng chính:
1. 🤖 Phân bổ Ngân sách - AI-powered budget allocation
2. 📈 Phân tích Doanh thu - Country revenue analysis  
3. 📅 Phân tích Tháng - Monthly trend analysis
4. 🔢 Phân tích DOL - Degree of Operating Leverage analysis
"""

import warnings
warnings.filterwarnings('ignore')
import sys
import os

from controller.app_controller import AppController

def main():
    """Main function khởi chạy ứng dụng DSS tích hợp với kiến trúc MVC thuần túy"""
    try: 
        app_controller = AppController()
        app_controller.run_application()
    except Exception as e:
        import streamlit as st
        st.error(f"❌ Lỗi khởi tạo ứng dụng: {str(e)}")
        st.info("💡 Vui lòng kiểm tra lại cấu hình và thử lại")
        
        with st.expander("🔧 Thông tin Debug", expanded=False):
            st.code(f"Chi tiết lỗi: {str(e)}")
            st.markdown("""
            **Các bước khắc phục:**
            1. Kiểm tra cấu trúc thư mục MVC
            2. Đảm bảo các file model, view, controller tồn tại
            3. Kiểm tra đường dẫn file dữ liệu (data/online_retail.csv)
            4. Kiểm tra các dependencies trong requirements.txt
            5. Khởi động lại ứng dụng
            """)

if __name__ == "__main__":
    main()