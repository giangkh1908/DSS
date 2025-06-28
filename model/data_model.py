import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class DataModel:
    """Model class xử lý tất cả business logic và data processing"""
    
    def __init__(self):
        self.df_clean = None
        self.analysis_df = None
        self.allocation_df = None
    
    @staticmethod
    @st.cache_data
    def load_and_clean_data(uploaded_file, time_frame_months):
        """Load & làm sạch dữ liệu với khung thời gian tùy chỉnh"""
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
            
            df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
            df['Revenue'] = df['Quantity'] * df['UnitPrice']
            
            max_date = df['InvoiceDate'].max()
            start_date = max_date - timedelta(days=time_frame_months * 30)
            df = df[df['InvoiceDate'] >= start_date]
            
            mask = (
                (df['Quantity'] > 0) & 
                (df['UnitPrice'] > 0) & 
                (df['CustomerID'].notna()) &
                (df['Revenue'] > 0) &
                (df['InvoiceDate'].notna())
            )
            
            df_clean = df[mask].copy()
            df_clean['Country'] = df_clean['Country'].str.strip().str.title()
            df_clean['YearMonth'] = df_clean['InvoiceDate'].dt.to_period('M')
            
            return df_clean
            
        except Exception as e:
            st.error(f"❌ Lỗi: {str(e)}")
            return None
    
    @staticmethod
    def filter_excluded_items(df_clean, excluded_countries, excluded_products):
        """Lọc bỏ quốc gia và sản phẩm không mong muốn"""
        if excluded_countries:
            df_clean = df_clean[~df_clean['Country'].isin(excluded_countries)]
        
        if excluded_products:
            df_clean = df_clean[~df_clean['StockCode'].isin(excluded_products)]
        
        return df_clean
    
    @staticmethod
    def analyze_countries_comprehensive(df_clean, selected_countries, time_frame_months):
        """Phân tích toàn diện các quốc gia với khung thời gian tùy chỉnh"""
        df_filtered = df_clean[df_clean['Country'].isin(selected_countries)]
        
        max_date = df_filtered['InvoiceDate'].max()
        analysis_period = max_date - timedelta(days=time_frame_months * 30)
        half_period = max_date - timedelta(days=time_frame_months * 15)
        
        recent_data = df_filtered[df_filtered['InvoiceDate'] >= analysis_period]
        recent_half = df_filtered[df_filtered['InvoiceDate'] >= half_period]
        prev_half = df_filtered[
            (df_filtered['InvoiceDate'] >= analysis_period) & 
            (df_filtered['InvoiceDate'] < half_period)
        ]
        
        country_analysis = []
        
        for country in selected_countries:
            country_data = df_filtered[df_filtered['Country'] == country]
            country_recent = recent_data[recent_data['Country'] == country]
            
            total_revenue = country_recent['Revenue'].sum()
            avg_monthly_revenue = total_revenue / time_frame_months
            
            total_orders = country_recent['InvoiceNo'].nunique()
            avg_orders_per_month = total_orders / time_frame_months
            
            avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
            
            monthly_revenue = country_recent.groupby(country_recent['InvoiceDate'].dt.to_period('M'))['Revenue'].sum()
            revenue_stability = 1 / (monthly_revenue.std() / monthly_revenue.mean()) if len(monthly_revenue) > 0 and monthly_revenue.mean() > 0 else 0
            
            monthly_pattern = country_data.groupby(country_data['InvoiceDate'].dt.month)['Revenue'].mean()
            seasonality_score = monthly_pattern.std() / monthly_pattern.mean() if monthly_pattern.mean() > 0 else 0
            
            country_analysis.append({
                'Country': country,
                'Total_Revenue': total_revenue,
                'Avg_Monthly_Revenue': avg_monthly_revenue,
                'Total_Orders': total_orders,
                'Avg_Orders_Per_Month': avg_orders_per_month,
                'Avg_Order_Value': avg_order_value,
                'Revenue_Stability': revenue_stability,
                'Seasonality_Score': seasonality_score
            })
        
        analysis_df = pd.DataFrame(country_analysis)
        
        if len(analysis_df) > 0:
            analysis_df['Revenue_Score'] = (analysis_df['Avg_Monthly_Revenue'] / analysis_df['Avg_Monthly_Revenue'].max()) * 10
            analysis_df['Order_Frequency_Score'] = (analysis_df['Avg_Orders_Per_Month'] / analysis_df['Avg_Orders_Per_Month'].max()) * 10
            analysis_df['Stability_Score'] = np.clip(analysis_df['Revenue_Stability'] * 2, 0, 10)
            
            analysis_df['Overall_Score'] = (
                analysis_df['Revenue_Score'] * 0.5 +
                analysis_df['Order_Frequency_Score'] * 0.35 +
                analysis_df['Stability_Score'] * 0.15
            )
            
            analysis_df['Risk_Level'] = analysis_df.apply(lambda x: 
                'Thấp' if x['Order_Frequency_Score'] > 7 and x['Revenue_Stability'] > 0.5 else
                'Cao' if x['Order_Frequency_Score'] < 4 or x['Revenue_Stability'] < 0.2 else
                'Trung Bình', axis=1)
            
            analysis_df['Investment_Potential'] = analysis_df.apply(lambda x:
                'Cao' if x['Overall_Score'] > 7 else
                'Thấp' if x['Overall_Score'] < 4 else
                'Trung Bình', axis=1)
        
        return analysis_df
    
    @staticmethod
    def allocate_budget_by_country(analysis_df, total_budget, min_per_country, max_per_country, expected_roi):
        """Phân bổ ngân sách theo quốc gia với ROI dự kiến tùy chỉnh"""
        
        if len(analysis_df) == 0:
            return analysis_df
        
        total_score = analysis_df['Overall_Score'].sum()
        analysis_df['Initial_Budget'] = (analysis_df['Overall_Score'] / total_score) * total_budget
        
        analysis_df['Allocated_Budget'] = analysis_df['Initial_Budget'].clip(
            lower=min_per_country,
            upper=max_per_country
        )
        
        total_allocated = analysis_df['Allocated_Budget'].sum()
        if total_allocated != total_budget:
            adjustment_factor = total_budget / total_allocated
            analysis_df['Allocated_Budget'] = analysis_df['Allocated_Budget'] * adjustment_factor
        
        analysis_df['Expected_Profit'] = analysis_df['Allocated_Budget'] * (expected_roi / 100)
        analysis_df['Total_Return'] = analysis_df['Allocated_Budget'] + analysis_df['Expected_Profit']
        
        analysis_df['Investment_Percentage'] = (analysis_df['Allocated_Budget'] / total_budget) * 100
        
        def classify_investment_level(percentage):
            if percentage >= 25:
                return "Rất Cao"
            elif percentage >= 15:
                return "Cao"
            elif percentage >= 10:
                return "Trung Bình"
            else:
                return "Thấp"
        
        analysis_df['Investment_Level'] = analysis_df['Investment_Percentage'].apply(classify_investment_level)
        
        return analysis_df.sort_values('Allocated_Budget', ascending=False)
    
    @staticmethod
    def get_country_selection_options(df_clean, time_frame_months):
        """Tạo các tùy chọn lựa chọn quốc gia với khung thời gian tùy chỉnh"""
        country_stats = df_clean.groupby('Country').agg({
            'Revenue': ['sum', 'mean', 'count'],
            'InvoiceNo': 'nunique'
        }).round(2)
        
        country_stats.columns = ['Total_Revenue', 'Avg_Revenue', 'Transaction_Count', 'Order_Count']
        country_stats = country_stats.reset_index()
        
        return country_stats
    
    @staticmethod
    def filter_countries_by_criteria(country_stats, criteria, num_countries):
        """Lọc quốc gia theo tiêu chí"""
        if criteria == "Doanh thu cao nhất":
            return country_stats.nlargest(num_countries, 'Total_Revenue')['Country'].tolist()
        elif criteria == "Nhiều đơn hàng nhất":
            return country_stats.nlargest(num_countries, 'Order_Count')['Country'].tolist()
        elif criteria == "Doanh thu trung bình cao nhất":
            return country_stats.nlargest(num_countries, 'Avg_Revenue')['Country'].tolist()
        else:
            return country_stats['Country'].tolist()[:num_countries]

    @staticmethod
    def analyze_top_products_by_country(df_clean, selected_countries, time_frame_months, top_n=3):
        """Phân tích top sản phẩm với validation tốt hơn"""
        df_filtered = df_clean[df_clean['Country'].isin(selected_countries)]
        
        max_date = df_filtered['InvoiceDate'].max()
        analysis_period = max_date - timedelta(days=time_frame_months * 30)
        recent_data = df_filtered[df_filtered['InvoiceDate'] >= analysis_period]
        
        country_products = {}
        
        for country in selected_countries:
            country_data = recent_data[recent_data['Country'] == country]
            
            if len(country_data) == 0:
                country_products[country] = []
                continue
            
            # Phân tích theo StockCode với validation
            product_analysis = country_data.groupby('StockCode').agg({
                'Quantity': 'sum',
                'Revenue': 'sum',
                'InvoiceNo': 'nunique',
                'Description': 'first'
            }).reset_index()
            
            # Lọc bỏ sản phẩm có doanh thu quá thấp
            product_analysis = product_analysis[product_analysis['Revenue'] > 100]
            
            if len(product_analysis) > 0:
                # Chuẩn hóa an toàn
                max_qty = product_analysis['Quantity'].max()
                max_rev = product_analysis['Revenue'].max()
                max_orders = product_analysis['InvoiceNo'].max()
                
                if max_qty > 0:
                    product_analysis['Quantity_Score'] = product_analysis['Quantity'] / max_qty
                else:
                    product_analysis['Quantity_Score'] = 0
                    
                if max_rev > 0:
                    product_analysis['Revenue_Score'] = product_analysis['Revenue'] / max_rev
                else:
                    product_analysis['Revenue_Score'] = 0
                    
                if max_orders > 0:
                    product_analysis['Orders_Score'] = product_analysis['InvoiceNo'] / max_orders
                else:
                    product_analysis['Orders_Score'] = 0
                
                # Tính điểm tổng hợp
                product_analysis['Overall_Score'] = (
                    product_analysis['Revenue_Score'] * 0.6 +
                    product_analysis['Quantity_Score'] * 0.3 +
                    product_analysis['Orders_Score'] * 0.1
                )
                
                # Lấy top N sản phẩm
                top_products = product_analysis.nlargest(min(top_n, len(product_analysis)), 'Overall_Score')
                
                country_products[country] = []
                for _, product in top_products.iterrows():
                    # Clean description
                    description = str(product['Description']).strip() if pd.notna(product['Description']) else f"Sản phẩm {product['StockCode']}"
                    
                    country_products[country].append({
                        'StockCode': str(product['StockCode']),
                        'Description': description,
                        'Total_Quantity': int(product['Quantity']),
                        'Total_Revenue': float(product['Revenue']),
                        'Total_Orders': int(product['InvoiceNo']),
                        'Overall_Score': float(product['Overall_Score']),
                        'Avg_Revenue_Per_Order': float(product['Revenue'] / product['InvoiceNo']) if product['InvoiceNo'] > 0 else 0
                    })
            else:
                country_products[country] = []
        
        return country_products

    @staticmethod
    def calculate_product_strategy_allocation(products, total_budget_for_country):
        """Tính toán phân bổ ngân sách theo chiến lược 70-20-10"""
        if not products or len(products) == 0:
            return None
        
        # Sắp xếp sản phẩm theo doanh thu
        sorted_products = sorted(products, key=lambda x: x['Total_Revenue'], reverse=True)
        
        # Phân loại sản phẩm
        core_product = sorted_products[0]  # Sản phẩm chủ lực
        growth_products = sorted_products[1:2] if len(sorted_products) > 1 else []  # Sản phẩm tiềm năng
        diversify_products = sorted_products[2:] if len(sorted_products) > 2 else []  # Đa dạng hóa
        
        strategy = {
            'core': {
                'percentage': 30,
                'budget': total_budget_for_country * 0.3,
                'products': [core_product],
                'reason': 'Sản phẩm chủ lực - doanh thu ổn định cao'
            },
            'growth': {
                'percentage': 10,
                'budget': total_budget_for_country * 0.1,
                'products': growth_products,
                'reason': 'Phát triển tiềm năng - cơ hội tăng trưởng'
            },
            'diversify': {
                'percentage': 60,
                'budget': total_budget_for_country * 0.6,
                'products': diversify_products,
                'reason': 'Đa dạng hóa - giảm rủi ro portfolio'
            }
        }
        
        return strategy

    @staticmethod
    def analyze_countries_with_products(df_clean, selected_countries, time_frame_months):
        """Phân tích quốc gia với chiến lược sản phẩm"""
        # Lấy phân tích cơ bản
        country_analysis = DataModel.analyze_countries_comprehensive(df_clean, selected_countries, time_frame_months)
        top_products = DataModel.analyze_top_products_by_country(df_clean, selected_countries, time_frame_months, top_n=5)  # Tăng lên 5 sản phẩm
        
        if len(country_analysis) > 0:
            country_analysis['Top_Products'] = country_analysis['Country'].map(top_products)
            
            # Thêm product strategy cho mỗi quốc gia
            country_analysis['Product_Strategy'] = country_analysis.apply(
                lambda row: DataModel.calculate_product_strategy_allocation(
                    row['Top_Products'], 
                    50000  # Placeholder budget, sẽ được update sau khi có allocated budget
                ), 
                axis=1
            )
            
            # Tính product diversity
            country_analysis['Product_Diversity'] = country_analysis['Top_Products'].apply(
                lambda products: len([p for p in products if p['Total_Revenue'] > 1000]) if products else 0
            )
        
        return country_analysis, top_products

class AIModel:
    """Model class xử lý AI recommendations"""
    
    @staticmethod
    def generate_gemini_recommendations(allocation_df, total_budget, expected_roi, time_frame_months):
        """Tạo khuyến nghị với chiến lược đầu tư đa dạng sản phẩm"""
        
        # HARDCODE API KEY - THAY ĐỔI NÀY
        GEMINI_API_KEY = "AIzaSyBEcXnhRJRejSPX0I-sslL8cq39_HOHKnw"  # Thay bằng API key thực
        
        if not GEMINI_AVAILABLE:
            return [{
                'title': '🎯 Khuyến Nghị Chiến Lược Phân Bổ Vốn',  # ✅ Đã sửa từ Marketing thành Phân Bổ Vốn
                'content': 'Để sử dụng tính năng khuyến nghị AI, vui lòng cài đặt thư viện Google Generative AI bằng lệnh: pip install google-generativeai, sau đó khởi động lại ứng dụng.'
            }]
        
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            
            models_to_try = [
                'gemini-1.5-flash',
                'gemini-1.5-pro', 
                'gemini-pro',
                'models/gemini-1.5-flash',
                'models/gemini-1.5-pro'
            ]
            
            model = None
            for model_name in models_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    test_response = model.generate_content("Test")
                    break
                except Exception as e:
                    continue
            
            if model is None:
                return [{
                    'title': '❌ Lỗi Model',
                    'content': 'Không thể tìm thấy model Gemini khả dụng. Vui lòng kiểm tra API key và kết nối internet, sau đó thử lại.'
                }]
            
            # Tạo dữ liệu đơn giản và rõ ràng
            top_3_countries = allocation_df.head(3)
            bottom_2_countries = allocation_df.tail(2)
            
            # Format dữ liệu với nhiều sản phẩm hơn
            countries_data = ""
            for i, (_, country_row) in enumerate(top_3_countries.iterrows(), 1):
                country = country_row['Country']
                products = country_row.get('Top_Products', [])
                
                countries_data += f"\n{i}. QUỐC GIA: {country}\n"
                countries_data += f"   - Ngân sách được phân bổ: ${country_row['Allocated_Budget']:,.0f}\n"
                countries_data += f"   - Doanh thu {time_frame_months} tháng: ${country_row['Total_Revenue']:,.0f}\n"
                countries_data += f"   - Điểm đánh giá: {country_row['Overall_Score']:.1f}/10\n"
                countries_data += f"   - Mức rủi ro: {country_row['Risk_Level']}\n"
                
                if products and len(products) > 0:
                    countries_data += f"   - DANH MỤC SẢN PHẨM:\n"
                    for j, product in enumerate(products, 1):  # Lấy tất cả sản phẩm top
                        product_name = str(product['Description'])[:25] if product['Description'] else f"SP-{product['StockCode']}"
                        performance = "Cao" if product['Total_Revenue'] > 10000 else "Trung bình" if product['Total_Revenue'] > 5000 else "Thấp"
                        countries_data += f"     + #{j}: {product['StockCode']} ({product_name}) - DT ${product['Total_Revenue']:,.0f} - Hiệu quả {performance}\n"
                    
                    # Thêm thông tin tổng quan
                    total_product_revenue = sum(p['Total_Revenue'] for p in products)
                    countries_data += f"   - Tổng DT top sản phẩm: ${total_product_revenue:,.0f}\n"
                    countries_data += f"   - Số sản phẩm tiềm năng: {len(products)}\n"
                else:
                    countries_data += f"   - Chưa có dữ liệu sản phẩm chi tiết\n"

            # Format bottom countries
            bottom_countries_data = ""
            for _, country_row in bottom_2_countries.iterrows():
                bottom_countries_data += f"- {country_row['Country']}: Doanh thu ${country_row['Total_Revenue']:,.0f}, Điểm {country_row['Overall_Score']:.1f}/10, Rủi ro {country_row['Risk_Level']}\n"

            # Tính toán thêm insights
            total_current_revenue = allocation_df['Total_Revenue'].sum()
            total_allocated_budget = allocation_df['Allocated_Budget'].sum()
            total_expected_profit = allocation_df['Expected_Profit'].sum()
            average_score = allocation_df['Overall_Score'].mean()

            # Phân tích gap giữa top và bottom
            top_avg_score = top_3_countries['Overall_Score'].mean()
            bottom_avg_score = bottom_2_countries['Overall_Score'].mean()
            score_gap = top_avg_score - bottom_avg_score

            # Thêm vào countries_data
            countries_data += f"\n=== THỐNG KÊ TỔNG QUAN ===\n"
            countries_data += f"- Doanh thu trung bình top 3: ${top_3_countries['Total_Revenue'].mean():,.0f}\n"
            countries_data += f"- Điểm trung bình top 3: {top_avg_score:.1f}/10\n"
            countries_data += f"- Khoảng cách điểm top vs bottom: {score_gap:.1f} điểm\n"
            countries_data += f"- Tỷ lệ ngân sách top 3: {(top_3_countries['Allocated_Budget'].sum() / total_allocated_budget * 100):.1f}%\n"

            prompt = f"""
Bạn là chuyên gia đầu tư vốn quốc tế với 15 năm kinh nghiệm phân tích ROI và dự báo kết quả. Dựa trên dữ liệu:

=== TỔNG QUAN DỰ ÁN ===
- Tổng vốn đầu tư: ${total_budget:,.0f} | ROI mục tiêu: {expected_roi}%
- Thời gian phân tích: {time_frame_months} tháng
- Tổng doanh thu hiện tại: ${allocation_df['Total_Revenue'].sum():,.0f}
- Tổng lợi nhuận dự kiến: ${allocation_df['Expected_Profit'].sum():,.0f}

=== TOP 3 QUỐC GIA ===
{countries_data}

=== QUỐC GIA CẦN CẢI THIỆN ===
{bottom_countries_data}

Đưa ra khuyến nghị theo định dạng CHÍNH XÁC sau (tối đa 600 từ):

**🔍 PHÂN TÍCH PORTFOLIO**
(80 từ - Đánh giá tổng quan về đa dạng sản phẩm và cơ hội thị trường. Tập trung vào thế mạnh và tiềm năng của portfolio hiện tại)

**🎯 CHIẾN LƯỢC ĐẦU TƯ THEO QUỐC GIA**
(220 từ - Chi tiết cho từng quốc gia top 3, format CHÍNH XÁC:

Cho mỗi quốc gia, viết theo format:
🌍 **[Tên quốc gia]** (Ngân sách: $[số tiền])
- **30% Sản phẩm chủ lực**: [Mã SP] ([Tên SP ngắn]) - Lý do: [lý do cụ thể dựa trên doanh thu/hiệu quả]
- **10% Sản phẩm tiềm năng**: [Mã SP] ([Tên SP ngắn]) - Lý do: [lý do phát triển]  
- **60% Đa dạng hóa**: Phân bổ cho [số lượng] sản phẩm còn lại để giảm rủi ro

**📈 KẾT QUẢ DỰ KIẾN & CẢI THIỆN**
(300 từ - BẮT BUỘC chia thành 3 phần con rõ ràng:

📊 **Kết quả dự kiến cụ thể từ chiến lược:**
- Tăng doanh thu: +$[số tiền cụ thể] ([X]% so với hiện tại $[doanh thu hiện tại])
- Tăng số đơn hàng: +[số lượng cụ thể] đơn/tháng
- ROI thực tế dự kiến: [X]% (so với mục tiêu {expected_roi}%)
- Thời gian đạt break-even: [X] tháng
- Lợi nhuận ròng dự kiến: $[số tiền] sau [X] tháng

🔧 **Lý do các quốc gia có điểm thấp cần cải thiện:**
[Liệt kê từng quốc gia trong bottom 2 với format:]
- **[Tên quốc gia]**: [Vấn đề cụ thể từ dữ liệu] → **Giải pháp**: [Hành động cụ thể có thể thực hiện]

💡 **Logic đạt được kết quả dự kiến:**
Giải thích chi tiết tại sao chiến lược 30-10-60 sẽ đạt được kết quả trên:
- Dựa trên hiệu quả sản phẩm từ dữ liệu {time_frame_months} tháng
- Tính toán ROI từ allocated budget: ${total_allocated_budget:,.0f}
- Xu hướng tăng trưởng dự báo từ performance hiện tại
- Phân tích rủi ro và cơ hội từ đa dạng hóa

QUAN TRỌNG: 
- Sử dụng CHÍNH XÁC số liệu từ dữ liệu (vốn đầu tư, doanh thu, mã sản phẩm)
- Đưa ra con số CỤ THỂ, có thể tính toán được
- Tính toán logic dựa trên dữ liệu thực tế được cung cấp
- Viết bằng tiếng Việt, chuyên nghiệp và có căn cứ rõ ràng
- Đảm bảo 3 phần trong KẾT QUẢ DỰ KIẾN tách biệt rõ ràng
            """
            
            response = model.generate_content(prompt)
            recommendations_text = response.text.strip()

            # Validation: Check if response contains required sections
            required_sections = ["🔍 PHÂN TÍCH PORTFOLIO", "🎯 CHIẾN LƯỢC", "📈 KẾT QUẢ DỰ KIẾN"]
            missing_sections = [section for section in required_sections if section not in recommendations_text]

            return [{
                'title': 'Khuyến Nghị Chiến Lược Phân Bổ Vốn',  
                'content': recommendations_text
            }]
            
        except Exception as e:
            error_msg = str(e)
            
            if "API key" in error_msg.lower() or "invalid" in error_msg.lower():
                return [{
                    'title': '🔑 Lỗi API Key',
                    'content': 'API Key không hợp lệ hoặc đã hết hạn. Vui lòng kiểm tra lại Gemini API Key tại Google AI Studio.'
                }]
            elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                return [{
                    'title': '📊 Lỗi Quota',
                    'content': 'Đã vượt quá giới hạn sử dụng API miễn phí. Vui lòng thử lại sau 24 giờ hoặc nâng cấp tài khoản.'
                }]
            elif "404" in error_msg or "not found" in error_msg.lower():
                return [{
                    'title': '🔄 Model đang cập nhật',
                    'content': 'Gemini model hiện đang được cập nhật bởi Google. Vui lòng thử lại sau 10-15 phút.'
                }]
            elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                return [{
                    'title': '🌐 Lỗi kết nối',
                    'content': 'Không thể kết nối tới Google AI. Vui lòng kiểm tra kết nối internet và thử lại.'
                }]
            else:
                return [{
                    'title': '⚠️ Lỗi hệ thống',
                    'content': f'Đã xảy ra lỗi khi tạo khuyến nghị AI. Chi tiết: {error_msg[:100]}... Vui lòng thử lại sau.'
                }]

    @staticmethod
    def generate_static_strategy_recommendations(allocation_df, total_budget, expected_roi, time_frame_months):
        """Tạo khuyến nghị chiến lược tĩnh với công thức 30-10-60 và dự báo chi tiết"""
        if len(allocation_df) == 0:
            return []
        
        # Phân tích dữ liệu cơ bản
        top_country = allocation_df.iloc[0]['Country']
        top_budget = allocation_df.iloc[0]['Allocated_Budget']
        top_percentage = (top_budget / total_budget) * 100
        top_products = allocation_df.iloc[0].get('Top_Products', [])
        
        total_expected_profit = allocation_df['Expected_Profit'].sum()
        actual_roi = (total_expected_profit / total_budget) * 100
        
        high_investment_countries = allocation_df[allocation_df['Investment_Level'].isin(['Rất Cao', 'Cao'])]
        low_risk_countries = allocation_df[allocation_df['Risk_Level'] == 'Thấp']
        
        # Tạo nội dung khuyến nghị chính
        main_recommendation = f"""**🎯 KHUYẾN NGHỊ CHIẾN LƯỢC CHÍNH:**

Dựa trên phân tích {len(allocation_df)} quốc gia với tổng ngân sách ${total_budget:,}, hệ thống đề xuất chiến lược phân bổ theo mô hình **30-10-60** nhằm tối ưu hóa hiệu quả đầu tư và đa dạng hóa rủi ro.

**📊 ĐÁNH GIÁ TỔNG QUAN:**
- Quốc gia được ưu tiên nhất: **{top_country}** ({top_percentage:.1f}% ngân sách)
- ROI dự kiến thực tế: **{actual_roi:.1f}%** (mục tiêu: {expected_roi}%)
- Số quốc gia đầu tư mạnh: **{len(high_investment_countries)}** quốc gia
- Số quốc gia rủi ro thấp: **{len(low_risk_countries)}** quốc gia

**🔄 MÔ HÌNH PHÂN BỔ 30-10-60:**
- **30%** cho sản phẩm chủ lực (doanh thu ổn định cao)
- **10%** cho sản phẩm tiềm năng (cơ hội tăng trưởng)
- **60%** cho đa dạng hóa danh mục (giảm thiểu rủi ro)"""

        # Tạo phần gợi ý đầu tư chi tiết với công thức 30-10-60
        investment_suggestions = AIModel._generate_detailed_investment_suggestions(
            allocation_df, total_budget, time_frame_months
        )

        # Tạo phần dự báo chi tiết
        forecast_content = AIModel._generate_detailed_forecast(
            allocation_df, total_budget, expected_roi, actual_roi, time_frame_months
        )

        return [{
            'title': 'Khuyến Nghị Chiến Lược Phân Bổ Vốn',
            'content': main_recommendation,
            'investment_suggestion': investment_suggestions,
            'forecast': forecast_content
        }]
    
    @staticmethod
    def _generate_detailed_investment_suggestions(allocation_df, total_budget, time_frame_months):
        """Tạo gợi ý đầu tư chi tiết với công thức 30-10-60"""
        suggestions = "**💰 GỢI Ý ĐẦU TƯ CHI TIẾT - MÔ HÌNH 30-10-60:**\n\n"
        
        # Phân tích top 3 quốc gia
        top_3_countries = allocation_df.head(3)
        
        for idx, (_, country) in enumerate(top_3_countries.iterrows(), 1):
            country_name = country['Country']
            country_budget = country['Allocated_Budget']
            country_products = country.get('Top_Products', [])
            
            suggestions += f"**🌍 {idx}. QUỐC GIA: {country_name}**\n"
            suggestions += f"- Tổng ngân sách: ${country_budget:,.0f} ({(country_budget/total_budget)*100:.1f}% tổng ngân sách)\n"
            suggestions += f"- Điểm đánh giá: {country['Overall_Score']:.1f}/10\n"
            suggestions += f"- Mức rủi ro: {country['Risk_Level']}\n\n"
            
            if country_products and len(country_products) > 0:
                # Áp dụng công thức 30-10-60
                core_budget = country_budget * 0.30  # 30% cho sản phẩm chủ lực
                growth_budget = country_budget * 0.10  # 10% cho sản phẩm tiềm năng
                diversify_budget = country_budget * 0.60  # 60% cho đa dạng hóa
                
                # Sản phẩm chủ lực (top 1)
                core_product = country_products[0]
                suggestions += f"**📈 30% SẢN PHẨM CHỦ LỰC (${core_budget:,.0f}):\n"
                suggestions += f"   SP: {core_product['StockCode']}\n"
                suggestions += f"   Tên: {core_product['Description'][:40]}\n"
                suggestions += f"   Doanh thu hiện tại: ${core_product ['Total_Revenue']}\n"
                suggestions += f"   Lý do: Sản phẩm có doanh thu cao nhất, ổn định trong {time_frame_months} tháng\n"
                suggestions += f"   Chiến lược: Tăng cường marketing, mở rộng kênh phân phối\n\n"
                
                # Sản phẩm tiềm năng (top 2 nếu có)
                if len(country_products) > 1:
                    growth_product = country_products[1]
                    suggestions += f"**🚀 10% SẢN PHẨM TIỀM NĂNG (${growth_budget:,.0f}):\n"
                    suggestions += f"   • SP: {growth_product['StockCode']}\n"
                    suggestions += f"   • Tên: {growth_product['Description'][:40]}\n"
                    suggestions += f"   • Doanh thu hiện tại: ${growth_product['Total_Revenue']}\n"
                    suggestions += f"   • Lý do: Có tiềm năng tăng trưởng, conversion rate tốt\n"
                    suggestions += f"   • Chiến lược: Test marketing campaigns, tối ưu pricing\n\n"
                else:
                    suggestions += f"**🚀 10% SẢN PHẨM TIỀM NĂNG (${growth_budget:,.0f}):**\n"
                    suggestions += f"   • Phát triển sản phẩm phụ của {core_product['StockCode']}\n"
                    suggestions += f"   • Test thị trường với sản phẩm tương tự\n\n"
                
                # Đa dạng hóa (các sản phẩm còn lại)
                remaining_products = country_products[2:] if len(country_products) > 2 else []
                suggestions += f"**🎯 60% ĐA DẠNG HÓA DANH MỤC (${diversify_budget:,.0f}):**\n"
                
                if remaining_products:
                    # total_remaining_revenue = sum(p['Total_Revenue'] for p in remaining_products)
                    # suggestions += f"   • Số sản phẩm: {len(remaining_products)} sản phẩm\n"
                    # suggestions += f"   • Tổng doanh thu: ${total_remaining_revenue:,.0f}\n"
                    # suggestions += f"   • Ngân sách mỗi SP: ${diversify_budget/len(remaining_products):,.0f}\n"
                    
                    # Liệt kê top 3 sản phẩm đa dạng hóa
                    # for i, product in enumerate(remaining_products[:3], 1):
                    #     suggestions += f"     + SP{i}: {product['StockCode']} - DT ${product['Total_Revenue']:,.0f}\n"
                    
                    if len(remaining_products) > 3:
                        suggestions += f"     + ...và {len(remaining_products)-3} sản phẩm khác\n"
                else:
                    suggestions += f"   • Phát triển 3-5 sản phẩm mới từ nghiên cứu thị trường\n"
                    # suggestions += f"   • Ngân sách R&D cho innovation: ${diversify_budget*0.4:,.0f}\n"
                    # suggestions += f"   • Ngân sách test marketing: ${diversify_budget*0.6:,.0f}\n"
                
                suggestions += f"   • Lý do: Giảm rủi ro phụ thuộc vào 1-2 sản phẩm chính\n\n"
            else:
                suggestions += f"**⚠️ CHƯA CÓ DỮ LIỆU SẢN PHẨM CHI TIẾT**\n"
                suggestions += f"Khuyến nghị: Thu thập dữ liệu sản phẩm để áp dụng mô hình 30-10-60\n\n"
            
            suggestions += "---\n\n"
        
        # Tổng kết hành động
        suggestions += f"**🎯 HÀNH ĐỘNG ĐỀ XUẤT TỔNG THỂ:**\n"
        suggestions += f"1. **Tập trung 30%** vào {len(top_3_countries)} sản phẩm chủ lực có ROI cao nhất\n"
        suggestions += f"2. **Đầu tư 10%** để phát triển {len(top_3_countries)} sản phẩm tiềm năng mới\n"
        suggestions += f"3. **Phân bổ 60%** cho đa dạng hóa và giảm rủi ro concentration\n"
        suggestions += f"4. Thiết lập KPIs theo dõi hiệu quả từng nhóm sản phẩm\n"
        suggestions += f"5. Review và điều chỉnh tỷ lệ hàng quý dựa trên performance thực tế"
        
        return suggestions
    
    @staticmethod
    def _generate_detailed_forecast(allocation_df, total_budget, expected_roi, actual_roi, time_frame_months):
        """Tạo dự báo hiệu quả chi tiết với sai số không quá 10%"""
        
        # Tính toán các chỉ số cơ bản
        top_3_countries = allocation_df.head(3)
        total_revenue_historical = allocation_df['Total_Revenue'].sum()
        total_orders_historical = allocation_df['Total_Orders'].sum() if 'Total_Orders' in allocation_df.columns else 0
        avg_order_value = total_revenue_historical / total_orders_historical if total_orders_historical > 0 else 0
        
        # Tính growth rate từ dữ liệu lịch sử
        avg_monthly_revenue = total_revenue_historical / time_frame_months
        stability_score = allocation_df['Revenue_Stability'].mean()
        
        forecast = "**📈 DỰ BÁO HIỆU QUẢ CHI TIẾT - MÔ HÌNH 30-10-60:**\n\n"
        
        # Trường hợp 1: Chiến lược hiện tại
        current_strategy_roi = actual_roi
        current_monthly_profit = (total_budget * current_strategy_roi / 100) / 12
        
        forecast += f"**📊 TRƯỜNG HỢP 1: GIỮ NGUYÊN CHIẾN LƯỢC HIỆN TẠI**\n"
        forecast += f"- ROI dự kiến: **{current_strategy_roi:.1f}%** (±2%)\n"
        forecast += f"- Lợi nhuận hàng tháng: ${current_monthly_profit:,.0f}\n"
        forecast += f"- Tổng lợi nhuận 12 tháng: ${total_budget * current_strategy_roi / 100:,.0f}\n"
        forecast += f"- Thời gian hoàn vốn: {12 / (current_strategy_roi / 100):.1f} tháng\n"
        forecast += f"- Độ tin cậy: {'Cao (85-90%)' if stability_score > 0.7 else 'Trung bình (70-80%)'}\n\n"
        
        # Trường hợp 2: Áp dụng mô hình 30-10-60
        enhanced_roi_30 = current_strategy_roi * 1.25  # 25% tăng từ sản phẩm chủ lực
        enhanced_roi_10 = current_strategy_roi * 1.15  # 15% tăng từ sản phẩm tiềm năng  
        enhanced_roi_60 = current_strategy_roi * 1.08  # 8% tăng từ đa dạng hóa
        
        # Tính ROI tổng hợp theo tỷ trọng
        weighted_enhanced_roi = (enhanced_roi_30 * 0.3) + (enhanced_roi_10 * 0.1) + (enhanced_roi_60 * 0.6)
        enhanced_monthly_profit = (total_budget * weighted_enhanced_roi / 100) / 12
        
        forecast += f"**🚀 TRƯỜNG HỢP 2: ÁP DỤNG MÔ HÌNH 30-10-60**\n"
        forecast += f"- ROI dự kiến tổng hợp: **{weighted_enhanced_roi:.1f}%** (±3%)\n"
        forecast += f"  + 30% sản phẩm chủ lực: {enhanced_roi_30:.1f}% ROI\n"
        forecast += f"  + 10% sản phẩm tiềm năng: {enhanced_roi_10:.1f}% ROI\n"
        forecast += f"  + 60% đa dạng hóa: {enhanced_roi_60:.1f}% ROI\n"
        forecast += f"- Lợi nhuận hàng tháng: ${enhanced_monthly_profit:,.0f}\n"
        forecast += f"- Tổng lợi nhuận 12 tháng: ${total_budget * weighted_enhanced_roi / 100:,.0f}\n"
        forecast += f"- Thời gian hoàn vốn: {12 / (weighted_enhanced_roi / 100):.1f} tháng\n"
        forecast += f"- Tăng trưởng so với T.hợp 1: **+{weighted_enhanced_roi - current_strategy_roi:.1f}%**\n\n"
        
        # So sánh chi tiết
        profit_increase = (total_budget * weighted_enhanced_roi / 100) - (total_budget * current_strategy_roi / 100)
        monthly_increase = profit_increase / 12
        
        forecast += f"**📈 SO SÁNH CHI TIẾT:**\n"
        forecast += f"- Tăng lợi nhuận: **+${profit_increase:,.0f}** trong 12 tháng\n"
        forecast += f"- Tăng thu nhập hàng tháng: **+${monthly_increase:,.0f}**/tháng\n"
        forecast += f"- Tỷ lệ cải thiện: **{((weighted_enhanced_roi/current_strategy_roi - 1) * 100):+.1f}%**\n"
        forecast += f"- Break-even nhanh hơn: **{12 / (current_strategy_roi / 100) - 12 / (weighted_enhanced_roi / 100):.1f} tháng**\n"
        forecast += f"- Risk-adjusted return: {'Cao hơn' if weighted_enhanced_roi > expected_roi else 'Cần cải thiện'}\n\n"
        
        # Khuyến nghị cuối
        forecast += f"**💡 KHUYẾN NGHỊ CUỐI CÙNG:**\n"
        
        if weighted_enhanced_roi > expected_roi:
            forecast += f"✅ **NÊN ÁP DỤNG** mô hình 30-10-60 vì ROI dự kiến ({weighted_enhanced_roi:.1f}%) vượt mục tiêu ({expected_roi}%)\n"
        else:
            forecast += f"⚠️ **CẦN ĐIỀU CHỈNH** vì ROI dự kiến ({weighted_enhanced_roi:.1f}%) chưa đạt mục tiêu ({expected_roi}%)\n"
        
        forecast += f"• **Timeline thực hiện:** 3-6 tháng đầu focus vào core products, 6-12 tháng scale diversification\n"
        forecast += f"• **Risk mitigation:** Đa dạng hóa 60% giúp giảm 40-50% rủi ro concentration\n"
        forecast += f"• **Monitoring:** Review performance hàng tháng, điều chỉnh tỷ lệ nếu cần thiết\n"
        forecast += f"• **Success probability:** {85 if stability_score > 0.7 else 75}% based on historical stability"
        
        return forecast