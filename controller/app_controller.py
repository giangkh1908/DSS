"""
Controller tổng thể để quản lý 3 chức năng chính của ứng dụng DSS
"""

import streamlit as st
import sys
import os

# Thêm đường dẫn để import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class AppController:
    """Controller chính điều phối giữa 3 chức năng"""
    
    def __init__(self):
        # Khởi tạo session state nếu chưa có
        if 'current_mode' not in st.session_state:
            st.session_state.current_mode = None
        
    def run_application(self):
        """Chạy ứng dụng với menu lựa chọn chức năng hoặc từng chức năng riêng biệt"""
        st.set_page_config(
            page_title="DSS - Decision Support System",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # Nếu chưa chọn chức năng, chỉ hiển thị dashboard (header, chọn chức năng, welcome, bảng so sánh, ...)
        if st.session_state.current_mode is None:
            self._render_dashboard()
        # Nếu đã chọn chức năng, chỉ hiển thị UI của chức năng đó (không render dashboard/header/welcome)
        elif st.session_state.current_mode == "Phân bổ Ngân sách":
            self._run_budget_allocation_mode()
        elif st.session_state.current_mode == "Phân tích Doanh thu":
            self._run_revenue_analysis_mode()
        elif st.session_state.current_mode == "Phân tích Tháng":
            self._run_monthly_revenue_mode()
        elif st.session_state.current_mode == "Phân tích DOL":
            self._run_dol_analysis_mode()
    
    def _render_dashboard(self):
        """Render toàn bộ dashboard, header, chọn chức năng, welcome, bảng so sánh, ..."""
        # CSS tùy chỉnh
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .feature-card {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #667eea;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .sidebar-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 1rem;
        }
        .mode-selection {
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
            border: 1px solid #e9ecef;
        }
        .mode-card {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #e9ecef;
            text-align: center;
            margin-top: 1rem;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .mode-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }
        .mode-card:hover::before {
            transform: scaleX(1);
        }
        .mode-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        }
        .mode-card.selected {
            border-color: #667eea;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            transform: translateY(-3px);
        }
        .mode-card.selected::before {
            transform: scaleX(1);
            background: rgba(255, 255, 255, 0.3);
        }
        .mode-description {
            font-size: 1rem;
            line-height: 1.5;
            margin-bottom: 1rem;
        }
        .mode-features {
            font-size: 0.9rem;
            opacity: 0.8;
            line-height: 1.6;
            margin-top: 1rem;
        }
        .config-section {
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0;
            border: 1px solid #e9ecef;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        .config-section h3 {
            color: #333;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #667eea;
        }
        @media (max-width: 768px) {
            .mode-card {
                margin: 0.5rem 0;
                padding: 1.5rem;
            }
            .main-header h1 {
                font-size: 1.8rem;
            }
        }
        </style>
        """, unsafe_allow_html=True)

        # Header chính
        st.markdown("""
        <div class="main-header">
            <h1>🏢 DSS - Decision Support System</h1>
            <p>Hệ thống hỗ trợ quyết định cho Marketing và Phân tích Doanh thu</p>
        </div>
        """, unsafe_allow_html=True)

        # File uploader chung
        with st.container():
            st.markdown("### 📁 Upload Dữ Liệu Phân Tích")
            if 'uploaded_data_path' not in st.session_state or not os.path.exists(st.session_state['uploaded_data_path']):
                uploaded_file = st.file_uploader(
                    "Chọn file CSV của bạn",
                    type=['csv'],
                    help="File cần có các cột: InvoiceDate, Country, CustomerID, Quantity, UnitPrice"
                )
                if uploaded_file is not None:
                    save_path = os.path.join('data', 'uploaded_data.csv')
                    with open(save_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    st.session_state['uploaded_data_path'] = save_path
                    st.session_state['uploaded_file_name'] = uploaded_file.name
                    st.success(f"✅ Đã upload: {uploaded_file.name}")
            else:
                file_name = st.session_state.get('uploaded_file_name', 'Chưa rõ')
                col1, col2 = st.columns([8,1])
                with col1:
                    st.info(f"📂 Đang sử dụng file: {file_name}")
                with col2:
                    if st.button("❌", key="remove_uploaded_file", help="Gỡ file dữ liệu", use_container_width=True):
                        del st.session_state['uploaded_data_path']
                        if 'uploaded_file_name' in st.session_state:
                            del st.session_state['uploaded_file_name']
                        st.rerun()
                # Cho phép upload lại file mới ngay cả khi đã có file
                uploaded_file = st.file_uploader(
                    "Thay thế file CSV",
                    type=['csv'],
                    help="Upload file mới để thay thế file hiện tại"
                )
                if uploaded_file is not None:
                    save_path = os.path.join('data', 'uploaded_data.csv')
                    with open(save_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    st.session_state['uploaded_data_path'] = save_path
                    st.session_state['uploaded_file_name'] = uploaded_file.name
                    st.success(f"✅ Đã thay thế file: {uploaded_file.name}")

        # Header thanh ngang để chọn chức năng
        self._display_mode_selection()

        # Hiển thị màn hình hướng dẫn, bảng so sánh, ...
        self._display_welcome_screen()
    
    def _display_mode_selection(self):
        """Hiển thị thanh ngang để chọn chức năng"""
        st.markdown("""
        <div class="mode-selection">
            <h2 style="text-align: center; color: #333; margin-bottom: 2rem;">
                🎯 Chọn Chức năng
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Tạo 4 cột cho 4 chức năng
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Hiển thị card cho chức năng 1
            card_class = "selected" if st.session_state.current_mode == "Phân bổ Ngân sách" else ""
            
            # Container có thể click được
            card_container = st.container()
            with card_container:
                if st.button(
                    "🤖 Phân bổ Ngân sách",
                    key="budget_mode",
                    help="Chức năng phân bổ ngân sách với AI",
                    use_container_width=True,
                    type="primary" if st.session_state.current_mode == "Phân bổ Ngân sách" else "secondary"
                ):
                    st.session_state.current_mode = "Phân bổ Ngân sách"
                    st.rerun()
                
                st.markdown(f"""
                <div class="mode-card {card_class}">
                    <div class="mode-description">
                        💼 Phân tích dữ liệu khách hàng và đề xuất phân bổ ngân sách tối ưu
                    </div>
                    <div class="mode-features">
                        ✓ Upload CSV data<br>
                        ✓ Smart Recommendations<br>
                        ✓ ROI Forecasting<br>
                        ✓ Budget Optimization
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Hiển thị card cho chức năng 2
            card_class = "selected" if st.session_state.current_mode == "Phân tích Doanh thu" else ""
            
            # Container có thể click được
            card_container = st.container()
            with card_container:
                if st.button(
                    "📈 Phân tích Doanh thu",
                    key="revenue_mode", 
                    help="Chức năng phân tích doanh thu theo quốc gia",
                    use_container_width=True,
                    type="primary" if st.session_state.current_mode == "Phân tích Doanh thu" else "secondary"
                ):
                    st.session_state.current_mode = "Phân tích Doanh thu"
                    st.rerun()
                
                st.markdown(f"""
                <div class="mode-card {card_class}">
                    <div class="mode-description">
                        📊 Phân tích doanh thu theo quốc gia và tính toán tốc độ tăng trưởng
                    </div>
                    <div class="mode-features">
                        ✓ Country Analysis<br>
                        ✓ Growth Rate Calculation<br>
                        ✓ Revenue Comparison<br>
                        ✓ Trend Forecasting
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            # Hiển thị card cho chức năng 3 - Phân tích Tháng
            card_class = "selected" if st.session_state.current_mode == "Phân tích Tháng" else ""
            
            card_container = st.container()
            with card_container:
                if st.button(
                    "📅 Phân tích Tháng",
                    key="monthly_mode", 
                    help="Phân tích doanh thu theo từng tháng",
                    use_container_width=True,
                    type="primary" if st.session_state.current_mode == "Phân tích Tháng" else "secondary"
                ):
                    st.session_state.current_mode = "Phân tích Tháng"
                    st.rerun()
                
                st.markdown(f"""
                <div class="mode-card {card_class}">
                    <div class="mode-description">
                        📅 Phân tích xu hướng doanh thu theo từng tháng
                    </div>
                    <div class="mode-features">
                        ✓ Monthly Trends<br>
                        ✓ Peak/Low Analysis<br>
                        ✓ Seasonal Patterns<br>
                        ✓ Strategic Insights
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col4:
            # Hiển thị card cho chức năng 4 - Phân tích DOL
            card_class = "selected" if st.session_state.current_mode == "Phân tích DOL" else ""
            
            card_container = st.container()
            with card_container:
                if st.button(
                    "🔢 Phân tích DOL",
                    key="dol_mode", 
                    help="Phân tích Degree of Operating Leverage",
                    use_container_width=True,
                    type="primary" if st.session_state.current_mode == "Phân tích DOL" else "secondary"
                ):
                    st.session_state.current_mode = "Phân tích DOL"
                    st.rerun()
                
                st.markdown(f"""
                <div class="mode-card {card_class}">
                    <div class="mode-description">
                        🔢 Phân tích độ nhạy cảm hoạt động và dự báo DOL
                    </div>
                    <div class="mode-features">
                        ✓ DOL Calculation<br>
                        ✓ Monthly Analysis<br>
                        ✓ Sensitivity Analysis<br>
                        ✓ Strategic Recommendations
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Hiển thị thông tin bổ sung nếu đã chọn
        if st.session_state.current_mode == "Phân bổ Ngân sách":
            st.info("🤖 **Chế độ:** Phân bổ Ngân sách - Upload file CSV để bắt đầu phân tích")
        elif st.session_state.current_mode == "Phân tích Doanh thu":
            st.info("📈 **Chế độ:** Phân tích Doanh thu - Upload file dữ liệu bán hàng để phân tích")
        elif st.session_state.current_mode == "Phân tích Tháng":
            st.info("📅 **Chế độ:** Phân tích Tháng - Phân tích xu hướng doanh thu theo tháng")
        elif st.session_state.current_mode == "Phân tích DOL":
            st.info("🔢 **Chế độ:** Phân tích DOL - Tính toán độ nhạy cảm hoạt động và dự báo")
    
    def _display_welcome_screen(self):
        """Hiển thị màn hình hướng dẫn"""
        if st.session_state.current_mode is None:
            st.markdown("""
            ### 👋 Chào mừng bạn đến với DSS - Decision Support System
            
            Vui lòng chọn một trong bốn chức năng phía trên để bắt đầu:
            """)
        
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>🤖 Chi tiết Phân bổ Ngân sách</h3>
                <p><strong>Quy trình làm việc:</strong></p>
                <ol>
                    <li>Upload file CSV dữ liệu khách hàng</li>
                    <li>Cấu hình thời gian và ngân sách</li>
                    <li>Chọn tiêu chí lọc quốc gia</li>
                    <li>Phân tích và đề xuất</li>
                    <li>Xuất báo cáo kết quả</li>
                </ol>
                <p><strong>Format dữ liệu cần:</strong></p>
                <code>InvoiceDate, Country, CustomerID, Quantity, UnitPrice</code>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>📈 Chi tiết Phân tích Doanh thu</h3>
                <p><strong>Quy trình làm việc:</strong></p>
                <ol>
                    <li>Upload file CSV/Excel doanh thu</li>
                    <li>Chọn khoảng thời gian phân tích</li>
                    <li>Lọc quốc gia và ngưỡng doanh thu</li>
                    <li>Chọn loại phân tích cần thiết</li>
                    <li>Xem kết quả và dự báo</li>
                </ol>
                <p><strong>Format dữ liệu cần:</strong></p>
                <code>InvoiceDate, Country, Revenue</code>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h3>📅 Chi tiết Phân tích Tháng</h3>
                <p><strong>Quy trình làm việc:</strong></p>
                <ol>
                    <li>Upload file CSV dữ liệu bán hàng</li>
                    <li>Chọn sản phẩm cần phân tích</li>
                    <li>Thiết lập khoảng thời gian</li>
                    <li>Xem biểu đồ xu hướng theo tháng</li>
                    <li>Nhận gợi ý chiến lược kinh doanh</li>
                </ol>
                <p><strong>Format dữ liệu cần:</strong></p>
                <code>InvoiceDate, Description, Quantity, UnitPrice</code>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="feature-card">
                <h3>🔢 Chi tiết Phân tích DOL</h3>
                <p><strong>Quy trình làm việc:</strong></p>
                <ol>
                    <li>Nhập chi phí biến đổi và cố định</li>
                    <li>Chọn sản phẩm và khoảng thời gian</li>
                    <li>Tính toán DOL và độ nhạy cảm</li>
                    <li>Xem biểu đồ xu hướng theo tháng</li>
                    <li>Nhận khuyến nghị chiến lược</li>
                </ol>
                <p><strong>Format dữ liệu cần:</strong></p>
                <code>InvoiceDate, StockCode, Quantity, UnitPrice</code>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        ### 📊 So sánh Tính năng
        
        | Tính năng | Phân bổ Ngân sách | Phân tích Doanh thu | Phân tích Tháng | Phân tích DOL |
        |-----------|---------------------|-------------------|----------------|-------------|
        | **Đối tượng** | Marketing Manager | Sales Analyst | Business Analyst | Financial Analyst |
        | **Input** | Customer Data CSV | Revenue Data CSV/Excel | Sales Data CSV | Cost & Product Data |
        | **AI Support** | ✅ Smart Recommendations | ✅ Trend Analysis | ✅ Pattern Recognition | ✅ Sensitivity Analysis |
        | **Output** | Budget Allocation Plan | Revenue Analysis Report | Monthly Trend Report | DOL Analysis Report |
        | **Forecasting** | ROI Prediction | Growth Rate Prediction | Seasonal Forecasting | Leverage Forecasting |
        """)
        
        # Hiển thị thông tin hệ thống
        with st.expander("ℹ️ Thông tin Hệ thống", expanded=False):
            st.markdown("""
            **Phiên bản:** 2.0  
            **Kiến trúc:** MVC (Model-View-Controller)  
            **Công nghệ:** Streamlit + AI Integration  
            **Cập nhật:** Tháng 6, 2025  
            """)
    
    def _run_budget_allocation_mode(self):
        """Chạy chức năng phân bổ ngân sách"""
        try:
            # Nút quay lại với styling đẹp hơn
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                if st.button("⬅️ Quay lại Menu", key="back_from_budget", type="secondary"):
                    st.session_state.current_mode = None
                    st.rerun()
            
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 2rem; border-radius: 15px; margin-bottom: 2rem; color: white; text-align: center;">
                <h2>🤖 Phân bổ Ngân sách</h2>
                <p>Hệ thống thông minh phân tích dữ liệu và đề xuất phân bổ ngân sách tối ưu</p>
            </div>
            """, unsafe_allow_html=True)
            
            from controller.main_controller import MainController
            
            # Khởi tạo và chạy controller chính
            main_controller = MainController()
            main_controller._handle_main_logic()
            
        except ImportError as e:
            st.error(f"❌ Lỗi Import: {str(e)}")
            st.info("💡 Kiểm tra các file trong thư mục model và view")
        except AttributeError as e:
            st.error(f"❌ Lỗi Method: {str(e)}")
            st.info("💡 Kiểm tra method _handle_main_logic() trong MainController")
        except Exception as e:
            st.error(f"❌ Lỗi khác: {str(e)}")
            
            # Debug info chi tiết
            with st.expander("🔧 Thông tin Debug chi tiết"):
                import traceback
                st.code(traceback.format_exc())
    
    def _run_dol_analysis_mode(self):
        """Chạy chức năng phân tích DOL"""
        try:
            # Nút quay lại
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                if st.button("⬅️ Quay lại Menu", key="back_from_dol", type="secondary"):
                    st.session_state.current_mode = None
                    st.rerun()
            
            # Import và chạy DOL controller
            from controller.dol_controller import DolController
            
            dol_controller = DolController()
            dol_controller.run()
            
        except ImportError as e:
            st.error(f"❌ Lỗi Import: {str(e)}")
            st.info("💡 Kiểm tra file dol_controller.py và các dependencies")
        except Exception as e:
            st.error(f"❌ Lỗi khác: {str(e)}")
            
            # Debug info chi tiết
            with st.expander("🔧 Thông tin Debug chi tiết"):
                import traceback
                st.code(traceback.format_exc())
    
    def _run_revenue_analysis_mode(self):
        """Chạy chức năng phân tích doanh thu"""
        try:
            # Nút quay lại với styling đẹp hơn
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                if st.button("⬅️ Quay lại Menu", key="back_from_revenue", type="secondary"):
                    st.session_state.current_mode = None
                    st.rerun()
            
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 2rem; border-radius: 15px; margin-bottom: 2rem; color: white; text-align: center;">
                <h2>📈 Phân tích Doanh thu Quốc gia</h2>
                <p>Phân tích chi tiết doanh thu theo từng quốc gia và xu hướng tăng trưởng</p>
            </div>
            """, unsafe_allow_html=True)
            
            from controller.app_L import main as revenue_analysis_main
            
            # Chạy chức năng phân tích doanh thu
            revenue_analysis_main()
            
        except ImportError as e:
            st.error(f"❌ Lỗi Import: {str(e)}")
            st.info("💡 Kiểm tra file app_L.py và các dependencies")
        except Exception as e:
            st.error(f"❌ Lỗi khác: {str(e)}")
            
            # Debug info chi tiết
            with st.expander("🔧 Thông tin Debug chi tiết"):
                import traceback
                st.code(traceback.format_exc())
    
    def _run_monthly_revenue_mode(self):
        """Chạy chức năng phân tích doanh thu theo tháng"""
        try:
            # Nút quay lại
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                if st.button("⬅️ Quay lại Menu", key="back_from_monthly", type="secondary"):
                    st.session_state.current_mode = None
                    st.rerun()
            
            # Import controller và chạy
            from controller.monthly_revenue_controller import MonthlyRevenueController
            
            monthly_controller = MonthlyRevenueController()
            monthly_controller.run()
            
        except ImportError as e:
            st.error(f"❌ Lỗi Import: {str(e)}")
            st.info("💡 Kiểm tra file monthly_revenue_controller.py và các dependencies")
        except Exception as e:
            st.error(f"❌ Lỗi khác: {str(e)}")
            
            # Debug info chi tiết
            with st.expander("🔧 Thông tin Debug chi tiết"):
                import traceback
                st.code(traceback.format_exc())
