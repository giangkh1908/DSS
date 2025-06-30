import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

class UIComponents:
    """View class chứa tất cả UI components và layout"""
    
    @staticmethod
    def setup_page_config():
        """Cấu hình trang Streamlit"""
        st.set_page_config(
            page_title="DSS - Phân Bổ Ngân Sách Marketing Theo Quốc Gia",
            page_icon="🌍",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    @staticmethod
    def load_custom_css():
        """Load custom CSS styles"""
        st.markdown("""
        <style>
            .main-header {
                font-size: 3rem;
                font-weight: bold;
                text-align: center;
                background: linear-gradient(90deg, #1f77b4, #2e8b57);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 2rem;
            }
            
            .metric-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1.5rem;
                border-radius: 15px;
                color: white;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                margin: 0.5rem 0;
            }
            
            .country-card {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                padding: 1.5rem;
                border-radius: 15px;
                color: white;
                margin: 1rem 0;
            }
            
            .analysis-table {
                background: white;
                padding: 1.5rem;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                margin: 1rem 0;
            }
            
            .investment-level {
                padding: 1rem;
                margin: 0.5rem 0;
                border-radius: 10px;
                border-left: 5px solid;
            }
            
            .high-investment {
                background-color: #e8f5e8;
                border-left-color: #4caf50;
            }
            
            .medium-investment {
                background-color: #fff3cd;
                border-left-color: #ffc107;
            }
            
            .low-investment {
                background-color: #f8d7da;
                border-left-color: #dc3545;
            }
            
            .recommendation-card {
                background: linear-gradient(135deg, #a8e6cf 0%, #88d8c0 100%);
                padding: 1.5rem;
                border-radius: 15px;
                color: #2c3e50;
                margin: 1rem 0;
                border-left: 5px solid #27ae60;
            }
            
            .ai-recommendation {
                background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
                padding: 2rem;
                border-radius: 15px;
                color: black;
                margin: 1.5rem 0;
                border-left: 5px solid #ff6b6b;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def display_main_header():
        """Hiển thị header chính"""
        st.markdown('<h1 class="main-header">🌍 DSS - Phân Bổ Ngân Sách Theo Quốc Gia</h1>', 
                    unsafe_allow_html=True)
    
    @staticmethod
    def display_welcome_screen():
        """Hiển thị màn hình chào mừng khi chưa upload file"""
        st.markdown("""
        <div class="recommendation-card">
            <h2>🌍 DSS Marketing Intelligence - Country Focus</h2>
            <p><strong>Hệ thống phân bổ ngân sách tập trung theo quốc gia</strong></p>
            <h4>🔧 Hướng dẫn sử dụng:</h4>
            <ol>
                <li>📁 Upload file CSV dữ liệu bán hàng</li>
                <li>📅 Chọn khung thời gian phân tích (3-24 tháng)</li>
                <li>🚫 Thiết lập danh sách loại trừ (nếu có)</li>
                <li>⚙️ Cấu hình tham số ngân sách và ROI</li>
                <li>🚀 Bắt đầu phân tích và nhận kết quả</li>
            </ol>
        
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def display_config_info(time_frame_months, selected_countries, total_budget, expected_roi, excluded_countries, excluded_products):
        """Hiển thị thông tin cấu hình phân tích"""
        st.markdown("## ⚙️ Cấu Hình Phân Tích")
        config_col1, config_col2, config_col3 = st.columns(3)
        
        with config_col1:
            st.info(f"📅 **Khung thời gian:** {time_frame_months} tháng gần nhất")
            st.info(f"🌍 **Số quốc gia:** {len(selected_countries)}")
        
        with config_col2:
            st.info(f"💰 **Tổng ngân sách:** ${total_budget:,}")
            st.info(f"📈 **ROI dự kiến:** {expected_roi}%")
        
        with config_col3:
            st.info(f"🚫 **Quốc gia loại trừ:** {len(excluded_countries)}")
            st.info(f"🚫 **Sản phẩm loại trừ:** {len(excluded_products)}")
    
    @staticmethod
    def display_selected_countries(selected_countries, country_stats):
        """Hiển thị danh sách quốc gia được chọn"""
        st.markdown("## 📋 Danh Sách Quốc Gia Được Phân Tích")
        
        cols = st.columns(4)
        for i, country in enumerate(selected_countries):
            with cols[i % 4]:
                country_info = country_stats[country_stats['Country'] == country].iloc[0]
                st.markdown(f"""
                <div class="country-card">
                    <h4>🌍 {country}</h4>
                    <p><strong>Doanh thu:</strong> ${country_info['Total_Revenue']:,.0f}</p>
                    <p><strong>Đơn hàng:</strong> {country_info['Order_Count']:,}</p>
                </div>
                """, unsafe_allow_html=True)
    
    @staticmethod
    def display_budget_metrics(selected_countries, total_budget, allocation_df):
        """Hiển thị metrics tổng quan ngân sách"""
        st.markdown("## 📊 Tổng Quan Ngân Sách")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🌍</h3>
                <h2>{len(selected_countries)}</h2>
                <p>Quốc gia</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>💰</h3>
                <h2>${total_budget:,.0f}</h2>
                <p>Tổng ngân sách</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_allocation = allocation_df['Allocated_Budget'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <h3>📊</h3>
                <h2>${avg_allocation:,.0f}</h2>
                <p>Ngân sách TB</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_expected_profit = allocation_df['Expected_Profit'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <h3>💵</h3>
                <h2>${total_expected_profit:,.0f}</h2>
                <p>Lợi nhuận dự kiến</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            roi_percent = (total_expected_profit / total_budget) * 100
            st.markdown(f"""
            <div class="metric-card">
                <h3>📈</h3>
                <h2>{roi_percent:.1f}%</h2>
                <p>ROI thực tế</p>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def display_detailed_analysis_table(allocation_df, time_frame_months):
        """Hiển thị bảng phân tích chi tiết quốc gia"""
        st.markdown(f"## 📋 Bảng Phân Tích Chi Tiết Quốc Gia ({time_frame_months} tháng)")
        st.markdown("*Phân tích toàn diện các chỉ số hiệu suất kinh doanh của từng quốc gia*")
        
        detailed_df = allocation_df[['Country', 'Total_Revenue', 'Avg_Monthly_Revenue', 
                                   'Avg_Orders_Per_Month', 'Revenue_Stability', 
                                   'Overall_Score', 'Risk_Level', 'Investment_Potential']].copy()
        
        detailed_df.columns = [
            'Quốc Gia', 
            f'Tổng Doanh Thu {time_frame_months}T ($)',
            'Doanh Thu TB/Tháng ($)', 
            'Đơn Hàng TB/Tháng',
            'Độ Ổn Định Doanh Thu',
            'Điểm Tổng Hợp',
            'Mức Rủi Ro',
            'Tiềm Năng Đầu Tư'
        ]
        
        detailed_df[f'Tổng Doanh Thu {time_frame_months}T ($)'] = detailed_df[f'Tổng Doanh Thu {time_frame_months}T ($)'].apply(lambda x: f"${x:,.0f}")
        detailed_df['Doanh Thu TB/Tháng ($)'] = detailed_df['Doanh Thu TB/Tháng ($)'].apply(lambda x: f"${x:,.0f}")
        detailed_df['Đơn Hàng TB/Tháng'] = detailed_df['Đơn Hàng TB/Tháng'].apply(lambda x: f"{x:.1f}")
        detailed_df['Độ Ổn Định Doanh Thu'] = detailed_df['Độ Ổn Định Doanh Thu'].apply(lambda x: f"{x:.2f}")
        detailed_df['Điểm Tổng Hợp'] = detailed_df['Điểm Tổng Hợp'].apply(lambda x: f"{x:.1f}/10")
        
        st.dataframe(detailed_df, use_container_width=True, hide_index=True)
        
        UIComponents.display_analysis_explanation()
    
    @staticmethod
    def display_analysis_explanation():
        """Hiển thị giải thích các chỉ số phân tích"""
        with st.expander("📖 Giải Thích Các Chỉ Số Phân Tích"):
            st.markdown("""
            **🔍 Ý nghĩa các chỉ số:**
            
            • **Tổng Doanh Thu:** Tổng doanh thu của quốc gia trong khung thời gian phân tích
            
            • **Doanh Thu TB/Tháng:** Doanh thu trung bình mỗi tháng, cho biết quy mô thị trường
            
            • **Đơn Hàng TB/Tháng:** Số đơn hàng trung bình mỗi tháng, thể hiện mức độ hoạt động thị trường (>50 = sôi động, >100 = rất sôi động)
            
            • **Độ Ổn Định Doanh Thu:** Chỉ số ổn định doanh thu theo tháng (>0.5 = ổn định, >1.0 = rất ổn định)
            
            • **Điểm Tổng Hợp:** Tổng hợp Revenue (50%), Order Frequency (35%), Stability (15%) thành điểm từ 0-10 (>7 = xuất sắc, 4-7 = tốt, <4 = cần cải thiện)
            
            • **Mức Rủi Ro:** Đánh giá rủi ro đầu tư (Thấp = an toàn, Trung Bình = cân nhắc, Cao = thận trọng)
            
            • **Tiềm Năng Đầu Tư:** Khuyến nghị mức độ đầu tư (Cao = ưu tiên, Trung Bình = cân bằng, Thấp = hạn chế)
            """)
    
    @staticmethod
    def display_budget_allocation_table(allocation_df, min_per_country, max_per_country, expected_roi):
        """Hiển thị bảng phân bổ ngân sách chi tiết"""
        st.markdown("## 💰 Bảng Phân Bổ Ngân Sách Chi Tiết")
        st.markdown("*Kế hoạch phân bổ ngân sách và dự báo lợi nhuận cho từng quốc gia*")
        
        budget_detailed_df = allocation_df[['Country', 'Overall_Score', 'Allocated_Budget', 'Investment_Percentage', 
                                          'Expected_Profit', 'Total_Return', 'Investment_Level', 'Risk_Level']].copy()
        
        budget_detailed_df.columns = [
            'Quốc Gia',
            'Điểm Đánh Giá',
            'Ngân Sách Được Phân Bổ ($)',
            'Tỷ Lệ Ngân Sách (%)', 
            'Lợi Nhuận Dự Kiến ($)',
            'Tổng Thu Về Dự Kiến ($)',
            'Mức Độ Đầu Tư',
            'Mức Rủi Ro'
        ]
        
        budget_detailed_df['Điểm Đánh Giá'] = budget_detailed_df['Điểm Đánh Giá'].apply(lambda x: f"{x:.1f}/10")
        budget_detailed_df['Ngân Sách Được Phân Bổ ($)'] = budget_detailed_df['Ngân Sách Được Phân Bổ ($)'].apply(lambda x: f"${x:,.0f}")
        budget_detailed_df['Tỷ Lệ Ngân Sách (%)'] = budget_detailed_df['Tỷ Lệ Ngân Sách (%)'].apply(lambda x: f"{x:.1f}%")
        budget_detailed_df['Lợi Nhuận Dự Kiến ($)'] = budget_detailed_df['Lợi Nhuận Dự Kiến ($)'].apply(lambda x: f"${x:,.0f}")
        budget_detailed_df['Tổng Thu Về Dự Kiến ($)'] = budget_detailed_df['Tổng Thu Về Dự Kiến ($)'].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(budget_detailed_df, use_container_width=True, hide_index=True)
        
        UIComponents.display_budget_strategy_explanation(min_per_country, max_per_country, expected_roi)
    
    @staticmethod
    def display_budget_strategy_explanation(min_per_country, max_per_country, expected_roi):
        """Hiển thị giải thích chiến lược phân bổ ngân sách"""
        with st.expander("💡 Giải Thích Chiến Lược Phân Bổ Ngân Sách"):
            st.markdown(f"""
            **🎯 Nguyên tắc phân bổ ngân sách:**
            
            **1. Dựa trên Điểm Đánh Giá Tổng Hợp:**
            - Quốc gia có điểm cao hơn sẽ nhận ngân sách lớn hơn
            - Công thức: (Điểm quốc gia / Tổng điểm) × Tổng ngân sách
            
            **2. Áp dụng Giới Hạn Min/Max:**
            - Ngân sách tối thiểu: ${min_per_country:,} cho mỗi quốc gia
            - Ngân sách tối đa: ${max_per_country:,} cho mỗi quốc gia
            - Đảm bảo không có quốc gia nào bị bỏ quên hoặc chiếm quá nhiều tài nguyên
            
            **3. Tính Toán ROI:**
            - ROI dự kiến được thiết lập: {expected_roi}%
            - Lợi nhuận dự kiến = Ngân sách × ({expected_roi}% / 100)
            - Tổng thu về = Ngân sách + Lợi nhuận dự kiến
            
            **4. Phân Loại Mức Độ Đầu Tư:**
            - **Rất Cao (≥25%):** Thị trường chiến lược, tập trung tài nguyên chính
            - **Cao (15-24%):** Thị trường quan trọng, đầu tư mạnh mẽ
            - **Trung Bình (10-14%):** Thị trường ổn định, duy trì và phát triển
            - **Thấp (<10%):** Thị trường thử nghiệm, đầu tư thận trọng
            """)
    
    @staticmethod
    def display_charts(allocation_df, time_frame_months):
        """Hiển thị biểu đồ phân tích hỗ trợ quyết định đầu tư"""
        st.markdown(f"## 📊 Biểu Đồ Hỗ Trợ Quyết định Đầu Tư")
        st.markdown("*Các biểu đồ giúp bạn đưa ra quyết định đầu tư thông minh*")
        
        # Tính toán ROI efficiency
        allocation_df['ROI_Efficiency'] = (allocation_df['Expected_Profit'] / allocation_df['Allocated_Budget']) * 100
        
        # 1. BIỂU ĐỒ HIỆU QUẢ ĐẦU TƯ (full width)
        st.markdown("### 💰 Hiệu Quả Đầu Tư: Ngân Sách vs Lợi Nhuận")
        
        fig1 = go.Figure()
        
        # Thêm scatter plot cho từng quốc gia
        fig1.add_trace(go.Scatter(
            x=allocation_df['Allocated_Budget'],
            y=allocation_df['Expected_Profit'],
            mode='markers+text',
            marker=dict(
                size=15,
                color=allocation_df['ROI_Efficiency'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(
                    title="ROI (%)",
                    thickness=15,
                    len=0.8
                )
            ),
            text=allocation_df['Country'],
            textposition='top center',
            name='Quốc Gia'
        ))
        
        # Thêm đường reference ROI = target
        max_budget = allocation_df['Allocated_Budget'].max()
        target_roi = allocation_df['Expected_Profit'].iloc[0] / allocation_df['Allocated_Budget'].iloc[0]
        
        fig1.add_trace(go.Scatter(
            x=[0, max_budget],
            y=[0, max_budget * target_roi],
            mode='lines',
            line=dict(dash='dash', color='red', width=2),
            name=f'ROI Target Line',
            showlegend=True
        ))
        
        fig1.update_layout(
            xaxis_title='Ngân Sách Đầu Tư ($)',
            yaxis_title='Lợi Nhuận Dự Kiến ($)',
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        
        # Insight box cho ROI
        col1, col2, col3 = st.columns(3)
        
        with col1:
            best_roi_country = allocation_df.loc[allocation_df['ROI_Efficiency'].idxmax()]
            st.success(f"🏆 **Hiệu quả cao nhất**\n{best_roi_country['Country']}\nROI: {best_roi_country['ROI_Efficiency']:.1f}%")
        
        with col2:
            worst_roi_country = allocation_df.loc[allocation_df['ROI_Efficiency'].idxmin()]
            st.error(f"⚠️ **Hiệu quả thấp nhất**\n{worst_roi_country['Country']}\nROI: {worst_roi_country['ROI_Efficiency']:.1f}%")
        
        with col3:
            avg_roi = allocation_df['ROI_Efficiency'].mean()
            above_avg = len(allocation_df[allocation_df['ROI_Efficiency'] > avg_roi])
            st.info(f"📊 **ROI trung bình**\n{avg_roi:.1f}%\n{above_avg}/{len(allocation_df)} quốc gia trên TB")
        
        # 2. BIỂU ĐỒ PHÂN BỔ NGÂN SÁCH
        st.markdown("### 🥧 Phân Bổ Ngân Sách Theo Quốc Gia")
        
        col4, col5 = st.columns([2, 1])
        
        with col4:
            # Investment level colors
            level_colors = {
                'Rất Cao': '#d62728',   # Red
                'Cao': '#ff7f0e',        # Orange  
                'Trung Bình': '#2ca02c', # Green
                'Thấp': '#1f77b4'        # Blue
            }
            colors_pie = [level_colors.get(level, '#gray') for level in allocation_df['Investment_Level']]
            
            fig2 = go.Figure()
            fig2.add_trace(go.Pie(
                labels=allocation_df['Country'],
                values=allocation_df['Allocated_Budget'],
                marker=dict(colors=colors_pie),
                textinfo='label+percent',
                textfont_size=12,
                hole=0.3
            ))
            
            fig2.update_layout(
                height=400,
                showlegend=True
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        
        with col5:
            st.markdown("### 📋 Thống Kê Phân Bổ")
            
            # Top 3 countries by budget
            top_3_budget = allocation_df.head(3)
            total_top3_budget = top_3_budget['Allocated_Budget'].sum()
            top3_percentage = (total_top3_budget / allocation_df['Allocated_Budget'].sum()) * 100
            
            st.metric(
                "Top 3 quốc gia chiếm", 
                f"{top3_percentage:.1f}%",
                f"${total_top3_budget:,.0f}"
            )
            
            # Concentration risk
            max_percentage = (allocation_df['Allocated_Budget'].max() / allocation_df['Allocated_Budget'].sum()) * 100
            if max_percentage > 40:
                st.error(f"⚠️ Rủi ro tập trung cao: {max_percentage:.1f}%")
            elif max_percentage > 25:
                st.warning(f"⚡ Tập trung trung bình: {max_percentage:.1f}%")
            else:
                st.success(f"✅ Phân bổ cân bằng: {max_percentage:.1f}%")
            
            # Investment level distribution
            st.markdown("**Phân loại đầu tư:**")
            investment_counts = allocation_df['Investment_Level'].value_counts()
            for level, count in investment_counts.items():
                percentage = (count / len(allocation_df)) * 100
                st.text(f"• {level}: {count} quốc gia ({percentage:.0f}%)")
            
            # Risk level distribution
            st.markdown("**Phân loại rủi ro:**")
            risk_counts = allocation_df['Risk_Level'].value_counts()
            for risk, count in risk_counts.items():
                percentage = (count / len(allocation_df)) * 100
                color = "🟢" if risk == "Thấp" else "🟡" if risk == "Trung Bình" else "🔴"
                st.text(f"{color} {risk}: {count} ({percentage:.0f}%)")
    
    @staticmethod
    def display_ai_recommendations(ai_recommendations):
        """Hiển thị khuyến nghị chiến lược chi tiết với format giống phân tích doanh thu"""
        if not ai_recommendations or len(ai_recommendations) == 0:
            st.warning("⚠️ Không có khuyến nghị chiến lược")
            return
        
        st.markdown("## 🤖 Khuyến Nghị Chiến Lược")
        st.markdown("*Phân tích thông minh và đề xuất chiến lược đầu tư tối ưu*")
        
        for recommendation in ai_recommendations:
            # Hiển thị khuyến nghị chính
            st.markdown("### 📊 Phân Tích Tổng Quan")
            st.write(recommendation['content'])
            
            st.markdown("---")
            
            # Hiển thị gợi ý đầu tư với expander giống bên phân tích doanh thu
            with st.expander("💰 GỢI Ý ĐẦU TƯ", expanded=False):
                st.write(recommendation['investment_suggestion'])
            
            # Hiển thị dự báo với expander
            with st.expander("📈 DỰ BÁO HIỆU QUẢ", expanded=False):
                st.write(recommendation['forecast'])
                
                # Thêm metrics cho dự báo (giống như bên phân tích doanh thu)
                col1, col2 = st.columns(2)
                
                # Parse ROI numbers từ content để hiển thị metrics
                content = recommendation['forecast']
                try:
                    # Extract ROI values từ text
                    import re
                    roi_matches = re.findall(r'(\d+\.?\d*)%', content)
                    if len(roi_matches) >= 2:
                        base_roi = float(roi_matches[0])
                        enhanced_roi = float(roi_matches[1])
                        
                        with col1:
                            st.metric(
                                label="Giữ nguyên chiến lược",
                                value=f"{base_roi:.1f}%",
                                delta=f"{base_roi:.1f}% ROI dự kiến"
                            )
                        with col2:
                            st.metric(
                                label="Tăng cường đầu tư 20%",
                                value=f"{enhanced_roi:.1f}%",
                                delta=f"{enhanced_roi - base_roi:+.1f}% so với hiện tại"
                            )
                except:
                    # Fallback nếu không parse được
                    with col1:
                        st.info("📊 **Chiến lược hiện tại**\nDuy trì phân bổ theo khuyến nghị")
                    with col2:
                        st.info("🚀 **Chiến lược tăng cường**\nTăng đầu tư vào top markets")
    
    @staticmethod
    def display_download_section(allocation_df, time_frame_months, ai_recommendations):
        """Hiển thị section download kết quả"""
        st.markdown("## 💾 Tải Kết Quả")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            analysis_csv = allocation_df.to_csv(index=False)
            st.download_button(
                "📊 Tải Phân Tích Chi Tiết (CSV)",
                analysis_csv,
                f"country_analysis_{time_frame_months}months_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv"
            )
        
        with col2:
            budget_allocation_csv = allocation_df[['Country', 'Allocated_Budget', 'Investment_Percentage', 
                                                 'Expected_Profit', 'Investment_Level']].to_csv(index=False)
            st.download_button(
                "💰 Tải Phân Bổ Ngân Sách (CSV)",
                budget_allocation_csv,
                f"budget_allocation_{time_frame_months}months_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv"
            )
        
        with col3:
            summary_data = []
            for _, row in allocation_df.iterrows():
                summary_data.append({
                    'Country': row['Country'],
                    'Investment_Level': row['Investment_Level'],
                    'Budget': row['Allocated_Budget'],
                    'Expected_Profit': row['Expected_Profit'],
                    'Risk_Level': row['Risk_Level'],
                    'Analysis_Period': f"{time_frame_months} months"
                })
            
            summary_df = pd.DataFrame(summary_data)
            
            if ai_recommendations:
                ai_rec_text = "\n\n".join([f"{rec['title']}: {rec['content']}" for rec in ai_recommendations])
                summary_df['AI_Recommendations'] = ai_rec_text
            
            summary_csv = summary_df.to_csv(index=False)
            st.download_button(
                "📋 Tải Tóm Tắt Khuyến Nghị (CSV)",
                summary_csv,
                f"investment_recommendations_{time_frame_months}months_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv"
            )

    @staticmethod
    def _parse_ai_content(content):
        """Parse nội dung AI thành các phần riêng biệt"""
        sections = {}
        
        # Chia content thành các phần dựa trên keyword
        if "PORTFOLIO" in content.upper() or "portfolio" in content.lower():
            portfolio_start = content.lower().find("portfolio")
            portfolio_end = content.lower().find("strategy", portfolio_start)
            if portfolio_end == -1:
                portfolio_end = len(content)
            sections["portfolio"] = content[portfolio_start:portfolio_end].strip()
        
        if "STRATEGY" in content.upper() or "chiến lược" in content.lower():
            strategy_start = max(content.lower().find("strategy"), content.lower().find("chiến lược"))
            strategy_end = content.lower().find("result", strategy_start)
            if strategy_end == -1:
                strategy_end = content.lower().find("kết quả", strategy_start)
            if strategy_end == -1:
                strategy_end = len(content)
            sections["strategy"] = content[strategy_start:strategy_end].strip()
        
        if "RESULT" in content.upper() or "kết quả" in content.lower():
            results_start = max(content.lower().find("result"), content.lower().find("kết quả"))
            sections["results"] = content[results_start:].strip()
        
        # Nếu không tìm thấy section nào, return toàn bộ content
        if not sections:
            sections["strategy"] = content
            
        return sections
    
    @staticmethod
    def _extract_strategy_summary(strategy_content):
        """Trích xuất tóm tắt chiến lược chính"""
        lines = strategy_content.split('\n')
        summary_lines = []
        
        for line in lines[:5]:  # Lấy 5 dòng đầu
            if line.strip() and len(line.strip()) > 10:
                summary_lines.append(line.strip())
        
        return '\n'.join(summary_lines[:3])  # Lấy tối đa 3 dòng
    
    @staticmethod
    def _extract_key_metrics(results_content):
        """Trích xuất các metrics chính từ kết quả"""
        metrics = {}
        
        # Tìm các patterns phổ biến
        lines = results_content.lower().split('\n')
        
        for line in lines:
            if 'revenue' in line or 'doanh thu' in line:
                if '%' in line:
                    import re
                    numbers = re.findall(r'\d+\.?\d*', line)
                    if numbers:
                        metrics['revenue_increase'] = f"{numbers[0]}%"
                        if len(numbers) > 1:
                            metrics['revenue_delta'] = f"+{numbers[1]}%"
            
            if 'roi' in line:
                import re
                numbers = re.findall(r'\d+\.?\d*', line)
                if numbers:
                    metrics['roi_expected'] = f"{numbers[0]}%"
            
            if 'order' in line or 'đơn hàng' in line:
                import re
                numbers = re.findall(r'\d+\.?\d*', line)
                if numbers:
                    metrics['orders_increase'] = f"{numbers[0]}%"
            
            if 'break-even' in line or 'hòa vốn' in line:
                import re
                numbers = re.findall(r'\d+', line)
                if numbers:
                    metrics['breakeven_time'] = f"{numbers[0]} tháng"
        
        # Default values nếu không tìm thấy
        if not metrics:
            metrics = {
                'revenue_increase': '15-25%',
                'roi_expected': '150%',
                'orders_increase': '10-20%',
                'breakeven_time': '6-8 tháng'
            }
        
        return metrics
    
    @staticmethod
    def _extract_results_detail(results_content):
        """Trích xuất chi tiết kết quả cụ thể"""
        lines = results_content.split('\n')
        detail_lines = []
        
        # Lọc các dòng có thông tin chi tiết
        for line in lines:
            if line.strip() and (
                'tăng' in line.lower() or 'increase' in line.lower() or 
                'roi' in line.lower() or 'profit' in line.lower() or
                '%' in line or '$' in line or '£' in line
            ):
                detail_lines.append(line.strip())
        
        if not detail_lines:
            detail_lines = [
                "• Dự kiến tăng doanh thu 15-25% trong 6 tháng đầu",
                "• ROI trung bình 150% trong năm đầu tiên", 
                "• Tăng số đơn hàng 10-20% từ tháng thứ 3",
                "• Break-even dự kiến sau 6-8 tháng đầu tư"
            ]
        
        return '\n'.join(detail_lines[:8])  # Lấy tối đa 8 dòng
    
    @staticmethod
    def _extract_improvement_analysis(results_content):
        """Trích xuất phân tích cải thiện"""
        lines = results_content.split('\n')
        improvement_lines = []
        
        # Tìm các dòng về cải thiện, tối ưu
        for line in lines:
            if line.strip() and (
                'cải thiện' in line.lower() or 'improvement' in line.lower() or
                'tối ưu' in line.lower() or 'optimize' in line.lower() or
                'nâng cao' in line.lower() or 'enhance' in line.lower()
            ):
                improvement_lines.append(line.strip())
        
        if not improvement_lines:
            improvement_lines = [
                "• Tối ưu hóa channel marketing hiệu quả nhất cho từng quốc gia",
                "• Cải thiện conversion rate thông qua personalization",
                "• Nâng cao customer lifetime value thông qua retention strategy",
                "• Tối ưu budget allocation dựa trên real-time performance"
            ]
        
        return '\n'.join(improvement_lines[:6])
    
    @staticmethod
    def _extract_logic_explanation(results_content):
        """Trích xuất logic giải thích cách đạt kết quả"""
        lines = results_content.split('\n')
        logic_lines = []
        
        # Tìm các dòng giải thích logic, lý do
        for line in lines:
            if line.strip() and (
                'vì' in line.lower() or 'because' in line.lower() or
                'do' in line.lower() or 'due to' in line.lower() or
                'dựa trên' in line.lower() or 'based on' in line.lower() or
                'nhờ' in line.lower() or 'thanks to' in line.lower()
            ):
                logic_lines.append(line.strip())
        
        if not logic_lines:
            logic_lines = [
                "• Dựa trên phân tích historical data và trend patterns",
                "• Áp dụng mô hình 30-10-60 đã được validate trong industry",
                "• Tận dụng seasonal patterns và country-specific behaviors",
                "• Sử dụng predictive analytics cho resource allocation",
                "• Kết hợp market intelligence với performance metrics",
                "• Optimized cho risk-adjusted returns"
            ]
        
        return '\n'.join(logic_lines[:6])

class MainPanelComponents:
    """Class chứa các component cho main panel (thay thế sidebar)"""
    
    @staticmethod
    def display_time_frame_selector():
        """Hiển thị selector cho khung thời gian trong main panel"""
        st.markdown("""
        <div class="config-section">
            <h3>📅 Cấu Hình Thời Gian</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            time_frame = st.selectbox(
                "Khung thời gian phân tích:",
                [3, 6, 9, 12, 18, 24],
                index=1,
                format_func=lambda x: f"{x} tháng gần nhất",
                help="Hệ thống sẽ phân tích dữ liệu trong khoảng thời gian này"
            )
            
            st.info(f"📊 Phân tích dữ liệu trong {time_frame} tháng gần nhất")
            
        return time_frame
    
    @staticmethod
    def display_exclusion_lists(available_countries):
        """Hiển thị danh sách loại trừ trong main panel"""
        st.markdown("""
        <div class="config-section">
            <h3>🚫 Danh Sách Loại Trừ</h3>
            <p>Chọn các quốc gia hoặc sản phẩm không muốn đưa vào phân tích</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🌍 Quốc gia loại trừ:**")
            excluded_countries = st.multiselect(
                "Chọn quốc gia:",
                available_countries,
                help="Các quốc gia này sẽ bị loại khỏi phân tích và phân bổ ngân sách"
            )
            
            if excluded_countries:
                st.warning(f"⚠️ Sẽ loại trừ {len(excluded_countries)} quốc gia")
        
        with col2:
            st.markdown("**📦 Sản phẩm loại trừ:**")
            excluded_products_input = st.text_area(
                "Mã sản phẩm (mỗi dòng một mã):",
                help="Nhập mã sản phẩm không muốn phân tích, mỗi dòng một mã",
                height=100,
                placeholder="Ví dụ:\nPOST\nDOT\nCRUK"
            )
            excluded_products = [p.strip() for p in excluded_products_input.split('\n') if p.strip()]
            
            if excluded_products:
                st.warning(f"⚠️ Sẽ loại trừ {len(excluded_products)} sản phẩm")
        
        return excluded_countries, excluded_products
    
    @staticmethod
    def display_country_selection():
        """Hiển thị lựa chọn quốc gia trong main panel"""
        st.markdown("### 🌍 Tiêu Chí Lựa Chọn Quốc Gia")
        
        col1, col2 = st.columns(2)
        
        with col1:
            country_criteria = st.selectbox(
                "Tiêu chí lựa chọn:",
                [
                    "Doanh thu cao nhất",
                    "Nhiều đơn hàng nhất", 
                    "Nhiều khách hàng nhất",
                    "ROI tiềm năng cao nhất",
                    "Tăng trưởng ổn định"
                ],
                help="Cách thức lựa chọn quốc gia để phân bổ ngân sách"
            )
        
        with col2:
            num_countries = st.number_input(
                "Số lượng quốc gia:",
                min_value=1,
                max_value=20,
                value=5,
                help="Số quốc gia sẽ được chọn để phân bổ ngân sách"
            )
        
        return country_criteria, num_countries
    
    @staticmethod
    def display_budget_parameters():
        """Hiển thị tham số ngân sách trong main panel"""
        st.markdown("### 💰 Tham Số Ngân Sách")
        
        col1, col2 = st.columns(2)
        
        with col1:
            total_budget = st.number_input(
                "Tổng ngân sách ($):",
                min_value=1000,
                max_value=10000000,
                value=100000,
                step=5000,
                help="Tổng ngân sách marketing có thể phân bổ"
            )
        
        with col2:
            expected_roi = st.number_input(
                "ROI mong muốn (%):",
                min_value=5.0,
                max_value=500.0,
                value=150.0,
                step=5.0,
                help="Tỷ suất lợi nhuận mong muốn trên đầu tư"
            )
        
        return total_budget, expected_roi
    
    @staticmethod
    def display_budget_constraints(total_budget, num_countries):
        """Hiển thị ràng buộc ngân sách trong main panel"""
        st.markdown("### ⚖️ Ràng Buộc Phân Bổ")
        
        col1, col2 = st.columns(2)
        
        with col1:
            min_per_country = st.number_input(
                "Ngân sách tối thiểu mỗi quốc gia ($):",
                min_value=100,
                max_value=total_budget // num_countries,
                value=min(5000, total_budget // num_countries),
                step=1000,
                help="Số tiền tối thiểu phải phân bổ cho mỗi quốc gia"
            )
        
        with col2:
            max_per_country = st.number_input(
                "Ngân sách tối đa mỗi quốc gia ($):",
                min_value=min_per_country,
                max_value=total_budget,
                value=min(50000, total_budget // 2),
                step=5000,
                help="Số tiền tối đa có thể phân bổ cho một quốc gia"
            )
        
        return min_per_country, max_per_country
    
    @staticmethod
    def display_analyze_button():
        """Hiển thị nút phân tích trong main panel"""
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            disabled = 'uploaded_data_path' not in st.session_state or not st.session_state['uploaded_data_path']
            return st.button(
                "🚀 Bắt Đầu Phân Tích",
                use_container_width=True,
                type="primary",
                help="Click để bắt đầu quá trình phân tích và phân bổ ngân sách",
                disabled=disabled
            )