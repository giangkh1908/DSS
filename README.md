# 🚀 Hướng dẫn Chạy Ứng dụng DSS - 3 Chức năng

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
│   ├── app_controller.py        # Controller chính điều phối 3 chức năng
│   ├── main_controller.py       # Controller phân bổ ngân sách AI
│   ├── app_L.py                # Controller phân tích doanh thu quốc gia
│   └── monthly_revenue_controller.py # Controller phân tích theo tháng
├── model/
│   ├── data_model.py           # Model cho phân bổ ngân sách
│   ├── data_processing_L.py    # Model cho phân tích doanh thu
│   └── analysis_L.py           # Logic phân tích doanh thu
└── view/
    ├── ui_components.py        # UI components cho phân bổ ngân sách
    └── plots_L.py             # Plots cho phân tích doanh thu
```

## 🌐 3 Chức năng Chính

### 🤖 1. Phân bổ Ngân sách AI
- **Controller**: `main_controller.py`
- **Input**: File CSV dữ liệu khách hàng  
- **Output**: Kế hoạch phân bổ ngân sách + AI recommendations
- **Format**: `InvoiceDate, Country, CustomerID, Quantity, UnitPrice`

### 📈 2. Phân tích Doanh thu Quốc gia
- **Controller**: `app_L.py`
- **Input**: File CSV/Excel dữ liệu bán hàng
- **Output**: Phân tích doanh thu theo quốc gia + xu hướng
- **Format**: `InvoiceDate, Country, Revenue`

### 📅 3. Phân tích Doanh thu Theo Tháng  
- **Controller**: `monthly_revenue_controller.py`
- **Input**: File CSV dữ liệu bán hàng
- **Output**: Xu hướng theo tháng + gợi ý chiến lược
- **Format**: `InvoiceDate, Description, Quantity, UnitPrice`

## 🔄 Cách Hoạt động

1. **Khởi động**: Chạy `dss_fe.py` → Hiển thị menu 3 chức năng
2. **Chọn chức năng**: Click button tương ứng
3. **Upload dữ liệu**: Upload file theo format yêu cầu
4. **Phân tích**: Hệ thống xử lý và hiển thị kết quả
5. **Quay lại**: Mỗi chức năng có nút "Quay lại Menu"

## ✨ Tính năng Mới

### 📅 Phân tích Theo Tháng
- **Xu hướng doanh thu**: Biểu đồ line chart và bar chart
- **Phân loại tháng**: Cao điểm, thấp điểm, biến động, ổn định
- **Gợi ý chiến lược**: Dựa trên từng loại tháng
- **Kế hoạch hành động**: Action plan chi tiết

### 🎯 Phân tích Pattern
- **Tháng cao điểm**: Chiến lược tối đa hóa cơ hội
- **Tháng thấp điểm**: Biện pháp kích cầu
- **Tháng biến động**: Phản ứng nhanh với thay đổi
- **Tháng ổn định**: Tối ưu hiệu quả

## 📊 So sánh 3 Chức năng

| Tính năng | Phân bổ Ngân sách | Phân tích Quốc gia | Phân tích Tháng |
|-----------|---------------------|-------------------|----------------|
| **Đối tượng** | Marketing Manager | Sales Analyst | Business Analyst |
| **Input** | Customer Data | Revenue Data | Sales Data |
| **AI Support** | ✅ Smart Recommendations | ✅ Trend Analysis | ✅ Pattern Recognition |
| **Output** | Budget Plan | Country Analysis | Monthly Trends |
| **Forecasting** | ROI Prediction | Growth Prediction | Seasonal Forecasting |

## 🛠️ Troubleshooting

### Lỗi Import
- Kiểm tra file `monthly_revenue_controller.py` tồn tại
- Đảm bảo cấu trúc thư mục đúng

### Lỗi Data Format
- Kiểm tra format file CSV theo yêu cầu
- Đảm bảo có đầy đủ các cột cần thiết

### Lỗi Performance  
- Cache được sử dụng để tối ưu tốc độ
- Restart app nếu gặp vấn đề về memory
