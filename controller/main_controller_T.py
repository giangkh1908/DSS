from model.decision_model import DecisionModel
from view.main_view import MainView

class MainController:
    def __init__(self):
        self.model = DecisionModel()
        self.view = MainView(self)

    def run(self):
        """Start the GUI application"""
        self.view.run()

    def calculate_dol(self, variable_cost, fixed_cost, time_period, product_code):
        """Handle DOL calculation from input screen"""
        try:
            # Call model to perform DOL calculation
            results = self.model.calculate_dol(
                variable_cost=variable_cost,
                fixed_cost=fixed_cost,
                time_period=time_period,
                product_code=product_code
            )
            
            # Show results screen
            self.view.show_results_screen(results)
            
        except Exception as e:
            # Handle errors (view will show error message)
            raise e

    def get_product_data(self, product_code):
        """Get historical data for a specific product"""
        return self.model.get_product_data(product_code)

    def get_available_products(self):
        """Get list of available products"""
        return self.model.get_available_products() 