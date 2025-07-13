# DSS - Decision Support System - Complete MVC Implementation

## 🎯 Tổng Quan Hệ Thống

Hệ thống hỗ trợ quyết định tích hợp hoàn chỉnh với **4 chức năng chính** theo kiến trúc **MVC thuần túy**.

## 🏗️ Cấu Trúc MVC Hoàn Chỉnh

```
Long/
├── dss_fe.py                       # 🚀 MAIN ENTRY POINT
│
├── controller/                     # 🎮 CONTROLLER LAYER
│   ├── app_controller.py          # Main app controller (4 modes)
│   ├── main_controller.py         # Budget allocation controller
│   ├── app_L.py                   # Country revenue analysis controller  
│   ├── monthly_revenue_controller.py # Monthly analysis controller
│   ├── revenue_analysis_controller.py # Product revenue controller
│   └── dol_controller.py          # DOL analysis controller (NEW)
│
├── model/                         # 📊 MODEL LAYER  
│   ├── data_model.py              # Core data & AI models
│   ├── decision_model.py          # DOL calculation model (UPDATED)
│   ├── data_processing_L.py       # Data processing functions
│   ├── marketing_strategies_model.py # Marketing business logic
│   ├── analysis_L.py              # Analysis models
│   └── monthly_revenue_model.py   # Monthly revenue models
│
├── view/                          # 🎨 VIEW LAYER
│   ├── ui_components.py           # Main UI components
│   ├── monthly_revenue_view.py    # Monthly revenue UI
│   ├── plots_L.py                 # Plotting UI
│   ├── revenue_analysis_view.py   # Product analysis UI
│   ├── dol_view.py                # DOL analysis UI (NEW)
│   ├── input_view.py              # Input forms
│   ├── main_view.py               # Main views
│   └── results_view.py            # Results display
│
├── components/                    # 🔧 SHARED COMPONENTS
│   └── charts.py                  # All chart functions
│
├── data/                         # 📈 DATA
│   └── online_retail.csv         # Sample dataset
│
└── styles/                       # 🎨 STYLING
    └── custom.css                # Application styles
```

## 🌟 4 Chức Năng Chính

### 1. 🤖 **Phân bổ Ngân sách**
- **Controller**: `main_controller.py`
- **Model**: `data_model.py`
- **View**: `ui_components.py`
- **Chức năng**: budget allocation 
- **Input**: Customer data CSV
- **Output**: Smart budget recommendations với ROI forecasting

### 2. 📈 **Phân tích Doanh thu Quốc gia**
- **Controller**: `app_L.py`
- **Model**: `analysis_L.py`
- **View**: `plots_L.py`
- **Chức năng**: Revenue analysis by country với growth trends
- **Input**: Revenue data CSV/Excel
- **Output**: Country comparison và revenue forecasting

### 3. 📅 **Phân tích Tháng**
- **Controller**: `revenue_analysis_controller.py`
- **Model**: `data_processing_L.py`, `marketing_strategies_model.py`
- **View**: `revenue_analysis_view.py`
- **Chức năng**: Monthly product revenue analysis với marketing insights
- **Input**: Sales data CSV
- **Output**: Monthly trends, peak/low analysis, strategic recommendations

### 4. 🔢 **Phân tích DOL** (Degree of Operating Leverage)
- **Controller**: `dol_controller.py` 
- **Model**: `decision_model.py` 
- **View**: `dol_view.py` 
- **Chức năng**: DOL calculation, sensitivity analysis, leverage forecasting
- **Input**: Cost parameters + product data
- **Output**: DOL metrics, monthly charts, strategic recommendations

## 🔥 Tính Năng Mới - DOL Analysis

### Quy Trình Hoạt Động
1. **Input**: Nhập chi phí biến đổi, chi phí cố định
2. **Product Selection**: Chọn sản phẩm từ database
3. **Time Selection**: Chọn khoảng thời gian dự báo
4. **Calculation**: Tính toán DOL và độ nhạy cảm
5. **Visualization**: Biểu đồ DOL theo từng tháng
6. **Recommendations**: Khuyến nghị chiến lược dựa trên DOL

### Công Thức DOL
```
DOL = Contribution Margin / (Contribution Margin - Fixed Cost)
```

### Phân Loại Độ Nhạy Cảm
- **DOL > 0.5**: Độ nhạy cảm cao → Chiến lược tăng trưởng mạnh
- **DOL = 0.5**: Độ nhạy cảm trung bình → Chiến lược cân bằng
- **DOL < 0.5**: Độ nhạy cảm thấp → Chiến lược bền vững

## 📱 Giao Diện Người Dùng

### Layout Chính
- **4 cột** cho 4 chức năng chính
- **Responsive design** với cards tương tác
- **Navigation sidebar** cho từng module
- **Back button** để quay lại menu chính

### Tính Năng UI/UX
- ✅ **Interactive cards** với hover effects
- ✅ **Color-coded modules** để dễ phân biệt
- ✅ **Progress indicators** cho calculations
- ✅ **Error handling** với debug information
- ✅ **Responsive layout** cho mobile/desktop


## 🚀 Khởi Chạy Ứng Dụng

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python -m streamlit run dss_fe.py
```

## 📊 Dependencies

```txt
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.24.0
plotly>=5.15.0
google-generativeai>=0.3.0
scikit-learn>=1.3.0
openpyxl>=3.0.0
matplotlib>=3.6.0
seaborn>=0.12.0
```

## 🎛️ Navigation Flow

1. **Start**: `dss_fe.py` → `AppController`
2. **Menu**: 4-column selection interface
3. **Module**: Dedicated controller for each feature
4. **Processing**: Model handles business logic
5. **Display**: View renders results với charts
6. **Navigation**: Back to menu or continue analysis

## 🔄 Luồng Dữ Liệu

```
User Input → Controller → Model → Data Processing → Results → View → UI Display
     ↑                                                              ↓
     ←←←←←←←←←←←←← User Actions ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

## 🎯 Future Enhancements

1. **Real-time Data Integration**
2. **Advanced AI Models** 
3. **Export Functionality** (PDF, Excel)
4. **User Authentication**
5. **Dashboard Customization**
6. **API Integration**
7. **Mobile App Version**

## 📈 Performance

- ⚡ **Fast Loading**: Streamlit caching
- 📊 **Efficient Charting**: Plotly optimization
- 💾 **Memory Management**: Pandas optimization
- 🔄 **State Management**: Session state handling

---