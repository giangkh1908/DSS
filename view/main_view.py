import tkinter as tk
from tkinter import ttk
from view.input_view import DOLInputView
from view.results_view import DOLResultsView

class MainView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.setup_main_window()
        self.current_view = None
        
    def setup_main_window(self):
        """Setup the main application window"""
        self.root.title("DSS - Decision Support System")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Set theme
        style = ttk.Style()
        style.theme_use('clam')
        
    def show_input_screen(self):
        """Show the DOL input screen"""
        # Clear any existing view
        if self.current_view:
            for widget in self.root.winfo_children():
                widget.destroy()
            self.setup_main_window()
        
        # Create and show input view
        self.current_view = DOLInputView(self.root, self.controller)
        
    def show_results_screen(self, results_data):
        """Show the results screen"""
        # Clear current view
        if self.current_view:
            for widget in self.root.winfo_children():
                widget.destroy()
            self.setup_main_window()
        
        # Create results view
        self.current_view = DOLResultsView(self.root, self.controller, results_data)
        
    def run(self):
        """Start the application"""
        self.show_input_screen()
        self.root.mainloop()
        
    def close(self):
        """Close the application"""
        self.root.quit()
        self.root.destroy()

    def show_decision(self, decision):
        print("Decision:", decision)

    def get_user_input(self):
        return input("Enter data: ") 