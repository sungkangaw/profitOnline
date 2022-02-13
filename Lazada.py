import csv
from inventory import Product
from sale import Sale
from summary import Summary
from utils import format_float
from config import Config


class LazadaSummary(Summary):
    def get_total_row_for_csv(self):
        self.calculate_all()
        return [
            "",
            "Lazada",
            self.order_quantity,
            self.item_quantity,
            "",
            "",
            "",
            "",
            "",
            format_float(self.total_unit_cost),
            format_float(self.total_unit_cost),
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
            format_float(self.total_shipping_fee_sum)
        ]


class LazadaSale(Sale):
    def __init__(self):
        super().__init__()
        self.quantity = 1

    def get_row_for_csv(self):
        self.calculate_all_data()
        return [
            self.week,
            "Lazada",
            self.order_number,
            self.item_number,
            "",
            self.sku,
            self.product.stock,
            self.details,
            self.quantity,
            str(self.product.unit_cost),
            str(self.product.unit_cost),
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
            format_float(self.shipping_fee.get_sum())
        ]

# Fee name
ITEM_PRICE_CREDIT = "Item Price Credit"
SHIPPING_FEE_CUSTOMER = "Shipping Fee (Paid By Customer)"
SHIPPING_FEE_LAZADA = "Shipping Fee Voucher (by Lazada)"
SHIPPING_FEE_SELLER = "Shipping Fee Paid by Seller"
PAYMENT_FEE = "Payment Fee"
LAZADA_BONUS = "Lazada Bonus"
LAZADA_BONUS_CO_FUND = "Lazada Bonus - LZD co-fund"

# Transaction type
ORDER_SALES = "Orders-Sales"
ORDER_CLAIMS = "Orders-Claims"
ORDER_ITEM_CHARGES = "Orders-Item Charges"
ORDER_LAZADA_FEES = "Orders-Lazada Fees"
ORDER_MARKETING_FEES = "Orders-Marketing Fees"
REFUND_LAZADA = "Refunds-Lazada Fees"
REFUND_CLAIM = "Refunds-Claims"
REFUND_MARKETING_FEES = "Refunds-Marketing Fees"
OTHER_SERVICES = "Other Services-Marketing Fees"
SPONSERED_DISCOVERY = "Sponsored Discovery - Top up"
TRANSACTION_TYPE_FILTER_OUT = [ORDER_CLAIMS, REFUND_CLAIM, REFUND_LAZADA, REFUND_MARKETING_FEES, OTHER_SERVICES, SPONSERED_DISCOVERY]


# LAZADA_COLUMN = {
#     "WEEK": 0,
#     "TRANSACTION_TYPE": 1,
#     "FEE_NAME": 2,
#     "DETAILS": 4,
#     "SKU": 5,
#     "AMOUNT": 7,
#     "ORDER_NO": 13,
#     "ORDER_ITEM_NO": 14,
# }

def update_amount_based_on_fee_type(order_item_no, row, sale_inventory, LAZADA_COLUMN):

    fee_name = row[LAZADA_COLUMN.get("FEE_NAME")]
    transaction_type = row[LAZADA_COLUMN.get("TRANSACTION_TYPE")]
    amount = float(row[LAZADA_COLUMN.get("AMOUNT")])

    #Lazada fees type
    if transaction_type == ORDER_LAZADA_FEES:
        if fee_name == PAYMENT_FEE:
            sale_inventory.sales[order_item_no].payment_fee = amount*(-1.0)
        else:
            sale_inventory.sales[order_item_no].bonus = amount * (-1.0)

    #Marketing fees type
    elif transaction_type == ORDER_MARKETING_FEES:
        sale_inventory.sales[order_item_no].service_fee = amount*(-1.0)

    # Other types
    else:
        if fee_name == ITEM_PRICE_CREDIT:
            sale_inventory.sales[order_item_no].item_price = amount
        elif fee_name == PAYMENT_FEE:
            sale_inventory.sales[order_item_no].payment_fee = amount*(-1.0)
        elif fee_name == SHIPPING_FEE_CUSTOMER:
            sale_inventory.sales[order_item_no].shipping_fee.customer = amount
        elif fee_name == SHIPPING_FEE_SELLER:
            sale_inventory.sales[order_item_no].shipping_fee.seller = amount
        elif fee_name == SHIPPING_FEE_LAZADA:
            sale_inventory.sales[order_item_no].shipping_fee.platform = amount


def read_and_create_lazada_inventory(file_path, inventory, configs):
    LAZADA_COLUMN = configs.LAZADA_COLUMN
    sale_inventory = LazadaSummary()
    with open(file_path, 'r', encoding='utf-8-sig') as in_file:
        # Read product data into list
        data = list(csv.reader(in_file))
        # Delete header row
        del data[0]

        missing_sku = dict()
        for row in data:

            order_item_no = row[LAZADA_COLUMN.get("ORDER_ITEM_NO")]
            if not order_item_no:
                continue

            #Filter out unused transaction type
            if row[LAZADA_COLUMN.get("TRANSACTION_TYPE")] in TRANSACTION_TYPE_FILTER_OUT:
                continue

            if order_item_no in sale_inventory.sales:
                update_amount_based_on_fee_type(order_item_no, row, sale_inventory, LAZADA_COLUMN)
            else:
                # Create product
                item = LazadaSale()
                item.week = row[LAZADA_COLUMN.get("WEEK")]
                item.sku = row[LAZADA_COLUMN.get("SKU")]
                item.details = row[LAZADA_COLUMN.get("DETAILS")]
                item.item_number = order_item_no
                item.order_number = row[LAZADA_COLUMN.get("ORDER_NO")]

                # Match with product inventory by SKU
                if item.sku in inventory.products:
                    item.product = inventory.products.get(item.sku)
                else:
                    #register missing sku
                    if item.sku in missing_sku:
                        continue
                    product = Product()
                    product.parent_sku = ""
                    product.sku = item.sku
                    product.name = item.details
                    missing_sku[item.sku] = product

                #Add to sale inventory then update the amount or fee
                sale_inventory.sales[order_item_no] = item

                update_amount_based_on_fee_type(order_item_no, row, sale_inventory)

    map(lambda x: x.calculate_all_data(), sale_inventory.sales.values())
    return (sale_inventory, missing_sku)
