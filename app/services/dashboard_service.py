from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:
    """
    Business logic for Dashboard.
    """

    def __init__(self, db):
        self.repository = DashboardRepository(db)

    def get_dashboard_data(self):
        return {
            "total_products": self.repository.total_products(),
            "total_customers": self.repository.total_customers(),
            "total_suppliers": self.repository.total_suppliers(),
            "total_invoices": self.repository.total_invoices(),
            "total_sales": self.repository.total_sales(),
            "low_stock_products": self.repository.low_stock_products(),
            "recent_invoices": self.repository.recent_invoices(),
        }