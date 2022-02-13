import csv
from config import Config

# OUT_COLUMNS = [
#     "Week",
#     "Platform",
#     "Order Number",
#     "Item Number",
#     "Parent SKU",
#     "Product SKU",
#     "Stock Place",
#     "Detail",
#     "Sale Quantity",
#     "Unit Cost",
#     "Total Cost",
#     "Sale Price",
#     "Profit",
#     "Profit %",
#     "Payment Fee",
#     "Bonus",
#     "Service Fee",
#     "Net Profit",
#     "Net Profit %",
#     "Shipping Fee Customer",
#     "Shipping Fee Platform",
#     "Shipping Fee Seller",
#     "Shipping Fee Sum",
#     "Province",
#     "District",
#     "Parcel Tracking No."
# ]


def write_output(out_path, sale_inventory, configs):
    with open(out_path, 'w', encoding='utf-8-sig') as out_file:

        #Prevent excel encoding issue
        #out_file.write(u'\uFEFF')

        csv_writer = csv.writer(out_file, delimiter=',', lineterminator='\n')

        OUT_COLUMNS = configs.OUT_COLUMNS
        csv_writer.writerow(OUT_COLUMNS)

        for sale in sale_inventory.sales.values():
            #Order of list must be the same as OUT_COLUMNS
            csv_writer.writerow(sale.get_row_for_csv())
        csv_writer.writerow(sale_inventory.get_total_row_for_csv())


def write_missing_inventory(out_path, missing_sku, encoding):
    with open(out_path, 'a', encoding=encoding) as out_file:

        #Prevent excel encoding issue
        out_file.write(u'\n')

        csv_writer = csv.writer(out_file, delimiter=',', lineterminator='\n')
        for sku, product in missing_sku.items():
            csv_writer.writerow(product.get_row_for_csv())
