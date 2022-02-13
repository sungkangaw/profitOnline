import csv
from sale import Sale
from utils import format_float
from summary import Summary
from inventory import Product
from config import Config

class ShopeeSummary(Summary):
    def get_total_row_for_csv(self):
        self.calculate_all()
        return [
            "",
            "Shopee",
            self.order_quantity,
            self.item_quantity,
            "",
            "",
            "",
            "",
            "",
            "",
            format_float(self.total_cost),
            format_float(self.total_item_price),
            format_float(self.total_profit),
            format_float(self.total_profit_percentage),
            format_float(self.total_payment_fee),
            format_float(self.total_bonus),
            format_float(self.total_service_fee),
            format_float(self.total_net_profit),
            format_float(self.total_net_profit_percentage),
            format_float(self.total_shipping_fee_customer),
            format_float(self.total_shipping_fee_platform),
            format_float(self.total_shipping_fee_seller),
            format_float(self.total_shipping_fee_sum),
            ""
        ]


class ShopeeSale(Sale):
    def __init__(self):
        super().__init__()
        self.province = ""
        self.district = ""
        self.parcel_tracking_no = ""

    def get_row_for_csv(self):
        self.calculate_all_data()
        return [
            self.week,
            "Shopee",
            self.order_number,
            self.item_number,
            self.parent_sku,
            self.sku,
            self.product.stock,
            self.details,
            str(self.quantity),
            str(self.product.unit_cost),
            str(self.total_cost),
            str(self.item_price),
            str(self.profit),
            format_float(self.profit_percentage),
            str(self.payment_fee),
            str(self.bonus),
            str(self.service_fee),
            format_float(self.net_profit),
            format_float(self.net_profit_percentage),
            str(self.shipping_fee.customer),
            str(self.shipping_fee.platform),
            str(self.shipping_fee.seller),
            format_float(self.shipping_fee.get_sum()),
            self.province,
            self.district,
            self.parcel_tracking_no
        ]

# SHOPEE_COLUMN_INCOME = {
#     "WEEK": 5,
#     "ORDER_NO": 1,
#     "SHIPPING_FEE_CUSTOMER": 12,
#     "SHIPPING_FEE_PLATFORM": 13,
#     "SHIPPING_FEE_SELLER": 14,
# }
#
# SHOPEE_COLUMN_ORDER = {
#     "PARCEL_TRACKING_NO": 10,
#     "PARENT_SKU": 13,
#     "SKU": 15,
#     "DETAILS": 14,
#     "SALE_QUANTITY": 19,
#     "SALE_PRICE": 20,
#     "PAYMENT_FEE": 32,
#     "SERVICE_FEE": 37,
#     "PROVINCE": 45,
#     "DISTRICT": 46
# }


def read_and_create_shopee_inventory(income_file_path, order_file_path, inventory, configs):
    SHOPEE_COLUMN_INCOME = configs.SHOPEE_COLUMN_INCOME
    SHOPEE_COLUMN_ORDER = configs.SHOPEE_COLUMN_ORDER

    sale_inventory = ShopeeSummary()
    with open(order_file_path, 'r', encoding='utf-8-sig') as order_file, open(income_file_path, 'r', encoding='utf-8-sig') as income_file:
        # Read product data into list
        income_data = list(csv.reader(income_file))
        order_data = list(csv.reader(order_file))

        # Delete header rows
        del income_data[0:6]
        del order_data[0]
        # create a dict with order number as key, items as value
        order_map = dict()
        for order in order_data:
            if order[0] in order_map:
                order_map[order[0]].append(order)
            else:
                order_map[order[0]] = [order]

        # create a dict with unique order_number as key
        income_map = dict()
        for income in income_data:
            income_map[income[1]] = income

        missing_sku = dict()
        for order_no, order_items in order_map.items():
            if order_no in income_map:
                row = income_map[order_no]
                total_price = sum(float(i[SHOPEE_COLUMN_ORDER.get("SALE_PRICE")]) for i in order_items)
                # Loop over item sold in the same order no
                for index, order_item in enumerate(order_items):
                    if len(order_items) > 1:
                        item_no = order_no + "_" + str(index)
                    else:
                        item_no = order_no

                    sale_price = float(order_item[SHOPEE_COLUMN_ORDER.get("SALE_PRICE")])
                    item_ratio = sale_price / total_price

                    # Create sale item
                    item = ShopeeSale()
                    item.week = row[SHOPEE_COLUMN_INCOME.get("WEEK")]
                    item.order_number = order_no
                    item.item_number = item_no
                    if index == 0:
                        item.shipping_fee.customer = float(row[SHOPEE_COLUMN_INCOME.get("SHIPPING_FEE_CUSTOMER")])
                        item.shipping_fee.platform = float(row[SHOPEE_COLUMN_INCOME.get("SHIPPING_FEE_PLATFORM")])
                        item.shipping_fee.seller = float(row[SHOPEE_COLUMN_INCOME.get("SHIPPING_FEE_SELLER")])
                    else:
                        item.shipping_fee.customer = 0
                        item.shipping_fee.platform = 0
                        item.shipping_fee.seller = 0

                    item.parent_sku = order_item[SHOPEE_COLUMN_ORDER.get("PARENT_SKU")]
                    item.sku = order_item[SHOPEE_COLUMN_ORDER.get("SKU")]
                    item.details = order_item[SHOPEE_COLUMN_ORDER.get("DETAILS")]
                    item.quantity = int(order_item[SHOPEE_COLUMN_ORDER.get("SALE_QUANTITY")])

                    item.item_price = sale_price
                    item.payment_fee = float(order_item[SHOPEE_COLUMN_ORDER.get("PAYMENT_FEE")])*item_ratio
                    item.service_fee = float(order_item[SHOPEE_COLUMN_ORDER.get("SERVICE_FEE")])*item_ratio
                    item.province = order_item[SHOPEE_COLUMN_ORDER.get("PROVINCE")].replace('จังหวัด', '')
                    item.district = order_item[SHOPEE_COLUMN_ORDER.get("DISTRICT")].replace('อำเภอ', '').replace('เขต', '')
                    item.parcel_tracking_no = str(order_item[SHOPEE_COLUMN_ORDER.get("PARCEL_TRACKING_NO")])

                    # Match with product inventory by SKU
                    if item.sku in inventory.products:
                        item.product = inventory.products.get(item.sku)
                    else:
                        if item.sku in missing_sku:
                            continue

                        product = Product()
                        product.parent_sku = item.parent_sku
                        product.sku = item.sku
                        product.name = item.details
                        missing_sku[item.sku] = product

                        # Calculate all formulas
                        item.calculate_all_data()

                    # Add to sale inventory then update the amount or fee
                    sale_inventory.sales[item_no] = item

    return (sale_inventory, missing_sku)
