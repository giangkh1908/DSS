# 🚀 Hướng dẫn Chạy Ứng dụng DSS - 4 Chức năng

## 📋 Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

## 🎯 Chạy Ứng dụng

```bash
streamlit run dss_fe.py
```

## 🏗️ Cấu trúc Dự án

```
Long/
├── dss_fe.py                    # Entry point chính
├── controller/
│   ├── app_controller.py        # Controller chính điều phối 4 chức năng
│   ├── main_controller.py       # Controller phân bổ ngân sách 
│   ├── app_L.py                # Controller phân tích doanh thu quốc gia
│   ├── monthly_revenue_controller.py # Controller phân tích theo tháng
│   └── dol_controller.py       # Controller phân tích DOL
├── model/
│   ├── data_model.py           # Model cho phân bổ ngân sách (30-10-60)
│   ├── data_processing_L.py    # Model cho phân tích doanh thu
│   ├── analysis_L.py           # Logic phân tích doanh thu
│   └── decision_model.py       # Model cho phân tích DOL
├── view/
│   ├── ui_components.py        # UI components cho phân bổ ngân sách  
│   ├── plots_L.py             # Plots cho phân tích doanh thu
│   ├── dol_view.py            # View cho phân tích DOL
│   └── monthly_revenue_view.py # View cho phân tích tháng
└── data/
    └── online_retail.csv       # Dữ liệu mẫu
```

## 🌐 4 Chức năng Chính

### 🤖 1. Phân bổ Ngân sách
- **Controller**: `main_controller.py`
- **Model**: `data_model.py` 
- **Input**: File CSV dữ liệu khách hàng  
- **Output**: Kế hoạch phân bổ ngân sách 
- **Format**: `InvoiceDate, Country, CustomerID, Quantity, UnitPrice`
- **Tính năng**:
  - 30% cho sản phẩm chủ lực (doanh thu cao nhất)
  - 10% cho sản phẩm tiềm năng (tăng trưởng tốt)
  - 60% cho đa dạng hóa danh mục (giảm rủi ro)
  - Dự báo ROI với sai số ±10%

### 📈 2. Phân tích Doanh thu Quốc gia
- **Controller**: `app_L.py`
- **Model**: `data_processing_L.py`, `analysis_L.py`
- **Input**: File CSV/Excel dữ liệu bán hàng
- **Output**: Phân tích doanh thu theo quốc gia + xu hướng
- **Format**: `InvoiceDate, Country, Revenue`
- **Tính năng**:
  - So sánh doanh thu các quốc gia
  - Tính tốc độ tăng trưởng YoY
  - Phân tích thị phần (pie chart)
  - Phân tích mùa vụ (seasonal patterns)

### 📅 3. Phân tích Doanh thu Theo Tháng  
- **Controller**: `monthly_revenue_controller.py`
- **View**: `monthly_revenue_view.py`
- **Input**: File CSV dữ liệu bán hàng
- **Output**: Xu hướng theo tháng + gợi ý chiến lược
- **Format**: `InvoiceDate, Description, Quantity, UnitPrice`
- **Tính năng**:
  - Biểu đồ xu hướng theo tháng
  - Phân loại tháng: Cao điểm, Thấp điểm, Biến động, Ổn định
  - Action plan cho từng loại tháng
  - Dự báo seasonal forecasting

### 🔢 4. Phân tích DOL (Degree of Operating Leverage)
- **Controller**: `dol_controller.py`
- **Model**: `decision_model.py`
- **View**: `dol_view.py`
- **Input**: Chi phí cố định, biến đổi + dữ liệu sản phẩm
- **Output**: DOL analysis + sensitivity analysis
- **Format**: `InvoiceDate, StockCode, Quantity, UnitPrice`
- **Tính năng**:
  - Tính toán DOL theo từng tháng
  - Phân tích độ nhạy cảm hoạt động
  - Dự báo leverage forecasting
  - Strategic recommendations

## 🔄 Cách Hoạt động

1. **Khởi động**: Chạy `dss_fe.py` → Hiển thị menu 4 chức năng
2. **Chọn chức năng**: Click button tương ứng (🤖📈📅🔢)
3. **Upload dữ liệu**: Upload file theo format yêu cầu
4. **Cấu hình**: Thiết lập tham số phân tích
5. **Phân tích**: Hệ thống xử lý và hiển thị kết quả
6. **Quay lại**: Mỗi chức năng có nút "⬅️ Quay lại Menu"

## ✨ Tính năng Nổi bật

### 🤖 Recommendations (Phân bổ Ngân sách)
- **Mô hình 30-10-60**: Phân bổ thông minh theo tỷ lệ vàng
- **Country-wise analysis**: Phân tích chi tiết từng quốc gia
- **Product portfolio**: Tối ưu danh mục sản phẩm
- **ROI forecasting**: Dự báo lợi nhuận với độ chính xác cao

### 📊 Advanced Analytics (Phân tích Doanh thu)
- **Multi-country comparison**: So sánh đa quốc gia
- **Growth rate calculation**: Tính toán tăng trưởng YoY
- **Market share analysis**: Phân tích thị phần chi tiết
- **Seasonal patterns**: Nhận diện mùa vụ kinh doanh

### 📈 Pattern Recognition (Phân tích Tháng)
- **4 loại tháng**: Cao điểm, Thấp điểm, Biến động, Ổn định
- **Strategic insights**: Gợi ý chiến lược cho từng pattern
- **Action planning**: Kế hoạch hành động cụ thể
- **Trend forecasting**: Dự báo xu hướng tương lai

### 🔢 Financial Analysis (DOL)
- **Leverage calculation**: Tính toán đòn bẩy hoạt động
- **Sensitivity analysis**: Phân tích độ nhạy cảm
- **Risk assessment**: Đánh giá rủi ro tài chính
- **Strategic recommendations**: Khuyến nghị chiến lược


## 🛠️ Troubleshooting

### Lỗi Import Controllers
```bash
❌ Lỗi Import: No module named 'monthly_revenue_controller'
```
**Giải pháp**: Kiểm tra file `monthly_revenue_controller.py` và `dol_controller.py` tồn tại

### Lỗi Data Format
```bash
❌ Lỗi khi đọc file: Invalid CSV format
```
**Giải pháp**: 
- Phân bổ Ngân sách: `InvoiceDate, Country, CustomerID, Quantity, UnitPrice`
- Phân tích Quốc gia: `InvoiceDate, Country, Revenue`  
- Phân tích Tháng: `InvoiceDate, Description, Quantity, UnitPrice`
- Phân tích DOL: `InvoiceDate, StockCode, Quantity, UnitPrice`

### Lỗi Memory/Performance
- Cache được tự động áp dụng với `@st.cache_data`
- Restart app: `Ctrl+C` → `streamlit run dss_fe.py`
- Giảm kích thước file dữ liệu nếu cần

### Lỗi Method Missing
```bash
❌ Lỗi Method: 'MainController' object has no attribute '_handle_main_logic'
```
**Giải pháp**: Kiểm tra method trong `main_controller.py`

## 📈 Performance Tips

1. **File size**: Khuyến nghị < 50MB cho tốc độ tối ưu
2. **Date format**: Sử dụng `DD/MM/YYYY` hoặc `YYYY-MM-DD`
3. **Memory**: Restart app sau mỗi 5-10 lần phân tích
4. **Browser**: Sử dụng Chrome/Firefox để có trải nghiệm tốt nhất

## 🔗 Quick Start

1. Clone project: `git clone <repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run app: `streamlit run dss_fe.py`
4. Access: `http://localhost:8501`
5. Upload data và bắt đầu phân tích!

## 📝 Version Info

- **Version**: 2.0
- **Architecture**: MVC Pattern
- **Framework**: Streamlit 
- **Last Update**: June 2025
- **Python**: 3.8+
