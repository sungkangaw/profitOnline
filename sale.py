from inventory import Product


class ShippingFee:
    def __init__(self):
        self.seller = 0.0
        self.customer = 0.0
        self.platform = 0.0
        self.sum = 0.0

    def get_sum(self):
        self.sum = self.customer + self.platform + self.seller
        return self.sum


class Sale:
    def __init__(self):
        self.week = "N/A"
        self.parent_sku = ""
        self.sku = "N/A"
        self.details = "N/A"
        self.order_number = ""
        self.item_number = ""
        self.item_price = 0.0
        self.quantity = 0
        self.total_cost = 0
        self.shipping_fee = ShippingFee()
        self.payment_fee = 0
        self.bonus = 0
        self.service_fee = 0
        self.product = Product()
        self.profit = 0
        self.profit_percentage = 0
        self.net_profit = 0
        self.net_profit_percentage = 0

    def calculate_all_data(self):
        self.total_cost = self.product.unit_cost * self.quantity
        self.profit = self.item_price - self.total_cost
        self.profit_percentage = self.profit/self.item_price*100 if self.item_price > 0 else 0
        self.net_profit = self.profit - self.payment_fee - self.service_fee - self.bonus
        self.net_profit_percentage = self.net_profit/self.item_price*100 if self.item_price > 0 else 0

    def get_row_for_csv(self):
        pass
