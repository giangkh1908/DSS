import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from typing import Dict, Any, List

class DOLResultsView:
    def __init__(self, parent, controller, results_data: Dict[str, Any]):
        self.parent = parent
        self.controller = controller
        self.results_data = results_data
        self.analysis_boxes = []  # Store references to analysis boxes
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame with scrollbar
        self.main_canvas = tk.Canvas(self.parent)
        self.scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.main_canvas.pack(side="left", fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(
            self.scrollable_frame, 
            text="Kết quả", 
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Summary Table
        self.create_summary_table()
        
        # Chart
        self.create_dol_chart()
        
        # Detailed Analysis Boxes
        self.create_analysis_boxes()
        
        # Back Button
        self.create_back_button()
        
    def create_summary_table(self):
        """Create the summary table with DOL forecasts"""
        # Table frame
        table_frame = ttk.LabelFrame(self.scrollable_frame, text="Bảng tóm tắt DOL", padding="10")
        table_frame.pack(fill="x", padx=20, pady=10)
        
        # Table headers
        headers = ["Thời gian", "DOL", "Độ nhạy cảm (DOL)", "So với trước", "Phân tích & Hành động"]
        
        for col, header in enumerate(headers):
            header_label = ttk.Label(
                table_frame, 
                text=header, 
                font=("Arial", 11, "bold"),
                relief="solid",
                borderwidth=1,
                padding=5
            )
            header_label.grid(row=0, column=col, sticky="ew", padx=1, pady=1)
        
        # Generate table data
        table_data = self.generate_table_data()
        
        # Table rows
        for row, data in enumerate(table_data, start=1):
            for col, value in enumerate(data):
                if col == 4:  # "Phân tích & Hành động" column
                    # Create clickable link
                    link_label = tk.Label(
                        table_frame,
                        text=str(value),
                        font=("Arial", 10, "underline"),
                        relief="solid",
                        borderwidth=1,
                        padx=5,
                        pady=5,
                        wraplength=150,
                        fg="blue",
                        cursor="hand2"
                    )
                    link_label.grid(row=row, column=col, sticky="ew", padx=1, pady=1)
                    
                    # Bind click event to scroll to corresponding analysis box
                    month = row  # Row corresponds to month
                    link_label.bind("<Button-1>", lambda e, m=month: self.scroll_to_analysis(m))
                    link_label.bind("<Enter>", lambda e, label=link_label: self.on_link_hover(label, True))
                    link_label.bind("<Leave>", lambda e, label=link_label: self.on_link_hover(label, False))
                else:
                    cell_label = ttk.Label(
                        table_frame,
                        text=str(value),
                        font=("Arial", 10),
                        relief="solid",
                        borderwidth=1,
                        padding=5,
                        wraplength=150
                    )
                    cell_label.grid(row=row, column=col, sticky="ew", padx=1, pady=1)
        
        # Configure grid weights
        for i in range(5):
            table_frame.columnconfigure(i, weight=1)
            
    def on_link_hover(self, label, is_hovering):
        """Handle link hover effects"""
        if is_hovering:
            label.configure(fg="red")
        else:
            label.configure(fg="blue")
    
    def scroll_to_analysis(self, month: int):
        """Scroll to the corresponding analysis box"""
        if 1 <= month <= len(self.analysis_boxes):
            # Get the analysis box widget
            analysis_box = self.analysis_boxes[month - 1]
            
            # Calculate the position to scroll to
            box_y = analysis_box.winfo_rooty() - self.scrollable_frame.winfo_rooty()
            
            # Scroll to the analysis box
            self.main_canvas.yview_moveto(box_y / self.scrollable_frame.winfo_height())
            
            # Highlight the analysis box briefly
            self.highlight_analysis_box(analysis_box)
    
    def highlight_analysis_box(self, analysis_box):
        """Briefly highlight the analysis box"""
        # For ttk widgets, we'll use a different approach
        # Change the text color of the title to highlight
        for child in analysis_box.winfo_children():
            if isinstance(child, ttk.Label) and "Phân tích tháng" in child.cget("text"):
                original_fg = child.cget("foreground")
                child.configure(foreground="red")
                # Reset after 2 seconds
                self.parent.after(2000, lambda: child.configure(foreground=original_fg))
                break
            
    def get_selected_months(self):
        """Return the number of months to forecast based on user selection"""
        time_period = self.results_data.get('time_period', '1 tháng tới')
        if '3' in time_period:
            return 3
        elif '2' in time_period:
            return 2
        else:
            return 1

    def generate_table_data(self):
        """Generate table data based on results and selected months"""
        data = []
        base_dol = self.results_data.get('dol', 0)
        months_to_show = self.get_selected_months()
        for month in range(1, months_to_show + 1):
            time_text = f"{month} tháng tới"
            dol_value = base_dol * (1 + (month - 1) * 0.1)
            sensitivity = self.get_sensitivity_level(dol_value)
            comparison = self.get_comparison_text(month, dol_value)
            analysis_ref = f"Xem phân tích tháng {month}"
            data.append([time_text, f"{dol_value:.2f}", sensitivity, comparison, analysis_ref])
        return data
    
    def get_sensitivity_level(self, dol_value: float) -> str:
        """Determine sensitivity level based on DOL value"""
        if dol_value > 2.0:
            return "Cao"
        elif dol_value >= 1.2:
            return "Trung bình"
        else:
            return "Thấp"
    
    def get_comparison_text(self, month: int, dol_value: float) -> str:
        """Get comparison text for the period"""
        if month == 1:
            return "Cơ sở"
        elif dol_value > 2.0:
            return "Tăng"
        elif dol_value < 1.2:
            return "Giảm"
        else:
            return "Giữ nguyên"
    
    def create_dol_chart(self):
        """Create the DOL chart"""
        chart_frame = ttk.LabelFrame(self.scrollable_frame, text="Biểu đồ DOL theo từng tháng", padding="10")
        chart_frame.pack(fill="x", padx=20, pady=10)
        fig, ax = plt.subplots(figsize=(10, 6))
        months_to_show = self.get_selected_months()
        months = list(range(1, months_to_show + 1))
        dol_values = []
        base_dol = self.results_data.get('dol', 0)
        for month in months:
            dol_value = base_dol * (1 + (month - 1) * 0.1)
            dol_values.append(dol_value)
        ax.plot(months, dol_values, marker='o', linewidth=2, markersize=8, color='blue')
        ax.set_xlabel('Tháng', fontsize=12)
        ax.set_ylabel('DOL', fontsize=12)
        ax.set_title('DOL Forecast Trend', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(months)
        for i, (x, y) in enumerate(zip(months, dol_values)):
            ax.annotate(f'{y:.2f}', (x, y), textcoords="offset points", xytext=(0,10), ha='center')
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def create_analysis_boxes(self):
        """Create detailed analysis boxes for each period"""
        analysis_frame = ttk.LabelFrame(self.scrollable_frame, text="Phân tích chi tiết", padding="10")
        analysis_frame.pack(fill="x", padx=20, pady=10)
        self.analysis_boxes = []
        months_to_show = self.get_selected_months()
        for month in range(1, months_to_show + 1):
            analysis_box = self.create_analysis_box(analysis_frame, month)
            self.analysis_boxes.append(analysis_box)
    
    def create_analysis_box(self, parent, month: int):
        """Create individual analysis box"""
        box_frame = ttk.LabelFrame(parent, text=f"Phân tích tháng {month}", padding="10")
        box_frame.pack(fill="x", pady=5)
        
        # Analysis & Action Plan
        analysis_label = ttk.Label(
            box_frame,
            text="Phân tích & lựa chọn phương án:",
            font=("Arial", 11, "bold")
        )
        analysis_label.pack(anchor="w", pady=(0, 5))
        
        analysis_text = self.get_analysis_text(month)
        analysis_content = ttk.Label(
            box_frame,
            text=analysis_text,
            font=("Arial", 10),
            wraplength=600,
            justify="left"
        )
        analysis_content.pack(anchor="w", pady=(0, 10))
        
        # Suggested Strategies
        strategies_label = ttk.Label(
            box_frame,
            text="Gợi ý chiến lược:",
            font=("Arial", 11, "bold")
        )
        strategies_label.pack(anchor="w", pady=(0, 5))
        
        strategies_text = self.get_strategies_text(month)
        strategies_content = ttk.Label(
            box_frame,
            text=strategies_text,
            font=("Arial", 10),
            wraplength=600,
            justify="left"
        )
        strategies_content.pack(anchor="w", pady=(0, 10))
        
        # Note
        note_label = ttk.Label(
            box_frame,
            text="Lưu ý:",
            font=("Arial", 11, "bold")
        )
        note_label.pack(anchor="w", pady=(0, 5))
        
        note_text = self.get_note_text(month)
        note_content = ttk.Label(
            box_frame,
            text=note_text,
            font=("Arial", 10),
            wraplength=600,
            justify="left",
            foreground="red"
        )
        note_content.pack(anchor="w", pady=(0, 10))
        
        return box_frame
    
    def get_analysis_text(self, month: int) -> str:
        """Get analysis text for the month"""
        base_dol = self.results_data.get('dol', 0)
        dol_value = base_dol * (1 + (month - 1) * 0.1)
        
        if dol_value > 2.0:
            return f"Tháng {month} có DOL cao ({dol_value:.2f}): Lợi nhuận thay đổi đáng kể khi doanh thu biến động, cho thấy rủi ro cao nhưng cũng có tiềm năng lợi nhuận cao. Cần thận trọng trong quản lý rủi ro và chuẩn bị kế hoạch dự phòng."
        elif dol_value >= 1.2:
            return f"Tháng {month} có DOL trung bình ({dol_value:.2f}): Khả năng sinh lời tương đối ổn định với những thay đổi vừa phải trong doanh thu. Đây là mức độ cân bằng tốt giữa rủi ro và cơ hội."
        else:
            return f"Tháng {month} có DOL thấp ({dol_value:.2f}): Ít nhạy cảm với thay đổi doanh thu, cho thấy tính ổn định cao. Công ty có thể tập trung vào tăng trưởng doanh thu mà không lo ngại về rủi ro cao."
    
    def get_strategies_text(self, month: int) -> str:
        """Get strategies text for the month"""
        base_dol = self.results_data.get('dol', 0)
        dol_value = base_dol * (1 + (month - 1) * 0.1)
        
        if dol_value > 2.0:
            return "1. Tập trung vào chiến dịch marketing ngắn hạn để tạo đà tăng trưởng doanh số\n2. Tăng cường quản lý rủi ro và dự trữ tài chính\n3. Tối ưu hóa quy trình sản xuất để giảm chi phí\n4. Theo dõi chặt chẽ biến động thị trường"
        elif dol_value >= 1.2:
            return "1. Tăng đầu tư R&D để nâng cao biên lợi nhuận và tăng cường khả năng cạnh tranh\n2. Tập trung vào phát triển thương hiệu và tăng lòng trung thành khách hàng\n3. Cân bằng giữa tăng trưởng và ổn định\n4. Đa dạng hóa danh mục sản phẩm"
        else:
            return "1. Nhấn mạnh tính tin cậy, chất lượng và ổn định của sản phẩm\n2. Mở rộng thị trường và tăng cường marketing\n3. Xem xét giảm đầu tư R&D nếu không mang lại cải tiến rõ ràng\n4. Tối ưu hóa giá cả và chi phí"
    
    def get_note_text(self, month: int) -> str:
        """Get note text for the month"""
        base_dol = self.results_data.get('dol', 0)
        dol_value = base_dol * (1 + (month - 1) * 0.1)
        
        if dol_value > 2.0:
            return f"⚠️ CẢNH BÁO: DOL tháng {month} cao ({dol_value:.2f}). Rủi ro thị trường lớn, cần thận trọng trong mọi quyết định đầu tư và mở rộng. Tập trung vào chiến dịch marketing ngắn hạn."
        elif dol_value >= 1.2:
            return f"✅ DOL tháng {month} ở mức trung bình ({dol_value:.2f}). Khuyến nghị tăng đầu tư R&D và tập trung vào phát triển thương hiệu dài hạn."
        else:
            return f"✅ DOL tháng {month} ở mức thấp ({dol_value:.2f}). Có thể thực hiện các chiến lược tăng trưởng với rủi ro thấp. Nhấn mạnh tính ổn định và chất lượng."
    
    def create_back_button(self):
        """Create back button to return to input screen"""
        button_frame = ttk.Frame(self.scrollable_frame)
        button_frame.pack(pady=20)
        
        back_button = ttk.Button(
            button_frame,
            text="Quay lại nhập liệu",
            command=self.go_back_to_input,
            style="Accent.TButton"
        )
        back_button.pack()
        
        # Style configuration
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 12, "bold"))
    
    def go_back_to_input(self):
        """Return to input screen"""
        self.controller.show_input_screen() 