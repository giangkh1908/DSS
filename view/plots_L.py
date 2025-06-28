import matplotlib.pyplot as plt
import streamlit as st
import calendar

def plot_results(pivot_table, growth_rate, total_revenue, country_metrics, monthly_revenue, quarterly_proportion, analysis_types):
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

def plot_revenue_comparison_ratios(total_revenue):
    top_country = total_revenue.idxmax()
    top_revenue = total_revenue[top_country]
    comparison_data = {}
    for country in total_revenue.index:
        if country != top_country:
            ratio = top_revenue / total_revenue[country]
            comparison_data[country] = ratio
    if not comparison_data:
        return
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    countries = list(comparison_data.keys())
    ratios = list(comparison_data.values())
    bars = ax1.bar(countries, ratios, color='skyblue', alpha=0.7)
    ax1.set_title(f'Tỷ lệ doanh thu: {top_country} so với các quốc gia khác')
    ax1.set_xlabel('Quốc gia')
    ax1.set_ylabel(f'Số lần gấp {top_country}')
    ax1.tick_params(axis='x', rotation=45)
    for bar, ratio in zip(bars, ratios):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{ratio:.1f}x', ha='center', va='bottom', fontweight='bold')
    revenues = [total_revenue[country] for country in countries]
    revenues.append(top_revenue)
    all_countries = countries + [top_country]
    colors = ['lightcoral'] * len(countries) + ['gold']
    bars2 = ax2.bar(all_countries, revenues, color=colors, alpha=0.7)
    ax2.set_title('So sánh doanh thu tuyệt đối')
    ax2.set_xlabel('Quốc gia')
    ax2.set_ylabel('Doanh thu (£)')
    ax2.tick_params(axis='x', rotation=45)
    for bar, revenue in zip(bars2, revenues):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(revenues)*0.01,
                f'{revenue:,.0f}', ha='center', va='bottom', fontsize=8)
    plt.tight_layout()
    st.pyplot(plt)
    plt.close() 