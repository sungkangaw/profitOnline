import math
import csv
from inventory import Product
from sale import Sale
from utils import format_float


class Summary:
    def __init__(self):
        self.week = 0
        self.sales = {}
        self.order_quantity = 0
        self.item_quantity = 0
        self.total_unit_cost = 0
        self.total_cost = 0
        self.total_item_price = 0
        self.total_profit = 0
        self.total_profit_percentage = 0
        self.total_payment_fee = 0
        self.total_bonus = 0
        self.total_service_fee = 0
        self.total_net_profit = 0
        self.total_net_profit_percentage = 0
        self.total_shipping_fee_customer = 0
        self.total_shipping_fee_platform = 0
        self.total_shipping_fee_seller = 0
        self.total_shipping_fee_sum = 0

    def calculate_all(self):
        #Todo: optimize by looping only once
        self.order_quantity = len(dict.fromkeys([sale.order_number for sale in self.sales.values()]))
        self.item_quantity = len(self.sales)
        self.total_unit_cost = sum([sale.product.unit_cost for sale in self.sales.values()])
        self.total_cost = sum([sale.total_cost for sale in self.sales.values()])
        self.total_item_price = sum([sale.item_price for sale in self.sales.values()])
        self.total_profit = sum([sale.profit for sale in self.sales.values()])
        self.total_profit_percentage = sum([sale.net_profit for sale in self.sales.values()])/self.item_quantity
        self.total_payment_fee = sum([sale.payment_fee for sale in self.sales.values()])
        self.total_bonus = sum([sale.bonus for sale in self.sales.values()])
        self.total_service_fee = sum([sale.service_fee for sale in self.sales.values()])
        self.total_net_profit = sum([sale.net_profit for sale in self.sales.values()])
        self.total_net_profit_percentage = sum([sale.net_profit_percentage for sale in self.sales.values()])/self.item_quantity
        self.total_shipping_fee_customer = sum([sale.shipping_fee.customer for sale in self.sales.values()])
        self.total_shipping_fee_platform = sum([sale.shipping_fee.platform for sale in self.sales.values()])
        self.total_shipping_fee_seller = sum([sale.shipping_fee.seller for sale in self.sales.values()])
        self.total_shipping_fee_sum = sum([sale.shipping_fee.sum for sale in self.sales.values()])

    def get_total_row_for_csv(self):
        pass
