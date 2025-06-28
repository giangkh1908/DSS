def get_marketing_strategy(month_type, month_number):
    """
    Trả về chiến lược marketing tùy theo loại tháng
    """
    strategies = {
        "peak": f"🔥 Tháng {month_number} - Tháng cao điểm: Tăng cường quảng cáo, mở rộng inventory, triển khai chương trình loyalty",
        "low": f"❄️ Tháng {month_number} - Tháng thấp điểm: Flash sale, combo deals, tặng kèm sản phẩm để kích cầu",
        "stable": f"✅ Tháng {month_number} - Tháng ổn định: Duy trì chất lượng, test marketing campaigns nhỏ",
        "volatile": f"⚡ Tháng {month_number} - Tháng biến động: Phân tích nguyên nhân, điều chỉnh chiến lược linh hoạt"
    }
    return strategies.get(month_type, "Không có chiến lược cụ thể")

def display_marketing_recommendations(peak_month, low_month, stable_months, volatile_month=None):
    """
    Hiển thị đầy đủ các gợi ý marketing
    """
    recommendations = []
    
    # Tháng cao điểm
    recommendations.append(get_marketing_strategy("peak", int(peak_month['Month'])))
    
    # Tháng thấp điểm  
    recommendations.append(get_marketing_strategy("low", int(low_month['Month'])))
    
    # Tháng ổn định
    if stable_months:
        for month in stable_months:
            recommendations.append(get_marketing_strategy("stable", month))
    
    # Tháng biến động
    if volatile_month:
        recommendations.append(get_marketing_strategy("volatile", volatile_month))
    
    return recommendations

def generate_detailed_marketing_plan(monthly_revenue, product_data=None):
    """
    Tạo kế hoạch marketing chi tiết dựa trên dữ liệu doanh thu
    """
    months = monthly_revenue['Month'].tolist()
    revenues = monthly_revenue['Revenue'].tolist()
    
    marketing_plan = {
        'seasonal_strategies': [],
        'budget_allocation': [],
        'campaign_suggestions': []
    }
    
    # Phân tích theo quý
    quarterly_revenue = {}
    for i, month in enumerate(months):
        quarter = f"Q{(month-1)//3 + 1}"
        if quarter not in quarterly_revenue:
            quarterly_revenue[quarter] = []
        quarterly_revenue[quarter].append(revenues[i])
    
    for quarter, rev_list in quarterly_revenue.items():
        avg_revenue = sum(rev_list) / len(rev_list)
        strategy = {
            'quarter': quarter,
            'avg_revenue': avg_revenue,
            'strategy': _get_quarterly_strategy(quarter, avg_revenue, max(revenues))
        }
        marketing_plan['seasonal_strategies'].append(strategy)
    
    return marketing_plan

def _get_quarterly_strategy(quarter, avg_revenue, max_revenue):
    """
    Tạo chiến lược theo quý
    """
    performance_ratio = avg_revenue / max_revenue
    
    if quarter == "Q1":
        if performance_ratio > 0.8:
            return "Tận dụng momentum đầu năm với New Year campaigns"
        else:
            return "Recovery strategy sau holiday season, focus on customer retention"
    elif quarter == "Q2":
        if performance_ratio > 0.8:
            return "Spring/Summer promotions, outdoor product focus"
        else:
            return "Mid-year boost campaigns, clearance sales"
    elif quarter == "Q3":
        if performance_ratio > 0.8:
            return "Back-to-school campaigns, summer finale sales"
        else:
            return "Preparation for Q4, inventory buildup"
    else:  # Q4
        if performance_ratio > 0.8:
            return "Holiday season maximization, premium pricing"
        else:
            return "Aggressive holiday promotions, bundle deals"

def analyze_market_opportunities(monthly_revenue, country_data=None):
    """
    Phân tích cơ hội thị trường từ dữ liệu doanh thu
    """
    opportunities = []
    months = monthly_revenue['Month'].tolist()
    revenues = monthly_revenue['Revenue'].tolist()
    
    # Tìm tháng có tiềm năng tăng trưởng
    avg_revenue = sum(revenues) / len(revenues)
    
    for i, (month, revenue) in enumerate(zip(months, revenues)):
        if revenue < avg_revenue * 0.7:  # Dưới 70% trung bình
            growth_potential = (avg_revenue - revenue) / revenue * 100
            opportunities.append({
                'month': month,
                'current_revenue': revenue,
                'growth_potential_pct': growth_potential,
                'recommendation': f"Tăng marketing budget cho tháng {month} - tiềm năng tăng trưởng {growth_potential:.1f}%"
            })
    
    return opportunities

def calculate_marketing_budget_allocation(total_budget, monthly_revenue):
    """
    Tính toán phân bổ ngân sách marketing dựa trên doanh thu các tháng
    """
    months = monthly_revenue['Month'].tolist()
    revenues = monthly_revenue['Revenue'].tolist()
    total_revenue = sum(revenues)
    
    allocations = []
    
    for month, revenue in zip(months, revenues):
        # Base allocation theo tỷ lệ doanh thu
        base_allocation = (revenue / total_revenue) * total_budget * 0.7
        
        # Bonus allocation cho tháng thấp điểm (để boost)
        avg_revenue = total_revenue / len(revenues)
        if revenue < avg_revenue:
            bonus = (avg_revenue - revenue) / avg_revenue * total_budget * 0.3
        else:
            bonus = 0
            
        month_budget = base_allocation + bonus
        
        allocations.append({
            'month': month,
            'budget': month_budget,
            'base_amount': base_allocation,
            'boost_amount': bonus,
            'strategy': 'Maintain momentum' if revenue >= avg_revenue else 'Growth acceleration'
        })
    
    return allocations 