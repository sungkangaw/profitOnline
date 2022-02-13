import csv


class Inventory:
    def __init__(self):
        self.products = {}


class Product:
    def __init__(self):
        self.stock = "N/A"
        self.parent_sku = "N/A"
        self.sku = "N/A"
        self.name = "N/A"
        self.color = "N/A"
        self.unit_cost = 0.0

    def get_row_for_csv(self):
        return [
            self.stock,
            self.parent_sku,
            self.sku,
            self.name,
            self.color,
            self.unit_cost
        ]


PRODUCT_INVENTORY_COLUMN = {
    "STOCK": 0,
    "PARENT_SKU": 1,
    "SKU": 2,
    "NAME": 3,
    "COLOR": 4,
    "UNIT_COST": 5
}


def read_and_create_product_inventory(file_path, encoding):
    product_inventory = Inventory()
    with open(file_path, 'r', encoding=encoding) as in_file:

        # Read product data into list
        data = list(csv.reader(in_file))
        len(data[0])
        # Delete header row
        del data[0]
        for row in data:
            # Create product
            product = Product()
            product.stock = row[PRODUCT_INVENTORY_COLUMN.get("STOCK")]
            product.parent_sku = row[PRODUCT_INVENTORY_COLUMN.get("PARENT_SKU")]
            product.sku = row[PRODUCT_INVENTORY_COLUMN.get("SKU")]
            product.name = row[PRODUCT_INVENTORY_COLUMN.get("NAME")]
            product.color = row[PRODUCT_INVENTORY_COLUMN.get("COLOR")]
            try:
                product.unit_cost = float(row[PRODUCT_INVENTORY_COLUMN.get("UNIT_COST")])
            except ValueError:
                pass
            product_inventory.products[product.sku] = product

    return product_inventory

