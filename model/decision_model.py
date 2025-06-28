import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from typing import Optional, List, Dict, Any

class DecisionModel:
    def __init__(self):
        self.data = []
        # Use flexible path for CSV data
        self.csv_path = self._find_data_file()
        self.df: Optional[pd.DataFrame] = None
        self.load_data()
    
    def _find_data_file(self) -> str:
        """Find the online_retail.csv file in various possible locations"""
        possible_paths = [
            "data/online_retail.csv",  # MVC structure
            "online_retail.csv",       # Current directory
            os.path.join(os.path.dirname(__file__), "..", "data", "online_retail.csv"),  # Relative to model
            r"C:\Users\PC\Documents\DSS_MVC\online_retail.csv"  # Original hardcoded path as fallback
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # If none found, return the MVC structure path (will show error in load_data)
        return "data/online_retail.csv"
    
    def load_data(self):
        """Load data from CSV file"""
        try:
            if os.path.exists(self.csv_path):
                # Read first few rows to check columns
                sample_df = pd.read_csv(self.csv_path, nrows=1)
                date_columns = []
                
                # Check for common date column names
                for col in sample_df.columns:
                    if 'date' in col.lower() or 'time' in col.lower():
                        date_columns.append(col)
                
                # Load with date parsing if date columns found
                if date_columns:
                    self.df = pd.read_csv(self.csv_path, parse_dates=date_columns)
                else:
                    self.df = pd.read_csv(self.csv_path)
                    
                print(f"✅ Data loaded successfully from: {self.csv_path}")
                print(f"📊 Dataset shape: {self.df.shape}")
                print(f"📋 Columns: {list(self.df.columns)}")
                
            else:
                print(f"❌ CSV file not found at: {self.csv_path}")
                print("💡 Available paths checked:")
                for path in [
                    "data/online_retail.csv",
                    "online_retail.csv", 
                    os.path.join(os.path.dirname(__file__), "..", "data", "online_retail.csv")
                ]:
                    status = "✅ Found" if os.path.exists(path) else "❌ Not found"
                    print(f"   {status}: {path}")
                    
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
    
    def get_available_products(self) -> List[str]:
        """Get list of available product codes"""
        if self.df is not None and 'StockCode' in self.df.columns:
            # Remove NaN values and convert to string
            products = self.df['StockCode'].dropna().astype(str).unique()
            return sorted(products.tolist())
        return []
    
    def get_product_data(self, product_code: str) -> Optional[pd.DataFrame]:
        """Get historical data for a specific product"""
        if self.df is None:
            return None
        
        # Filter data for the specific product
        product_data = self.df[self.df['StockCode'].astype(str) == str(product_code)].copy()
        
        if product_data.empty:
            return None
        
        # Sort by date if InvoiceDate exists
        if 'InvoiceDate' in product_data.columns:
            product_data = product_data.sort_values(by='InvoiceDate', ascending=True)
        
        return product_data
    
    def get_available_years(self) -> List[int]:
        """Get list of available years in the dataset"""
        if self.df is None or 'InvoiceDate' not in self.df.columns:
            return []
        
        # Handle non-datetime columns
        try:
            if not pd.api.types.is_datetime64_any_dtype(self.df['InvoiceDate']):
                self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'], errors='coerce')
            
            available_years = sorted(self.df['InvoiceDate'].dt.year.dropna().unique().astype(int).tolist())
            return available_years
        except Exception as e:
            print(f"Error getting available years: {str(e)}")
            return []
    
    def get_monthly_dol_data(self, product_code: str, variable_cost: float, fixed_cost: float, year: Optional[int] = None) -> Dict[int, float]:
        """Get DOL data for each month in a specific year"""
        product_data = self.get_product_data(product_code)
        if product_data is None or product_data.empty:
            return {}
        
        # If no year specified, use the most recent year with data
        if year is None:
            available_years = self.get_available_years()
            if not available_years:
                return {}
            year = max(available_years)
        
        monthly_dol = {}
        
        # Filter data for the specific year
        if 'InvoiceDate' in product_data.columns:
            try:
                # Ensure InvoiceDate is datetime
                if not pd.api.types.is_datetime64_any_dtype(product_data['InvoiceDate']):
                    product_data['InvoiceDate'] = pd.to_datetime(product_data['InvoiceDate'], errors='coerce')
                
                year_data = product_data[product_data['InvoiceDate'].dt.year == year].copy()
                
                if year_data.empty:
                    return {}
                
                # Calculate DOL for each month
                for month in range(1, 13):
                    month_data = year_data[year_data['InvoiceDate'].dt.month == month]
                    
                    if not month_data.empty:
                        # Calculate DOL for this month
                        avg_unit_price = month_data['UnitPrice'].mean()
                        total_quantity = month_data['Quantity'].sum()
                        
                        revenue = total_quantity * avg_unit_price
                        contribution_margin = total_quantity * (avg_unit_price - variable_cost)
                        
                        if contribution_margin - fixed_cost != 0:
                            dol = contribution_margin / (contribution_margin - fixed_cost)
                            # Clamp DOL to reasonable range to avoid extreme values
                            dol = max(-10, min(10, dol))
                        else:
                            dol = 0
                        
                        monthly_dol[month] = dol
            except Exception as e:
                print(f"Error calculating monthly DOL: {str(e)}")
                return {}
        
        return monthly_dol
    
    def forecast_quantity(self, product_code: str, time_period: str) -> float:
        """Forecast quantity for the specified time period"""
        product_data = self.get_product_data(product_code)
        
        if product_data is None or product_data.empty:
            return 0.0
        
        # Get the latest 3 months of data
        if 'InvoiceDate' in product_data.columns:
            try:
                # Ensure InvoiceDate is datetime
                if not pd.api.types.is_datetime64_any_dtype(product_data['InvoiceDate']):
                    product_data['InvoiceDate'] = pd.to_datetime(product_data['InvoiceDate'], errors='coerce')
                
                latest_date = product_data['InvoiceDate'].max()
                three_months_ago = latest_date - timedelta(days=90)
                recent_data = product_data[product_data['InvoiceDate'] >= three_months_ago]
            except:
                recent_data = product_data
        else:
            recent_data = product_data
        
        if recent_data.empty:
            return 0.0
        
        # Calculate average quantity per transaction
        avg_quantity = recent_data['Quantity'].mean()
        
        # Simple forecast: average quantity * number of months
        months_map = {"1 tháng tới": 1, "2 tháng tới": 2, "3 tháng tới": 3}
        months = months_map.get(time_period, 1)
        
        forecasted_quantity = avg_quantity * months
        
        return max(0.0, forecasted_quantity)
    
    def calculate_dol(self, variable_cost: float, fixed_cost: float, time_period: str, product_code: str, selected_year: Optional[int] = None) -> Dict[str, Any]:
        """Calculate Degree of Operating Leverage (DOL)"""
        try:
            # Get product data
            product_data = self.get_product_data(product_code)
            
            if product_data is None or product_data.empty:
                raise ValueError(f"No data found for product code: {product_code}")
            
            # Get average unit price
            avg_unit_price = product_data['UnitPrice'].mean()
            
            # Forecast quantity
            forecasted_quantity = self.forecast_quantity(product_code, time_period)
            
            # Calculate revenue
            revenue = forecasted_quantity * avg_unit_price
            
            # Calculate contribution margin
            contribution_margin = forecasted_quantity * (avg_unit_price - variable_cost)
            
            # Calculate DOL
            if contribution_margin - fixed_cost != 0:
                dol = contribution_margin / (contribution_margin - fixed_cost)
                # Clamp DOL to reasonable range
                dol = max(-10, min(10, dol))
            else:
                dol = float('inf')
            
            # Calculate profit
            profit = contribution_margin - fixed_cost
            
            # Get monthly DOL data for the selected year
            monthly_dol_data = self.get_monthly_dol_data(product_code, variable_cost, fixed_cost, selected_year)
            
            # Get the year used for monthly data
            available_years = self.get_available_years()
            data_year = max(available_years) if available_years else None
            
            # Use selected year if provided, otherwise use data year
            analysis_year = selected_year if selected_year is not None else data_year
            
            # Prepare results
            results = {
                'product_code': product_code,
                'time_period': time_period,
                'forecasted_quantity': forecasted_quantity,
                'avg_unit_price': avg_unit_price,
                'variable_cost': variable_cost,
                'fixed_cost': fixed_cost,
                'revenue': revenue,
                'contribution_margin': contribution_margin,
                'profit': profit,
                'dol': dol,
                'monthly_dol_data': monthly_dol_data,
                'data_year': data_year,
                'selected_year': analysis_year,
                'historical_data': product_data.tail(10).to_dict(orient='records')
            }
            
            return results
            
        except Exception as e:
            raise Exception(f"Error calculating DOL: {str(e)}")
    
    def add_data(self, item):
        """Add data item"""
        self.data.append(item)

    def make_decision(self):
        """Make decision based on data"""
        if not self.data:
            return "No data available"
        
        return f"Decision made based on {len(self.data)} data points" 