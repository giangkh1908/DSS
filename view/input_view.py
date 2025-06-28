import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

class DOLInputView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.product_data = []  # Store product data for search
        self.setup_ui()
        self.load_product_codes()
    
    def setup_ui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.parent, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="Dự đoán DOL", 
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Variable Cost Input
        ttk.Label(self.main_frame, text="Chi phí biến đổi:", font=("Arial", 12)).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.variable_cost_var = tk.StringVar()
        self.variable_cost_entry = ttk.Entry(
            self.main_frame, 
            textvariable=self.variable_cost_var,
            width=30,
            font=("Arial", 11)
        )
        self.variable_cost_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Fixed Cost Input
        ttk.Label(self.main_frame, text="Chi phí cố định:", font=("Arial", 12)).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.fixed_cost_var = tk.StringVar()
        self.fixed_cost_entry = ttk.Entry(
            self.main_frame, 
            textvariable=self.fixed_cost_var,
            width=30,
            font=("Arial", 11)
        )
        self.fixed_cost_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Time Period Dropdown
        ttk.Label(self.main_frame, text="Khoảng thời gian:", font=("Arial", 12)).grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        self.time_period_var = tk.StringVar()
        self.time_period_combo = ttk.Combobox(
            self.main_frame,
            textvariable=self.time_period_var,
            values=["1 tháng tới", "2 tháng tới", "3 tháng tới"],
            state="readonly",
            width=27,
            font=("Arial", 11)
        )
        self.time_period_combo.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        self.time_period_combo.set("1 tháng tới")  # Default value
        
        # Product Code Search and Dropdown
        ttk.Label(self.main_frame, text="Mã sản phẩm:", font=("Arial", 12)).grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        
        # Search frame for product
        product_search_frame = ttk.Frame(self.main_frame)
        product_search_frame.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Search entry
        self.product_search_var = tk.StringVar()
        self.product_search_entry = ttk.Entry(
            product_search_frame,
            textvariable=self.product_search_var,
            width=20,
            font=("Arial", 11)
        )
        self.product_search_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Add placeholder text as a label
        placeholder_label = ttk.Label(
            product_search_frame,
            text="Tìm kiếm mã hoặc mô tả...",
            font=("Arial", 9),
            foreground="gray"
        )
        placeholder_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Search button
        self.search_button = ttk.Button(
            product_search_frame,
            text="Tìm",
            command=self.search_products,
            width=8
        )
        self.search_button.pack(side=tk.LEFT)
        
        # Product Code Dropdown
        self.product_code_var = tk.StringVar()
        self.product_code_combo = ttk.Combobox(
            self.main_frame,
            textvariable=self.product_code_var,
            state="readonly",
            width=27,
            font=("Arial", 11)
        )
        self.product_code_combo.grid(row=5, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Calculate Button
        self.calculate_button = ttk.Button(
            self.main_frame,
            text="Tính DOL",
            command=self.calculate_dol,
            style="Accent.TButton"
        )
        self.calculate_button.grid(row=6, column=0, columnspan=2, pady=30)
        
        # Configure grid weights
        self.main_frame.columnconfigure(1, weight=1)
        
        # Style configuration
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 12, "bold"))
        
        # Bind search on Enter key
        self.product_search_entry.bind('<Return>', lambda e: self.search_products())
    
    def load_product_codes(self):
        """Load product codes and descriptions from the Excel file"""
        try:
            # Path to the Excel file
            excel_path = r"C:\Users\PC\Documents\DSS_MVC\online_retail.xlsx"
            
            if os.path.exists(excel_path):
                # Read the Excel file
                df = pd.read_excel(excel_path)
                
                # Get unique products with both StockCode and Description
                if 'StockCode' in df.columns:
                    # Create product data list
                    self.product_data = []
                    
                    # Group by StockCode and get unique descriptions
                    if 'Description' in df.columns:
                        # Get unique combinations of StockCode and Description
                        unique_products = df[['StockCode', 'Description']].drop_duplicates()
                        
                        for _, row in unique_products.iterrows():
                            stock_code = str(row['StockCode']) if not pd.isna(row['StockCode']) else ""
                            description = str(row['Description']) if not pd.isna(row['Description']) else ""
                            
                            # Create display text
                            display_text = f"{stock_code} - {description[:50]}{'...' if len(description) > 50 else ''}"
                            
                            self.product_data.append({
                                'stock_code': stock_code,
                                'description': description,
                                'display_text': display_text
                            })
                    else:
                        # If no Description column, just use StockCode
                        unique_codes = df['StockCode'].unique()
                        for code in unique_codes:
                            if not pd.isna(code):
                                stock_code = str(code)
                                self.product_data.append({
                                    'stock_code': stock_code,
                                    'description': "",
                                    'display_text': stock_code
                                })
                    
                    # Sort by stock code
                    self.product_data.sort(key=lambda x: x['stock_code'])
                    
                    # Update the combobox with all products initially
                    self.update_product_dropdown(self.product_data)
                    
                    if self.product_data:
                        self.product_code_combo.set(self.product_data[0]['stock_code'])
                else:
                    messagebox.showwarning("Warning", "StockCode column not found in the Excel file")
            else:
                messagebox.showerror("Error", f"Excel file not found at: {excel_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading product codes: {str(e)}")
    
    def search_products(self):
        """Search products by StockCode or Description"""
        search_term = self.product_search_var.get().strip().lower()
        
        if not search_term:
            # If search is empty, show all products
            self.update_product_dropdown(self.product_data)
            return
        
        # Filter products based on search term
        filtered_products = []
        for product in self.product_data:
            stock_code = product['stock_code'].lower()
            description = product['description'].lower()
            
            # Check if search term matches StockCode or Description
            if search_term in stock_code or search_term in description:
                filtered_products.append(product)
        
        # Update dropdown with filtered results
        self.update_product_dropdown(filtered_products)
        
        # Show search results count
        if filtered_products:
            self.product_code_combo.set(filtered_products[0]['stock_code'])
            if len(filtered_products) == 1:
                messagebox.showinfo("Tìm kiếm", f"Tìm thấy 1 sản phẩm")
            else:
                messagebox.showinfo("Tìm kiếm", f"Tìm thấy {len(filtered_products)} sản phẩm")
        else:
            messagebox.showinfo("Tìm kiếm", "Không tìm thấy sản phẩm nào")
            # Reset to all products
            self.update_product_dropdown(self.product_data)
    
    def update_product_dropdown(self, products):
        """Update the product dropdown with the given product list"""
        # Create display values for dropdown
        display_values = [product['display_text'] for product in products]
        
        # Update combobox values
        self.product_code_combo['values'] = display_values
        
        # Store the mapping of display text to stock code
        self.display_to_stockcode = {product['display_text']: product['stock_code'] for product in products}
        
        # Bind selection event to update the actual stock code
        self.product_code_combo.bind('<<ComboboxSelected>>', self.on_product_selected)
    
    def on_product_selected(self, event):
        """Handle product selection from dropdown"""
        selected_display = self.product_code_combo.get()
        if selected_display in self.display_to_stockcode:
            # Update the variable with the actual stock code
            self.product_code_var.set(self.display_to_stockcode[selected_display])
    
    def calculate_dol(self):
        """Handle the calculate DOL button click"""
        try:
            # Validate inputs
            variable_cost = float(self.variable_cost_var.get())
            fixed_cost = float(self.fixed_cost_var.get())
            time_period = self.time_period_var.get()
            product_code = self.product_code_var.get()
            
            if not all([variable_cost, fixed_cost, time_period, product_code]):
                messagebox.showwarning("Warning", "Please fill in all fields")
                return
            
            # Call controller method to perform calculation
            self.controller.calculate_dol(
                variable_cost=variable_cost,
                fixed_cost=fixed_cost,
                time_period=time_period,
                product_code=product_code
            )
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for costs")
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating DOL: {str(e)}")
    
    def get_input_values(self):
        """Return current input values"""
        return {
            'variable_cost': self.variable_cost_var.get(),
            'fixed_cost': self.fixed_cost_var.get(),
            'time_period': self.time_period_var.get(),
            'product_code': self.product_code_var.get()
        }
    
    def clear_inputs(self):
        """Clear all input fields"""
        self.variable_cost_var.set("")
        self.fixed_cost_var.set("")
        self.time_period_combo.set("1 tháng tới")
        self.product_search_var.set("")
        if self.product_data:
            self.update_product_dropdown(self.product_data)
            self.product_code_combo.set(self.product_data[0]['stock_code']) 