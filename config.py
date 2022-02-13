import configparser

class Config:
    def __init__(self):
        parser = configparser.ConfigParser()
        parser.read("config.txt")
        self.SHOPEE_COLUMN_INCOME = {
            "WEEK": int(parser.get("SHOPEE_COLUMN_INCOME", "WEEK")),
            "ORDER_NO": int(parser.get("SHOPEE_COLUMN_INCOME", "ORDER_NO")),
            "SHIPPING_FEE_CUSTOMER": int(parser.get("SHOPEE_COLUMN_INCOME", "SHIPPING_FEE_CUSTOMER")),
            "SHIPPING_FEE_PLATFORM": int(parser.get("SHOPEE_COLUMN_INCOME", "SHIPPING_FEE_PLATFORM")),
            "SHIPPING_FEE_SELLER": int(parser.get("SHOPEE_COLUMN_INCOME", "SHIPPING_FEE_SELLER")),
        }

        self.SHOPEE_COLUMN_ORDER = {
            "PARCEL_TRACKING_NO": int(parser.get("SHOPEE_COLUMN_ORDER", "PARCEL_TRACKING_NO")),
            "PARENT_SKU": int(parser.get("SHOPEE_COLUMN_ORDER", "PARENT_SKU")),
            "SKU": int(parser.get("SHOPEE_COLUMN_ORDER", "SKU")),
            "DETAILS": int(parser.get("SHOPEE_COLUMN_ORDER", "DETAILS")),
            "SALE_QUANTITY": int(parser.get("SHOPEE_COLUMN_ORDER", "SALE_QUANTITY")),
            "SALE_PRICE": int(parser.get("SHOPEE_COLUMN_ORDER", "SALE_PRICE")),
            "PAYMENT_FEE": int(parser.get("SHOPEE_COLUMN_ORDER", "PAYMENT_FEE")),
            "SERVICE_FEE": int(parser.get("SHOPEE_COLUMN_ORDER", "SERVICE_FEE")),
            "PROVINCE": int(parser.get("SHOPEE_COLUMN_ORDER", "PROVINCE")),
            "DISTRICT": int(parser.get("SHOPEE_COLUMN_ORDER", "DISTRICT")),
        }

        self.LAZADA_COLUMN = {
            "WEEK": int(parser.get("LAZADA_COLUMN", "WEEK")),
            "TRANSACTION_TYPE": int(parser.get("LAZADA_COLUMN", "TRANSACTION_TYPE")),
            "FEE_NAME": int(parser.get("LAZADA_COLUMN", "FEE_NAME")),
            "DETAILS": int(parser.get("LAZADA_COLUMN", "DETAILS")),
            "SKU": int(parser.get("LAZADA_COLUMN", "SKU")),
            "AMOUNT": int(parser.get("LAZADA_COLUMN", "AMOUNT")),
            "ORDER_NO": int(parser.get("LAZADA_COLUMN", "ORDER_NO")),
            "ORDER_ITEM_NO": int(parser.get("LAZADA_COLUMN", "ORDER_ITEM_NO")),
        }

        self.OUT_COLUMNS = parser.get("OUTPUT_COLUMN", "OUT_COLUMNS")
