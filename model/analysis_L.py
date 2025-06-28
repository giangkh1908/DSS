# Các hàm phân tích, khuyến nghị, dự báo, và logic không liên quan đến giao diện
# ... Copy các hàm generate_recommendations, comment_total_revenue, recommend_total_revenue, comment_growth_rate, recommend_growth_rate, comment_compare_revenue, recommend_compare_revenue, action_suggestions_total_revenue, action_suggestions_growth_rate, action_suggestions_compare_revenue, suggest_investment_total_revenue, suggest_investment_growth_rate, suggest_investment_compare_revenue, estimate_profit_increase_total_revenue_one_year, estimate_growth_trend_growth_rate_one_year từ ass.py vào đây ... 

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import calendar

def generate_recommendations(pivot_table, growth_rate, total_revenue, country_metrics, monthly_revenue, quarterly_proportion, analysis_types):
    # Biểu đồ tổng doanh thu theo thời gian
    if 'Tổng doanh thu' in analysis_types:
        plt.figure(figsize=(12, 6))
        for country in pivot_table.columns:
            plt.plot(pivot_table.index, pivot_table[country], label=country, marker='o')
        plt.title('Xu hướng Doanh thu theo Quốc gia')
        plt.xlabel('Tháng-Năm')
        plt.ylabel('Doanh thu (£)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(plt)
        plt.close()
    if 'Tốc độ tăng trưởng' in analysis_types:
        plt.figure(figsize=(12, 6))
        for country in growth_rate.columns:
            plt.plot(growth_rate.index, growth_rate[country], label=country, marker='o')
        plt.title('Tốc độ Tăng trưởng Doanh thu theo Quốc gia')
        plt.xlabel('Tháng-Năm')
        plt.ylabel('Tốc độ Tăng trưởng (%)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(plt)
        plt.close()
    if 'So sánh doanh thu' in analysis_types:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        total_revenue.plot(kind='bar', ax=ax1)
        ax1.set_title('So sánh Tổng Doanh thu theo Quốc gia')
        ax1.set_xlabel('Quốc gia')
        ax1.set_ylabel('Tổng Doanh thu (£)')
        ax1.tick_params(axis='x', rotation=45)
        market_share = (total_revenue / total_revenue.sum() * 100)
        ax2.pie(market_share, labels=market_share.index, autopct='%1.1f%%')
        ax2.set_title('Thị phần Doanh thu theo Quốc gia')
        plt.tight_layout()
        st.pyplot(plt)
        plt.close()
    if 'Phân tích Mùa vụ' in analysis_types and monthly_revenue is not None:
        plt.figure(figsize=(12, 6))
        monthly_avg = monthly_revenue.to_frame('Doanh thu TB')
        monthly_avg['Tháng'] = [calendar.month_name[i] for i in monthly_avg.index]
        plt.bar(monthly_avg['Tháng'], monthly_avg['Doanh thu TB'])
        plt.title('Doanh thu Trung bình theo Tháng')
        plt.xlabel('Tháng')
        plt.ylabel('Doanh thu Trung bình (£)')
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(plt)
        plt.close()
        if quarterly_proportion is not None:
            plt.figure(figsize=(8, 8))
            plt.pie(quarterly_proportion, labels=[f'Quý {i}' for i in range(1, 5)],
                   autopct='%1.1f%%', startangle=90)
            plt.title('Tỷ trọng Doanh thu theo Quý')
            plt.axis('equal')
            st.pyplot(plt)
            plt.close()
    if 'Hiệu suất Quốc gia' in analysis_types and country_metrics is not None:
        fig, ax = plt.subplots(figsize=(12, 8))
        scatter = ax.scatter(country_metrics['YoY_Growth'], 
                           country_metrics['Stability'],
                           s=country_metrics['Total_Revenue']/1e4,
                           alpha=0.6,
                           c=country_metrics['Total_Revenue'],
                           cmap='viridis')
        for idx, row in country_metrics.iterrows():
            ax.annotate(idx, (row['YoY_Growth'], row['Stability']),
                       xytext=(5, 5), textcoords='offset points')
        plt.colorbar(scatter, label='Tổng doanh thu (£)')
        ax.axhline(y=30, color='r', linestyle='--', alpha=0.3)
        ax.axvline(x=20, color='r', linestyle='--', alpha=0.3)
        ax.text(21, 31, 'Tăng trưởng không ổn định', fontsize=8)
        ax.text(-5, 31, 'Suy giảm không ổn định', fontsize=8)
        ax.text(21, 5, 'Tăng trưởng ổn định', fontsize=8)
        ax.text(-5, 5, 'Suy giảm ổn định', fontsize=8)
        ax.set_xlabel('Tăng trưởng Năm (%)')
        ax.set_ylabel('Độ biến động (CV %)')
        ax.set_title('Ma trận Hiệu suất Quốc gia')
        ax.grid(True, linestyle='--', alpha=0.3)
        plt.tight_layout()
        st.pyplot(plt)
        plt.close()

def comment_total_revenue(pivot_table):
    top_country = pivot_table.sum().idxmax()
    return f"- Quốc gia có doanh thu cao nhất: {top_country}."

def recommend_total_revenue(pivot_table):
    return "Khuyến nghị: Tập trung vào các quốc gia có doanh thu cao để tối ưu hóa nguồn lực và tăng trưởng ổn định."

def comment_growth_rate(growth_rate):
    avg_growth = growth_rate.mean()
    top_growth_country = avg_growth.idxmax()
    return f"- Quốc gia có tốc độ tăng trưởng trung bình cao nhất: {top_growth_country} ({avg_growth[top_growth_country]:.2f}%)."

def recommend_growth_rate(growth_rate):
    return "Khuyến nghị: Đẩy mạnh marketing ở các quốc gia có tốc độ tăng trưởng cao và tìm hiểu nguyên nhân ở các quốc gia tăng trưởng thấp."

def comment_compare_revenue(total_revenue):
    top = total_revenue.idxmax()
    top_revenue = total_revenue[top]
    comparison_ratios = {}
    for country in total_revenue.index:
        if country != top:
            ratio = top_revenue / total_revenue[country]
            comparison_ratios[country] = ratio
    details = f"- Quốc gia có tổng doanh thu lớn nhất: {top} ({top_revenue:,.0f} £).\n"
    if comparison_ratios:
        details += "- **So sánh với các quốc gia khác:**\n"
        for country, ratio in comparison_ratios.items():
            details += f"  • {top} gấp {ratio:.1f} lần {country}\n"
        avg_ratio = sum(comparison_ratios.values()) / len(comparison_ratios)
        max_ratio = max(comparison_ratios.values())
        min_ratio = min(comparison_ratios.values())
        details += f"- **Thống kê tỷ lệ:**\n"
        details += f"  • Tỷ lệ trung bình: {avg_ratio:.1f} lần\n"
        details += f"  • Tỷ lệ cao nhất: {max_ratio:.1f} lần\n"
        details += f"  • Tỷ lệ thấp nhất: {min_ratio:.1f} lần\n"
        if avg_ratio >= 5:
            assessment = "Rất cao - có sự chênh lệch lớn giữa các thị trường"
        elif avg_ratio >= 3:
            assessment = "Cao - có sự chênh lệch đáng kể"
        elif avg_ratio >= 2:
            assessment = "Trung bình - có sự chênh lệch vừa phải"
        else:
            assessment = "Thấp - các thị trường tương đối cân bằng"
        details += f"- **Đánh giá chênh lệch:** {assessment}"
    return details

def recommend_compare_revenue(total_revenue):
    top = total_revenue.idxmax()
    top_revenue = total_revenue[top]
    other_revenues = [total_revenue[country] for country in total_revenue.index if country != top]
    if other_revenues:
        avg_ratio = top_revenue / (sum(other_revenues) / len(other_revenues))
        if avg_ratio >= 5:
            recommendation = f"Khuyến nghị: Tập trung mạnh vào {top} vì có ưu thế vượt trội ({avg_ratio:.1f} lần trung bình), đồng thời xem xét chiến lược thâm nhập thị trường cho các quốc gia khác."
        elif avg_ratio >= 3:
            recommendation = f"Khuyến nghị: Duy trì vị thế tại {top} và tăng cường đầu tư vào các thị trường tiềm năng khác để cân bằng thị phần."
        elif avg_ratio >= 2:
            recommendation = f"Khuyến nghị: Phân bổ nguồn lực hợp lý giữa {top} và các thị trường khác để tối ưu hóa tăng trưởng tổng thể."
        else:
            recommendation = f"Khuyến nghị: Các thị trường tương đối cân bằng, có thể mở rộng đều đặn ở tất cả các quốc gia được chọn."
    else:
        recommendation = "Khuyến nghị: Xem xét phân bổ lại nguồn lực dựa trên thị phần doanh thu và tập trung vào các thị trường tiềm năng."
    return recommendation

def action_suggestions_total_revenue():
    return [
        "Tăng cường quảng cáo vì đang có doanh thu cao, cần tiếp tục duy trì và đẩy mạnh.",
        "Tối ưu hóa nguồn lực, đảm bảo độ ổn định và tăng trưởng.",
        "Theo dõi sát các quốc gia khác có doanh thu tăng đột biến để học hỏi kinh nghiệm."
    ]

def action_suggestions_growth_rate():
    return [
        "Đẩy mạnh marketing vì đang có tốc độ tăng trưởng cao, nghĩa là hướng đi hiện tại vẫn đúng.",
        "Phân tích nguyên nhân tăng trưởng thấp ở các quốc gia khác.",
        "Thử nghiệm chiến lược mới tại các thị trường tăng trưởng nhanh, nhưng cần đảm bảo tính an toàn và độ ổn định."
    ]

def action_suggestions_compare_revenue():
    return [
        "Phân bổ lại nguồn lực dựa trên thị phần doanh thu, tránh lãng phí và thất thoát.",
        "Tập trung phát triển các thị trường tiềm năng có thị phần nhỏ nhưng tính tăng trưởng tốt.",
        "Xem xét giảm đầu tư ở các quốc gia có doanh thu thấp kéo dài."
    ]

def suggest_investment_total_revenue(pivot_table, country_metrics):
    top_country = pivot_table.sum().idxmax()
    total_revenue = country_metrics.loc[top_country, 'Total_Revenue']
    stability = country_metrics.loc[top_country, 'Stability']
    benefit = (
        f"Đầu tư vào {top_country} giúp duy trì và mở rộng thị phần tại thị trường lớn nhất "
        f"({total_revenue:,.0f} £), đồng thời tối ưu hóa nguồn lực nhờ độ ổn định doanh thu ({stability:.2f}%)."
    )
    return top_country, benefit, total_revenue, stability

def suggest_investment_growth_rate(growth_rate, country_metrics):
    avg_growth = growth_rate.mean()
    top_country = avg_growth.idxmax()
    growth = avg_growth[top_country]
    stability = country_metrics.loc[top_country, 'Stability']
    benefit = (
        f"Đầu tư vào {top_country} giúp tận dụng tốc độ tăng trưởng mạnh ({growth:.2f}%), "
        f"có tiềm năng sinh lời cao. Độ ổn định doanh thu: {stability:.2f}%."
    )
    return top_country, benefit, growth, stability

def suggest_investment_compare_revenue(total_revenue, country_metrics):
    top_country = total_revenue.idxmax()
    revenue = total_revenue[top_country]
    stability = country_metrics.loc[top_country, 'Stability']
    benefit = (
        f"Đầu tư vào {top_country} giúp tối ưu hóa lợi nhuận tổng thể ({revenue:,.0f} £), "
        f"củng cố vị thế tại thị trường chủ lực với độ ổn định doanh thu {stability:.2f}%."
    )
    return top_country, benefit, revenue, stability

def estimate_profit_increase_total_revenue_one_year(pivot_table, country_metrics):
    top_country = pivot_table.sum().idxmax()
    monthly_revenue = pivot_table[top_country].dropna()
    if len(monthly_revenue) < 2:
        return 0.0, 0.0, "Không đủ dữ liệu để tính toán", top_country, monthly_revenue
    growth_rates = monthly_revenue.pct_change().dropna()
    avg_growth = growth_rates.mean() if not growth_rates.empty else 0
    current_revenue = monthly_revenue.iloc[-1] if not monthly_revenue.empty else 0
    total_revenue = country_metrics.loc[top_country, 'Total_Revenue']
    stability = country_metrics.loc[top_country, 'Stability']
    x = np.arange(len(monthly_revenue))
    y = monthly_revenue.values
    slope, intercept = np.polyfit(x, y, 1)
    trend_growth = slope / y[-1] if y[-1] != 0 else 0
    volatility = growth_rates.std()
    seasonal_factor = 1.0
    if len(monthly_revenue) >= 12:
        monthly_avg = monthly_revenue.groupby(monthly_revenue.index.str[-2:]).mean()
        if len(monthly_avg) >= 2:
            seasonal_factor = monthly_avg.iloc[-1] / monthly_avg.mean()
    stability_factor = max(0.5, 1 - (stability / 100))
    base_growth = (trend_growth * 12) * stability_factor * seasonal_factor
    base_forecast = base_growth * 100
    investment_multiplier = 1.2
    efficiency_gain = 1.15 + (0.1 * stability_factor)
    enhanced_growth = base_growth * investment_multiplier * efficiency_gain
    enhanced_forecast = enhanced_growth * 100
    explanation = f"""
    **Phân tích dự báo lợi nhuận cho {top_country}:**
    
    📊 **Dữ liệu hiện tại:**
    - Doanh thu tháng gần nhất: {current_revenue:,.0f} £
    - Tổng doanh thu: {total_revenue:,.0f} £
    - Độ ổn định thị trường: {stability:.2f}%
    
    📈 **Phân tích xu hướng:**
    - Tốc độ tăng trưởng trung bình/tháng: {avg_growth*100:.2f}%
    - Xu hướng tuyến tính: {trend_growth*100:.2f}%/tháng
    - Độ biến động thị trường: {volatility*100:.2f}%
    - Hệ số mùa vụ: {seasonal_factor:.2f}
    - Hệ số ổn định: {stability_factor:.2f}
    
    🎯 **Dự báo lợi nhuận năm sau:**
    
    **Trường hợp 1: Giữ nguyên ngân sách đầu tư**
    - Dự báo tăng trưởng: {base_forecast:.2f}%
    - Lý do: Dựa trên xu hướng tự nhiên của thị trường
    - Độ tin cậy: {'Cao' if stability <= 30 else 'Trung bình' if stability <= 60 else 'Thấp'}
    
    **Trường hợp 2: Tăng ngân sách đầu tư thêm 20%**
    - Dự báo tăng trưởng: {enhanced_forecast:.2f}%
    - Tăng thêm so với trường hợp 1: {enhanced_forecast - base_forecast:.2f}%
    - Hiệu quả đầu tư dự kiến: {efficiency_gain:.2f}x
    - Lý do: Tăng cường marketing và mở rộng thị trường
    
    💡 **Khuyến nghị:**
    - {'Nên tăng đầu tư' if enhanced_forecast - base_forecast > 5 else 'Cân nhắc kỹ trước khi tăng đầu tư'}
    - Thị trường {'ổn định' if stability <= 30 else 'có biến động vừa phải' if stability <= 60 else 'có biến động cao'}
    - ROI dự kiến: {((enhanced_forecast - base_forecast) / 20):.2f}% cho mỗi 1% tăng đầu tư
    """
    return base_forecast, enhanced_forecast, explanation, top_country, monthly_revenue

def estimate_growth_trend_growth_rate_one_year(growth_rate, country_metrics):
    avg_growth = growth_rate.mean()
    top_country = avg_growth.idxmax()
    country_growth = growth_rate[top_country].dropna()
    if len(country_growth) < 2:
        return "Không đủ dữ liệu", 0.0, 0.0, f"Không đủ dữ liệu để phân tích xu hướng cho {top_country}", top_country
    last = country_growth.iloc[-1]
    avg = country_growth.mean()
    stability = country_metrics.loc[top_country, 'Stability']
    if len(country_growth) >= 3:
        recent_3m = country_growth.tail(3)
        momentum = recent_3m.mean() - avg
        acceleration = recent_3m.iloc[-1] - recent_3m.iloc[0]
    else:
        momentum = last - avg
        acceleration = 0
    growth_volatility = country_growth.std()
    growth_stability = 1 - (growth_volatility / abs(avg)) if avg != 0 else 0.5
    market_factor = max(0.5, 1 - (stability / 100))
    reversion_strength = 0.3
    momentum_decay = 0.7
    base_forecast = avg + (momentum * momentum_decay) + (acceleration * 0.5)
    base_forecast = base_forecast * market_factor
    base_forecast = max(base_forecast, avg * 0.5)
    base_forecast = min(base_forecast, avg * 2.0)
    investment_efficiency = 1.2
    market_response = 1.15 + (0.1 * market_factor)
    enhanced_momentum = momentum * 1.3
    enhanced_forecast = avg + (enhanced_momentum * momentum_decay) + (acceleration * 0.8)
    enhanced_forecast = enhanced_forecast * market_factor * market_response
    enhanced_forecast = max(enhanced_forecast, base_forecast * 1.05)
    enhanced_forecast = min(enhanced_forecast, avg * 2.5)
    if enhanced_forecast > last:
        trend = "Tăng"
        trend_reason = "tốc độ tăng trưởng dự kiến cao hơn hiện tại"
    elif enhanced_forecast < last:
        trend = "Giảm"
        trend_reason = "tốc độ tăng trưởng dự kiến thấp hơn hiện tại"
    else:
        trend = "Giữ nguyên"
        trend_reason = "tốc độ tăng trưởng dự kiến tương đương hiện tại"
    change_from_current = base_forecast - last
    additional_growth = enhanced_forecast - base_forecast
    explanation = f"""
    **Phân tích dự báo tốc độ tăng trưởng cho {top_country}:**
    
    📊 **Dữ liệu hiện tại:**
    - Tốc độ tăng trưởng hiện tại: {last:.2f}%
    - Tốc độ tăng trưởng trung bình: {avg:.2f}%
    - Độ biến động tăng trưởng: {growth_volatility:.2f}%
    - Độ ổn định thị trường: {stability:.2f}%
    
    📈 **Phân tích xu hướng:**
    - Momentum (3 tháng gần đây): {momentum:.2f}%
    - Acceleration (tốc độ thay đổi): {acceleration:.2f}%
    - Độ ổn định tăng trưởng: {growth_stability:.2f}
    - Hệ số thị trường: {market_factor:.2f}
    
    🎯 **Dự báo tốc độ tăng trưởng năm sau:**
    
    **Trường hợp 1: Giữ nguyên tình trạng hiện tại**
    - Dự báo tăng trưởng: {base_forecast:.2f}%
    - Thay đổi so với hiện tại: {change_from_current:+.2f}%
    - Lý do: Dựa trên xu hướng tự nhiên và mean reversion
    - Độ tin cậy: {'Cao' if growth_stability >= 0.7 else 'Trung bình' if growth_stability >= 0.4 else 'Thấp'}
    
    **Trường hợp 2: Tăng cường đầu tư thêm 20%**
    - Dự báo tăng trưởng: {enhanced_forecast:.2f}%
    - Thay đổi so với hiện tại: {enhanced_forecast - last:+.2f}%
    - Tăng thêm so với giữ nguyên: {additional_growth:+.2f}%
    - Hiệu quả đầu tư dự kiến: {market_response:.2f}x
    - Lý do: Tăng cường marketing và mở rộng thị trường
    
    🎯 **Xu hướng tổng thể: {trend}**
    - Lý do: {trend_reason}
    - Thị trường {'ổn định' if stability <= 30 else 'có biến động vừa phải' if stability <= 60 else 'có biến động cao'}
    
    💡 **Khuyến nghị:**
    - {'Nên tăng đầu tư' if additional_growth > 3 else 'Cân nhắc kỹ trước khi tăng đầu tư'}
    - ROI dự kiến: {additional_growth/20:.2f}% cho mỗi 1% tăng đầu tư
    - Rủi ro: {'Thấp' if stability <= 30 else 'Trung bình' if stability <= 60 else 'Cao'}
    """
    return trend, base_forecast, enhanced_forecast, explanation, top_country 