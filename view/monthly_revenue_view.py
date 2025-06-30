"""
View cho chức năng phân tích doanh thu theo tháng
"""

import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

class MonthlyRevenueView:
    def __init__(self):
        pass
    
    def display_header(self):
        """Hiển thị header của ứng dụng"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 15px; margin-bottom: 2rem; color: white; text-align: center;">
            <h1>📅 Phân Tích Doanh Thu Theo Tháng</h1>
            <p>Phân tích xu hướng doanh thu theo từng tháng và tìm ra các giai đoạn then chốt</p>
        </div>
        """, unsafe_allow_html=True)
    
    def display_product_selection(self, product_list):
        """Hiển thị dropdown chọn sản phẩm"""
        product = st.selectbox(
            "🛒 Chọn sản phẩm để phân tích",
            product_list,
            index=None,
            placeholder="Nhập tên sản phẩm để tìm kiếm...",
            help="Chọn sản phẩm cụ thể để phân tích doanh thu theo tháng"
        )
        return product
    
    def display_date_selection(self, min_date, max_date):
        """Hiển thị date picker"""
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input(
                "📅 Ngày bắt đầu phân tích", 
                min_value=min_date, 
                max_value=max_date, 
                value=min_date
            )
        
        with col2:
            end_date = st.date_input(
                "📅 Ngày kết thúc phân tích", 
                min_value=min_date, 
                max_value=max_date, 
                value=max_date
            )
        
        return start_date, end_date
    
    def plot_monthly_revenue_matplotlib(self, monthly_revenue):
        """Vẽ biểu đồ doanh thu theo tháng bằng matplotlib"""
        plt.figure(figsize=(12, 6))
        bars = plt.bar(monthly_revenue['Month'], monthly_revenue['Revenue'], color='skyblue')
        plt.xlabel('Tháng', fontsize=14)
        plt.ylabel('Doanh thu', fontsize=14)
        plt.title('Doanh thu theo từng tháng', fontsize=16, fontweight='bold')
        plt.xticks(monthly_revenue['Month'])
        
        # Ghi số doanh thu trên đầu mỗi cột
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval, f"{yval:,.0f}", 
                    ha='center', va='bottom', fontsize=12, color='black')
        
        plt.tight_layout()
        st.pyplot(plt)
    
    def plot_monthly_revenue_plotly(self, monthly_revenue):
        """Vẽ biểu đồ doanh thu theo tháng bằng plotly (interactive)"""
        fig = go.Figure()
        
        # Thêm bar chart
        fig.add_trace(go.Bar(
            x=monthly_revenue['Month'],
            y=monthly_revenue['Revenue'],
            name='Doanh thu',
            marker_color='rgba(102, 126, 234, 0.8)',
            text=[f"{val:,.0f}" for val in monthly_revenue['Revenue']],
            textposition='outside',
            hovertemplate='<b>Tháng %{x}</b><br>Doanh thu: %{y:,.0f}<extra></extra>'
        ))
        
        # Thêm đường xu hướng
        fig.add_trace(go.Scatter(
            x=monthly_revenue['Month'],
            y=monthly_revenue['Revenue'],
            mode='lines+markers',
            name='Xu hướng',
            line=dict(color='red', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title={
                'text': 'Doanh thu theo từng tháng',
                'x': 0.5,
                'font': {'size': 20}
            },
            xaxis_title='Tháng',
            yaxis_title='Doanh thu',
            hovermode='x unified',
            height=500,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def display_special_months(self, peak_month, low_month, max_var_month, stable_months):
        """Hiển thị các tháng đặc biệt"""
        st.markdown("### 🌟 Các tháng đặc biệt")
        
        # Tạo số cột dựa trên số tháng đặc biệt
        num_cols = 4
        cols = st.columns(num_cols)
        
        # Tháng cao điểm
        with cols[0]:
            if st.button(f"🔥 Tháng cao điểm: {int(peak_month['Month'])}", key="peak"):
                st.info(
                    "🔥 Tháng này ghi nhận doanh thu đạt mức cao nhất trong năm, cho thấy nhu cầu thị trường tăng mạnh, có thể nhờ các dịp lễ hội hoặc chương trình ưu đãi trước đó. "
                    "Doanh nghiệp cần tận dụng thời điểm này bằng cách đẩy mạnh các hoạt động marketing phủ rộng, tăng cường khuyến mãi hấp dẫn, kết hợp quảng bá đa kênh và đảm bảo nguồn hàng dồi dào. "
                    "Đây là giai đoạn lý tưởng để gia tăng thị phần và tối đa hóa doanh thu."
                )
        
        # Tháng thấp điểm
        with cols[1]:
            if st.button(f"❄️ Tháng thấp điểm: {int(low_month['Month'])}", key="low"):
                st.info(
                    "❄️ Tháng này có doanh thu tụt xuống mức thấp nhất, phản ánh nhu cầu mua sắm suy giảm, có thể do ảnh hưởng mùa vụ hoặc thói quen tiêu dùng. "
                    "Để kích cầu, doanh nghiệp nên triển khai các chương trình ưu đãi nhẹ như giảm giá theo khung giờ vàng, tặng quà kèm đơn hàng hoặc kết hợp sản phẩm thành các combo ưu đãi. "
                    "Đồng thời, nên đẩy mạnh truyền thông nhằm thu hút sự chú ý và tạo cảm giác khẩn cấp cho khách hàng."
                )
        
        # Tháng biến động mạnh nhất
        with cols[2]:
            if max_var_month is not None:
                if st.button(f"⚡ Biến động mạnh: {max_var_month}", key="strong_var"):
                    st.info(
                        "⚡ Tháng này ghi nhận sự biến động doanh thu đột ngột so với tháng trước, có thể là sự tăng vọt bất ngờ hoặc sụt giảm đáng lo ngại. "
                        "Nếu doanh thu tăng mạnh, đây là tín hiệu tích cực cần được tận dụng ngay bằng việc gia tăng sản xuất, mở rộng quảng cáo và triển khai các chương trình tri ân khách hàng. "
                        "Ngược lại, nếu doanh thu giảm sâu, doanh nghiệp cần nhanh chóng phân tích nguyên nhân và tung ra các chiến dịch kích cầu khẩn cấp như flash sale ngắn ngày hoặc ưu đãi sốc nhằm kìm hãm đà giảm và ổn định lại thị trường."
                    )
            else:
                st.write("Không có tháng biến động mạnh.")
        
        # Các tháng ổn định
        with cols[3]:
            if stable_months:
                stable_month_str = ', '.join(map(str, stable_months[:3]))  # Chỉ hiển thị 3 tháng đầu
                if st.button(f"✅ Ổn định: {stable_month_str}{'...' if len(stable_months) > 3 else ''}", key="stable_months"):
                    st.info(
                        "✅ Doanh thu trong tháng duy trì ở mức ổn định, không có biến động lớn, cho thấy thị trường đang phát triển theo xu hướng đều đặn. "
                        "Trong bối cảnh này, doanh nghiệp nên tập trung duy trì chất lượng sản phẩm, dịch vụ và thử nghiệm các chiến dịch marketing nhỏ nhằm thăm dò thị trường hoặc cải thiện trải nghiệm khách hàng. "
                        "Đây cũng là thời điểm phù hợp để tối ưu chi phí quảng cáo và chuẩn bị cho các giai đoạn cao điểm tiếp theo."
                    )
            else:
                st.write("Không có tháng ổn định.")
    
    def display_trend_analysis(self, trend_analysis):
        """Hiển thị phân tích xu hướng"""
        st.markdown("### 📉 Phân tích xu hướng")
        
        for paragraph in trend_analysis:
            st.write(paragraph)
    
    def display_decision_suggestions(self, peak_month, low_month, max_var_month, stable_months):
        """Hiển thị gợi ý quyết định"""
        st.markdown("### 💡 Gợi ý quyết định")
        
        # Tháng cao điểm
        st.markdown("**🔥 Tháng cao điểm:** Tháng {}<br>{}".format(
            int(peak_month['Month']),
            "Tháng này ghi nhận doanh thu đạt mức cao nhất trong năm, cho thấy nhu cầu thị trường tăng mạnh, có thể nhờ các dịp lễ hội hoặc chương trình ưu đãi trước đó. "
            "Doanh nghiệp cần tận dụng thời điểm này bằng cách đẩy mạnh các hoạt động marketing phủ rộng, tăng cường khuyến mãi hấp dẫn, kết hợp quảng bá đa kênh và đảm bảo nguồn hàng dồi dào. "
            "Đây là giai đoạn lý tưởng để gia tăng thị phần và tối đa hóa doanh thu."
        ), unsafe_allow_html=True)
        
        # Tháng thấp điểm
        st.markdown("**❄️ Tháng thấp điểm:** Tháng {}<br>{}".format(
            int(low_month['Month']),
            "Tháng này có doanh thu tụt xuống mức thấp nhất, phản ánh nhu cầu mua sắm suy giảm, có thể do ảnh hưởng mùa vụ hoặc thói quen tiêu dùng. "
            "Để kích cầu, doanh nghiệp nên triển khai các chương trình ưu đãi nhẹ như giảm giá theo khung giờ vàng, tặng quà kèm đơn hàng hoặc kết hợp sản phẩm thành các combo ưu đãi. "
            "Đồng thời, nên đẩy mạnh truyền thông nhằm thu hút sự chú ý và tạo cảm giác khẩn cấp cho khách hàng."
        ), unsafe_allow_html=True)
        
        # Tháng biến động mạnh
        if max_var_month is not None:
            st.markdown("**⚡ Tháng biến động mạnh:** Tháng {}<br>{}".format(
                max_var_month,
                "Tháng này ghi nhận sự biến động doanh thu đột ngột so với tháng trước, có thể là sự tăng vọt bất ngờ hoặc sụt giảm đáng lo ngại. "
                "Nếu doanh thu tăng mạnh, đây là tín hiệu tích cực cần được tận dụng ngay bằng việc gia tăng sản xuất, mở rộng quảng cáo và triển khai các chương trình tri ân khách hàng. "
                "Ngược lại, nếu doanh thu giảm sâu, doanh nghiệp cần nhanh chóng phân tích nguyên nhân và tung ra các chiến dịch kích cầu khẩn cấp như flash sale ngắn ngày hoặc ưu đãi sốc nhằm kìm hãm đà giảm và ổn định lại thị trường."
            ), unsafe_allow_html=True)
        else:
            st.markdown("**⚡ Tháng biến động mạnh:** Không có tháng biến động mạnh.", unsafe_allow_html=True)
        
        # Tháng ổn định
        if stable_months:
            st.markdown("**✅ Tháng ổn định:** Tháng {}<br>{}".format(
                ', '.join(str(sm) for sm in stable_months),
                "Doanh thu trong tháng duy trì ở mức ổn định, không có biến động lớn, cho thấy thị trường đang phát triển theo xu hướng đều đặn. "
                "Trong bối cảnh này, doanh nghiệp nên tập trung duy trì chất lượng sản phẩm, dịch vụ và thử nghiệm các chiến dịch marketing nhỏ nhằm thăm dò thị trường hoặc cải thiện trải nghiệm khách hàng. "
                "Đây cũng là thời điểm phù hợp để tối ưu chi phí quảng cáo và chuẩn bị cho các giai đoạn cao điểm tiếp theo."
            ), unsafe_allow_html=True)
        else:
            st.markdown("**✅ Tháng ổn định:** Không có tháng ổn định.", unsafe_allow_html=True)
    
    def display_no_data_warning(self):
        """Hiển thị cảnh báo không có dữ liệu"""
        st.warning("⚠️ Không có dữ liệu cho lựa chọn này.")
    
    def display_upload_prompt(self):
        """Hiển thị thông báo upload file"""
        st.info("👆 Vui lòng chọn file CSV để bắt đầu phân tích doanh thu theo tháng!")
    
    def display_error(self, error_message):
        """Hiển thị lỗi"""
        st.error(f"❌ Lỗi: {error_message}")
    
    def display_success(self, message):
        """Hiển thị thông báo thành công"""
        st.success(f"✅ {message}")
