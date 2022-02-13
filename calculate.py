import sys
from inventory import read_and_create_product_inventory
from Lazada import read_and_create_lazada_inventory
from shopee import read_and_create_shopee_inventory
from writer import write_output, write_missing_inventory
import ntpath
from config import Config

LAZADA = "lazada"
SHOPEE = "shopee"

from chardet.universaldetector import UniversalDetector

def test_encoding(file_name):
    detector = UniversalDetector()
    with open(file_name, 'rb') as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                 break
        detector.close()
    return detector.result['encoding']

#
# import tkinter as tk
# from tkinter import ttk
# from tkinter import filedialog
#
# def getFile():
#     global df
#
#     import_file_path = filedialog.askopenfilename()
#     print(import_file_path)
#
# window = tk.Tk()
#
# window.title("Profit calculation app")
# window.geometry('350x200')
#
# tab_control = ttk.Notebook(window)
#
# tab1 = ttk.Frame(tab_control)
# tab2 = ttk.Frame(tab_control)
#
# tab_control.add(tab1, text='Lazada')
# tab_control.add(tab2, text='Shopee')
#
# btn = tk.Button(tab1, text="File", command=getFile)
# btn.grid(column=1, row=1)
#
# lbl1 = tk.Label(tab1, text= 'Product cost: ')
# lbl1.grid(column=0, row=0)
#
# lbl12 = tk.Label(tab1, text= 'Lazada file: ')
# lbl12.grid(column=0, row=2)
#
# lbl2 = tk.Label(tab2, text= 'Product cost: ')
# lbl2.grid(column=0, row=0)
#
# lbl21 = tk.Label(tab2, text= 'Sale file: ')
# lbl21.grid(column=0, row=2)
#
# lbl22 = tk.Label(tab2, text= 'Order all file: ')
# lbl22.grid(column=0, row=4)
#
# tab_control.pack(expand=1, fill='both')
#
# window.mainloop()

if __name__ == '__main__':
    product_inventory_file = 'db/product_cost.csv'

    product_inventory_encoding = 'utf-8-sig'
    encoding = test_encoding(product_inventory_file)
    # print(encoding)
    if encoding == 'Windows-1252':
        product_inventory_encoding = 'cp1252'
        print("Product cost file encoding is incorrect.")
        sys.exit()

    print("Reading product file db/product_cost.csv")
    product_inventory = read_and_create_product_inventory(product_inventory_file, product_inventory_encoding)

    print("Reading config.txt")
    configs = Config()

    sale_file = sys.argv[1] if len(sys.argv) >1 and sys.argv[1] else 'shopee\Shopee_Income.โอนเงินสำเร็จ.20201214_20201220.csv' #sys.argv[0]
    base_file = ntpath.basename(sale_file)

    if base_file.lower().startswith(LAZADA) and base_file.lower().endswith(".csv"):
        print("Processing for Lazada")
        out_file = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else 'lazada_output.csv'  # sys.argv[1]
        print("Reading Lazada file " + sale_file)
        result = read_and_create_lazada_inventory(sale_file, product_inventory, configs)

        print("Writing output to " + out_file)
        sale_inventory = result[0]
        write_output(out_file, sale_inventory, configs)

        missing_sku = result[1]
        if len(missing_sku) > 0:
            print("***** " +str(len(missing_sku)) + " SKUs missing. Writing missing skus to db/product_cost.csv")
            write_missing_inventory(product_inventory_file, missing_sku, product_inventory_encoding)
    elif base_file.lower().startswith(SHOPEE) and base_file.lower().endswith(".csv"):
        try:
            print("Processing for Shopee")
            sale_order = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else 'shopee\Shopee_Order.all.20201201_20201231.csv'
            sale_order_base_file = ntpath.basename(sale_order)
            if sale_order_base_file.lower().startswith(SHOPEE) and sale_order_base_file.lower().endswith(".csv"):
                out_file = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else 'shopee_output.csv'

                print("Reading shopee file " + sale_file + " and " + sale_order)
                result = read_and_create_shopee_inventory(sale_file, sale_order, product_inventory, configs)

                print("Writing output to " + out_file)
                sale_inventory = result[0]
                write_output(out_file, sale_inventory, configs)

                missing_sku = result[1]
                if len(missing_sku) > 0:
                    print("***** " + str(len(missing_sku)) + " SKUs missing. Writing missing skus to db/product_cost.csv")
                    write_missing_inventory(product_inventory_file, missing_sku, product_inventory_encoding)
            else:
                print("Shopee files missing. Please check.")
        except IndexError:
            print("Shopee order file missing!")
    else:
        print("Please check input file name. File name must start with Shopee or Lazada and has .csv extension")
        sys.exit()