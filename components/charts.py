import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def plot_monthly_revenue(monthly_revenue):
    """Tạo biểu đồ doanh thu theo tháng với plotly để tương tác tốt hơn"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=monthly_revenue['Month'],
        y=monthly_revenue['Revenue'],
        name='Doanh thu',
        marker_color='lightblue',
        text=[f"{val:,.0f}" for val in monthly_revenue['Revenue']],
        textposition='auto',
        hovertemplate='<b>Tháng %{x}</b><br>Doanh thu: %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="📊 Doanh Thu Theo Tháng",
        xaxis_title="Tháng",
        yaxis_title="Doanh thu",
        xaxis=dict(tickmode='linear'),
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_monthly_revenue_matplotlib(monthly_revenue):
    """Tạo biểu đồ matplotlib cho monthly revenue - compatible với dss-revenue-analysis"""
    plt.figure(figsize=(10, 6))
    bars = plt.bar(monthly_revenue['Month'], monthly_revenue['Revenue'], color='skyblue')
    plt.xlabel('Tháng', fontsize=14)
    plt.ylabel('Doanh thu', fontsize=14)
    plt.xticks(monthly_revenue['Month'])

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f"{yval:,.0f}", ha='center', va='bottom', fontsize=12, color='black')

    plt.tight_layout()
    st.pyplot(plt)

def plot_monthly_revenue_plotly(monthly_revenue):
    """Tạo biểu đồ plotly interactive cho monthly revenue"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=monthly_revenue['Month'],
        y=monthly_revenue['Revenue'],
        name='Doanh thu',
        marker_color='lightblue',
        text=[f"{val:,.0f}" for val in monthly_revenue['Revenue']],
        textposition='auto',
        hovertemplate='<b>Tháng %{x}</b><br>Doanh thu: %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="📊 Doanh Thu Theo Tháng",
        xaxis_title="Tháng",
        yaxis_title="Doanh thu",
        xaxis=dict(tickmode='linear'),
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_revenue_chart(monthly_revenue):
    """Legacy function for compatibility với các MVC components"""
    return plot_monthly_revenue_plotly(monthly_revenue)
