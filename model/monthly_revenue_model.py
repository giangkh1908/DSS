"""
Model cho chức năng phân tích doanh thu theo tháng
"""

import pandas as pd
import numpy as np

class MonthlyRevenueModel:
    def __init__(self):
        self.data = None
        self.monthly_revenue = None
    
    def load_data(self, file_path):
        """Load the dataset from a CSV file or file-like object."""
        try:
            data = pd.read_csv(file_path)
            return data, None
        except Exception as e:
            return None, str(e)
    
    def preprocess_data(self, data):
        """Tiền xử lý dữ liệu: tạo cột Month và tính lại Revenue."""
        try:
            data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
            data['Month'] = data['InvoiceDate'].dt.month
            data['Quantity'] = pd.to_numeric(data['Quantity'], errors='coerce').fillna(0)
            data['UnitPrice'] = pd.to_numeric(data['UnitPrice'], errors='coerce').fillna(0)
            data['Revenue'] = data['Quantity'] * data['UnitPrice']
            self.data = data
            return data, None
        except Exception as e:
            return None, str(e)
    
    def calculate_monthly_revenue(self, data):
        """Calculate total revenue for each month."""
        try:
            monthly_revenue = data.groupby('Month')['Revenue'].sum().reset_index()
            self.monthly_revenue = monthly_revenue
            return monthly_revenue, None
        except Exception as e:
            return None, str(e)
    
    def identify_peak_low_months(self, monthly_revenue):
        """Identify peak and low months based on revenue."""
        try:
            peak_month = monthly_revenue.loc[monthly_revenue['Revenue'].idxmax()]
            low_month = monthly_revenue.loc[monthly_revenue['Revenue'].idxmin()]
            return peak_month, low_month, None
        except Exception as e:
            return None, None, str(e)
    
    def calculate_revenue_variation(self, monthly_revenue):
        """Calculate the variation in revenue between months."""
        try:
            monthly_revenue['Variation'] = monthly_revenue['Revenue'].diff()
            return monthly_revenue, None
        except Exception as e:
            return None, str(e)
    
    def get_volatility_month(self, monthly_revenue):
        """Tính tháng biến động mạnh nhất (theo phần trăm so với tháng trước, lớn nhất và >30%)"""
        try:
            revenues = monthly_revenue['Revenue'].tolist()
            months = monthly_revenue['Month'].astype(int).tolist()
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
                return months[max_idx], None
            else:
                return None, None
        except Exception as e:
            return None, str(e)
    
    def get_stable_months(self, monthly_revenue):
        """Các tháng ổn định (±15% trung bình)"""
        try:
            avg = monthly_revenue['Revenue'].mean()
            lower = avg * 0.85
            upper = avg * 1.15
            stable_months = monthly_revenue[
                (monthly_revenue['Revenue'] >= lower) & (monthly_revenue['Revenue'] <= upper)
            ]['Month'].astype(int).tolist()
            return stable_months, None
        except Exception as e:
            return None, str(e)
    
    def analyze_trend(self, monthly_revenue):
        """Phân tích xu hướng chi tiết"""
        try:
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

            # 4. Xu hướng tăng dần cuối năm
            if len(revenues) >= 2 and revenues[-2] < revenues[-1] and revenues[-1] > np.mean(revenues[:-2]):
                result.append(
                    f"**Xu hướng tăng dần cuối năm:**\nDoanh thu có xu hướng tăng mạnh vào các tháng cuối năm, cụ thể tháng {months[-2]} đạt {revenues[-2]:,.0f}, tháng {months[-1]} đạt {revenues[-1]:,.0f}. "
                    "Đây là tín hiệu tích cực từ các chương trình mua sắm cuối năm hoặc nhu cầu trang trí, quà tặng dịp lễ hội."
                )

            # 5. Biến động doanh thu đột ngột
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

            # 6. Xu hướng tăng trưởng ổn định cả năm
            if all(revenues[i] <= revenues[i+1] for i in range(len(revenues)-1)):
                result.append(
                    "**Xu hướng tăng trưởng ổn định cả năm:**\nDoanh thu có xu hướng tăng trưởng ổn định xuyên suốt năm, phản ánh sự cải thiện tích cực trong hoạt động kinh doanh và chiến lược marketing hiệu quả."
                )

            # 7. Xu hướng suy giảm liên tục
            if all(revenues[i] >= revenues[i+1] for i in range(len(revenues)-1)):
                result.append(
                    "**Xu hướng suy giảm liên tục:**\nDoanh thu cho thấy xu hướng giảm liên tục theo thời gian. Doanh nghiệp cần nhanh chóng phân tích nguyên nhân và có các biện pháp khắc phục như điều chỉnh giá bán, tăng cường quảng bá hoặc làm mới sản phẩm."
                )

            return result, None
        except Exception as e:
            return None, str(e)
