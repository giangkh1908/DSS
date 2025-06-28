import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta

# Hàm để đọc và làm sạch dữ liệu
@st.cache_data(ttl=3600)  # Cache dữ liệu trong 1 giờ
def load_and_clean_data(file_path):
    df = pd.read_excel(
        file_path,
        usecols=['InvoiceDate', 'Country', 'Revenue'],
        parse_dates=['InvoiceDate']
    )
    df = df.loc[df['Revenue'] > 0]
    df['MonthYear'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    df = df.reset_index(drop=True)
    return df

# Hàm để đọc và làm sạch dữ liệu từ file upload
@st.cache_data(ttl=3600)
def load_and_clean_data_from_upload(uploaded_file, file_type):
    """Load và clean dữ liệu từ file upload"""
    try:
        if file_type == 'csv':
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        else:  # excel
            df = pd.read_excel(uploaded_file)
        
        # Xử lý cột ngày
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
        
        # Tính Revenue nếu chưa có
        if 'Revenue' not in df.columns:
            if 'Quantity' in df.columns and 'UnitPrice' in df.columns:
                df['Revenue'] = df['Quantity'] * df['UnitPrice']
            else:
                raise ValueError("File cần có cột 'Revenue' hoặc cả 'Quantity' và 'UnitPrice'")
        
        # Lọc dữ liệu hợp lệ
        df = df.loc[df['Revenue'] > 0]
        df = df.dropna(subset=['InvoiceDate', 'Country', 'Revenue'])
        
        # Tạo cột MonthYear
        df['MonthYear'] = df['InvoiceDate'].dt.to_period('M').astype(str)
        df = df.reset_index(drop=True)
        
        return df
        
    except Exception as e:
        raise Exception(f"Lỗi xử lý file: {str(e)}")

@st.cache_data(ttl=3600)
def filter_data(df, start_date, end_date, countries, revenue_threshold):
    df_filtered = df.copy(deep=False)
    start_period = pd.Period(start_date.strftime('%Y-%m'))
    end_period = pd.Period(end_date.strftime('%Y-%m'))
    df_periods = pd.Series(df_filtered['MonthYear'].map(lambda x: pd.Period(x)))
    mask = (df_periods >= start_period) & (df_periods <= end_period)
    df_filtered = df_filtered.loc[mask]
    if countries:
        df_filtered = df_filtered[df_filtered['Country'].isin(countries)]
    if revenue_threshold > 0:
        country_revenue = df_filtered.groupby('Country')['Revenue'].sum()
        valid_countries = country_revenue[country_revenue >= revenue_threshold].index
        df_filtered = df_filtered[df_filtered['Country'].isin(valid_countries)]
    return df_filtered

@st.cache_data(ttl=3600)
def calculate_total_revenue(df):
    pivot_table = df.pivot_table(
        values='Revenue',
        index='MonthYear',
        columns='Country',
        aggfunc='sum',
        fill_value=0
    )
    return pivot_table

@st.cache_data(ttl=3600)
def calculate_percentage_change(pivot_table):
    growth_rate = (pivot_table.pct_change() * 100).round(1)
    return growth_rate

@st.cache_data(ttl=3600)
def compare_total_revenue(pivot_table):
    total_revenue = pivot_table.sum()
    return total_revenue

@st.cache_data(ttl=3600)
def analyze_seasonality(df):
    df['Month'] = df['InvoiceDate'].dt.month
    monthly_revenue = df.groupby('Month')['Revenue'].mean()
    threshold = monthly_revenue.mean() + monthly_revenue.std()
    peak_months = monthly_revenue[monthly_revenue >= threshold].index.tolist()
    df['Quarter'] = df['InvoiceDate'].dt.quarter
    quarterly_revenue = df.groupby('Quarter')['Revenue'].sum()
    quarterly_proportion = (quarterly_revenue / quarterly_revenue.sum() * 100).round(2)
    return monthly_revenue, peak_months, quarterly_proportion

@st.cache_data(ttl=3600)
def analyze_country_performance(df):
    country_metrics = pd.DataFrame()
    country_metrics['Total_Revenue'] = df.groupby('Country')['Revenue'].sum()
    df['Year'] = df['InvoiceDate'].dt.year
    yearly_revenue = df.pivot_table(
        values='Revenue', 
        index='Country',
        columns='Year',
        aggfunc='sum',
        fill_value=0
    )
    years = sorted(df['Year'].unique())
    if len(years) >= 2:
        yoy_growth = ((yearly_revenue[years[-1]] / yearly_revenue[years[-2]]) - 1) * 100
        country_metrics['YoY_Growth'] = yoy_growth
    monthly_revenue = df.groupby(['Country', 'MonthYear'])['Revenue'].sum().reset_index()
    country_metrics['Stability'] = monthly_revenue.groupby('Country')['Revenue'].agg(lambda x: (x.std() / x.mean()) * 100)
    return country_metrics

def apply_currency_threshold(df, threshold_amount):
    """Áp dụng ngưỡng tiền tệ để lọc giao dịch"""
    if threshold_amount > 0:
        df = df[df['Revenue'] >= threshold_amount]
    return df

def apply_quantity_threshold(df, threshold_qty):
    """Áp dụng ngưỡng số lượng để lọc giao dịch"""
    if threshold_qty > 0:
        df = df[df['Quantity'] >= threshold_qty]
    return df

def apply_product_filter(df, excluded_products):
    """Áp dụng bộ lọc loại trừ sản phẩm"""
    if excluded_products:
        df = df[~df['StockCode'].isin(excluded_products)]
    return df

def apply_time_range_filter(df, start_date, end_date):
    """Áp dụng bộ lọc thời gian"""
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
    if start_date:
        df = df[df['InvoiceDate'] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df['InvoiceDate'] <= pd.to_datetime(end_date)]
    return df

def format_large_number(number):
    """Format số lớn thành dạng K, M, B"""
    if number >= 1_000_000_000:
        return f"{number/1_000_000_000:.1f}B"
    elif number >= 1_000_000:
        return f"{number/1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number/1_000:.1f}K"
    else:
        return f"{number:.0f}"

def calculate_growth_rate(current, previous):
    """Tính tỷ lệ tăng trưởng"""
    if previous == 0:
        return float('inf') if current > 0 else 0
    return ((current - previous) / previous) * 100

def analyze_product_performance(df):
    """Phân tích hiệu quả sản phẩm"""
    product_stats = df.groupby(['StockCode', 'Description']).agg({
        'Quantity': 'sum',
        'Revenue': 'sum',
        'InvoiceNo': 'nunique'
    }).reset_index()
    
    product_stats.columns = ['StockCode', 'Description', 'Total_Quantity', 'Total_Revenue', 'Total_Orders']
    product_stats['Avg_Order_Value'] = product_stats['Total_Revenue'] / product_stats['Total_Orders']
    
    return product_stats.sort_values('Total_Revenue', ascending=False)

def analyze_customer_segments(df):
    """Phân tích phân khúc khách hàng"""
    customer_stats = df.groupby('CustomerID').agg({
        'Revenue': ['sum', 'count'],
        'InvoiceNo': 'nunique',
        'InvoiceDate': ['min', 'max']
    }).reset_index()
    
    customer_stats.columns = ['CustomerID', 'Total_Revenue', 'Total_Items', 'Total_Orders', 'First_Purchase', 'Last_Purchase']
    customer_stats['Avg_Order_Value'] = customer_stats['Total_Revenue'] / customer_stats['Total_Orders']
    customer_stats['Purchase_Frequency'] = customer_stats['Total_Orders']
    
    return customer_stats

def get_top_products(df, n=10, metric='Revenue'):
    """Lấy top sản phẩm theo metric"""
    product_performance = analyze_product_performance(df)
    metric_col = f'Total_{metric}'
    if metric_col in product_performance.columns:
        return product_performance.nlargest(n, metric_col)
    return product_performance.head(n)

def get_time_series_data(df, frequency='M'):
    """Tạo dữ liệu chuỗi thời gian"""
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df_ts = df.set_index('InvoiceDate')
    
    if frequency == 'M':
        return df_ts.groupby(pd.Grouper(freq='M')).agg({
            'Revenue': 'sum',
            'Quantity': 'sum',
            'InvoiceNo': 'nunique'
        }).reset_index()
    elif frequency == 'D':
        return df_ts.groupby(pd.Grouper(freq='D')).agg({
            'Revenue': 'sum',
            'Quantity': 'sum',
            'InvoiceNo': 'nunique'
        }).reset_index()
    elif frequency == 'W':
        return df_ts.groupby(pd.Grouper(freq='W')).agg({
            'Revenue': 'sum',
            'Quantity': 'sum', 
            'InvoiceNo': 'nunique'
        }).reset_index()
    
    return df_ts

def detect_outliers(df, column='Revenue', method='iqr'):
    """Phát hiện outliers"""
    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    elif method == 'zscore':
        z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
        return df[z_scores > 3]
    
    return pd.DataFrame()

def clean_data_basic(df):
    """Làm sạch dữ liệu cơ bản"""
    df = df.copy()
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)
    df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce').fillna(0)
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    
    df = df.dropna(subset=['InvoiceDate', 'CustomerID'])
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0]
    
    return df

# Functions from src/utils/data_processing.py
def load_data(file_path):
    """Load the dataset from a CSV file or file-like object."""
    data = pd.read_csv(file_path)
    return data

def preprocess_data(data):
    """Tiền xử lý dữ liệu: tạo cột Month và tính lại Revenue."""
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    data['Month'] = data['InvoiceDate'].dt.month
    data['Quantity'] = pd.to_numeric(data['Quantity'], errors='coerce').fillna(0)
    data['UnitPrice'] = pd.to_numeric(data['UnitPrice'], errors='coerce').fillna(0)
    data['Revenue'] = data['Quantity'] * data['UnitPrice']
    return data

def calculate_monthly_revenue(data):
    """Calculate total revenue for each month."""
    monthly_revenue = data.groupby('Month')['Revenue'].sum().reset_index()
    return monthly_revenue

def identify_peak_low_months(monthly_revenue):
    """Identify peak and low months based on revenue."""
    peak_month = monthly_revenue.loc[monthly_revenue['Revenue'].idxmax()]
    low_month = monthly_revenue.loc[monthly_revenue['Revenue'].idxmin()]
    return peak_month, low_month

def calculate_revenue_variation(monthly_revenue):
    """Calculate the variation in revenue between months."""
    monthly_revenue['Variation'] = monthly_revenue['Revenue'].diff()
    return monthly_revenue

def analyze_trend(monthly_revenue):
    """Phân tích xu hướng doanh thu chi tiết"""
    months = monthly_revenue['Month'].tolist()
    revenues = monthly_revenue['Revenue'].tolist()
    result = []

    # 1. Tháng cao điểm nhất
    peak_idx = np.argmax(revenues)
    peak_month = months[peak_idx]
    peak_value = revenues[peak_idx]
    result.append(
        f"**Tháng cao điểm nhất:**\nTháng {peak_month} có doanh thu cao nhất, đạt {peak_value:,.0f} đơn vị tiền tệ. "
        "Đây có thể là thời điểm có chương trình khuyến mãi lớn, mùa lễ hội hoặc nhu cầu thị trường tăng cao. "
        "Doanh nghiệp nên tận dụng tháng này để đẩy mạnh marketing và gia tăng trữ hàng."
    )

    # 2. Tháng thấp điểm nhất
    low_idx = np.argmin(revenues)
    low_month = months[low_idx]
    low_value = revenues[low_idx]
    result.append(
        f"**Tháng thấp điểm nhất:**\nTháng {low_month} ghi nhận doanh thu thấp nhất, chỉ đạt {low_value:,.0f} đơn vị tiền tệ. "
        "Đây có thể là tháng thấp điểm do yếu tố mùa vụ, thời tiết hoặc thói quen tiêu dùng. "
        "Doanh nghiệp nên cân nhắc các biện pháp kích cầu trong tháng này."
    )

    # 3. Xu hướng ổn định (±15% trung bình)
    avg = np.mean(revenues)
    lower = avg * 0.85
    upper = avg * 1.15
    stable_months = [months[i] for i, rev in enumerate(revenues) if lower <= rev <= upper]
    if stable_months:
        result.append(
            f"**Xu hướng ổn định:**\nDoanh thu trong các tháng {stable_months} duy trì ở mức ổn định, dao động trong khoảng {lower:,.0f} đến {upper:,.0f} đơn vị. "
            "Đây là những tháng bình thường, ít chịu tác động từ các sự kiện lớn."
        )
        for i, rev in enumerate(revenues):
            if months[i] in stable_months:
                result.append(
                    f"- Tháng {months[i]} có doanh thu ổn định ở mức {rev:,.0f} đơn vị."
                )

    # 4. Xu hướng tăng dần cuối năm
    if len(revenues) >= 2 and revenues[-2] < revenues[-1] and revenues[-1] > np.mean(revenues[:-2]):
        result.append(
            f"**Xu hướng tăng dần cuối năm:**\nDoanh thu có xu hướng tăng mạnh vào các tháng cuối năm, cụ thể tháng {months[-2]} đạt {revenues[-2]:,.0f}, tháng {months[-1]} đạt {revenues[-1]:,.0f}. "
            "Đây là tín hiệu tích cực từ các chương trình mua sắm cuối năm hoặc nhu cầu trang trí, quà tặng dịp lễ hội."
        )

    # 5. Xu hướng giảm dần giữa năm
    if len(revenues) > 4:
        mid = len(revenues) // 2
        if revenues[mid] < np.mean(revenues[:mid]):
            mid_months = months[mid-1:mid+2]
            result.append(
                f"**Xu hướng giảm dần giữa năm:**\nDoanh thu có xu hướng giảm nhẹ vào giữa năm, đặc biệt trong các tháng {mid_months}. "
                "Doanh nghiệp cần theo dõi kỹ và cân nhắc triển khai các chiến dịch kích cầu hoặc ưu đãi trong giai đoạn này."
            )

    # 6. Biến động doanh thu đột ngột
    max_pct = 0
    max_idx = None
    for i in range(1, len(revenues)):
        if revenues[i-1] == 0:
            continue
        diff = revenues[i] - revenues[i-1]
        pct = abs(diff) / revenues[i-1]
        if pct > max_pct:
            max_pct = pct
            max_idx = i
    if max_idx is not None and max_pct > 0.3:
        diff = revenues[max_idx] - revenues[max_idx-1]
        result.append(
            f"**Biến động doanh thu đột ngột:**\nTháng {months[max_idx]} ghi nhận sự biến động lớn nhất về doanh thu so với tháng trước, với mức {'tăng' if diff>0 else 'giảm'} {abs(diff):,.0f} đơn vị. "
            "Doanh nghiệp nên rà soát nguyên nhân, có thể do các sự kiện bất thường hoặc hiệu quả của chiến dịch marketing."
        )

    # 7. Xu hướng tăng trưởng ổn định cả năm
    if all(revenues[i] <= revenues[i+1] for i in range(len(revenues)-1)):
        result.append(
            "**Xu hướng tăng trưởng ổn định cả năm:**\nDoanh thu có xu hướng tăng trưởng ổn định xuyên suốt năm, phản ánh sự cải thiện tích cực trong hoạt động kinh doanh và chiến lược marketing hiệu quả."
        )

    # 8. Xu hướng suy giảm liên tục
    if all(revenues[i] >= revenues[i+1] for i in range(len(revenues)-1)):
        result.append(
            "**Xu hướng suy giảm liên tục:**\nDoanh thu cho thấy xu hướng giảm liên tục theo thời gian. Doanh nghiệp cần nhanh chóng phân tích nguyên nhân và có các biện pháp khắc phục như điều chỉnh giá bán, tăng cường quảng bá hoặc làm mới sản phẩm."
        )

    return result