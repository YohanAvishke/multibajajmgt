import csv
import json
import requests
import logging
import pandas

# -*- File Paths -*-
INVOICE_PATH = "../data/inventory/invoices.json"
ADJUSTMENT_PATH = "../data/inventory/adjustments/adjustment-21:05:12-new.csv"
INVENTORY_PATH = "../data/inventory/stock.inventory.line.csv"

# -*- Request URLs -*-
URL = "https://erp.dpg.lk/Help/GetHelp"
URL_PRODUCTS = "https://erp.dpg.lk/PADEALER/PADLRGOODRECEIVENOTE/Inquire"

# -*- Request Headers -*-
HEADERS = {
    "authority": "erp.dpg.lk",
    "sec-ch-ua": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "accept": "*/*",
    "x-requested-with": "XMLHttpRequest",
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.72 Mobile Safari/537.36",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://erp.dpg.lk",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://erp.dpg.lk/Application/Home/PADEALER",
    "accept-language": "en-US,en;q=0.9",
    "cookie": ".AspNetCore.Session=CfDJ8GocJQ9OP09IpVQeLLXSxcYZs8%2F1D5Z9oidQOvcjvwxY2ui1WavPUypGOO1acPJWb0ZIKTitoBIF"
              "m2JpZcSt9jqeBTiOe6ERQDecoNhv7Y54t1vJb8caJ5yrVr68k5V4JHpOtGF61SQRcUZ2sHMNjhPMVDpNGfPZV5IOM%2BHns9oP"
}

# -*- Main function -*-
if __name__ == "__main__":
    logging_format = "%(asctime)s: %(levelname)s - %(message)s"
    logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%H:%M:%S")


# -*- Functions -*-
def get_grn_for_invoice():
    # -*- coding: utf-8 -*-
    """ Before
    Add the Invoice numbers to ['Invoice']['Numbers']['Invoice']

    ``` After
    Call get_products_from_invoices()
    """
    with open(INVOICE_PATH, "r") as invoice_file:
        invoice_reader = json.load(invoice_file)
    invoice = invoice_reader["Invoice"]

    for number in invoice["Numbers"]:
        invoice_number = number["Invoice"]

        payload = "strInstance=DLR&strPremises=KGL&strAppID=00011&strFORMID=00605&strFIELD_NAME=%2CSTR_DEALER_CODE" \
                  "%2CSTR_GRN_NO%2CSTR_ORDER_NO%2CSTR_INVOICE_NO%2CINT_TOTAL_GRN_VALUE&strHIDEN_FIELD_INDEX=%2C0&" \
                  "strDISPLAY_NAME=%2CSTR_DEALER_CODE%2CGRN+No%2COrder+No%2CInvoice+No%2CTotal+GRN+Value&" \
                  f"strSearch={invoice_number}&strSEARCH_TEXT=&strSEARCH_FIELD_NAME=STR_GRN_NO&" \
                  "strColName=STR_INVOICE_NO&strLIMIT=50&strARCHIVE=TRUE&strORDERBY=STR_GRN_NO&" \
                  "strOTHER_WHERE_CONDITION=%5B%5B%22STR_DEALER_CODE+%22%2C%22%3D%22%2C%22'AC2011063676'%22%5D%5D&" \
                  "strAPI_URL=api%2FModules%2FPadealer%2FPadlrgoodreceivenote%2FList&strTITEL=&strAll_DATA=true&" \
                  "strSchema="
        response = requests.request("POST", URL, headers=HEADERS, data=payload)

        if response:
            invoice_details = json.loads(response.text)

            if invoice_details == "NO DATA FOUND":
                logging.info(f"Invoice Number: {invoice_number} is Invalid !!!")
            elif len(invoice_details) > 1:
                logging.info(f"Invoice Number: {invoice_number} is too Vague !!!")
            else:
                number["GRN"] = invoice_details[0]["GRN No"]
        else:
            logging.error(f'An error has occurred !!! \nStatus: {response.status_code} \nFor reason: {response.reason}')

    with open(INVOICE_PATH, "w") as invoice_file:
        json.dump(invoice_reader, invoice_file)

    logging.info("Invoice data scrapping done.")


def get_products_from_invoices():
    # -*- coding: utf-8 -*-
    """ Before
    get_grn_for_invoice() should be called before

    ''' After Call
    Part Numbers are located at ['Invoice']['Products']
    """
    with open(INVOICE_PATH, "r") as invoice_file:
        invoice_reader = json.load(invoice_file)
    invoice = invoice_reader["Invoice"]
    invoice["Products"] = []

    for number in invoice["Numbers"]:
        invoice_number = number["Invoice"]
        grn_number = number["GRN"] if "GRN" in number else None

        payload_mid = f"&strInvoiceNo={invoice_number}&strPADealerCode=AC2011063676&STR_FORM_ID=00605"
        payload = f"strMode=GRN&strGRNno={grn_number + payload_mid}&STR_FUNCTION_ID=IQ" \
            if grn_number else f"strMode=INVOICE{payload_mid}&STR_FUNCTION_ID=CR"
        payload = f"{payload}&STR_PREMIS=KGL&STR_INSTANT=DLR&STR_APP_ID=00011"

        response = requests.request("POST", URL_PRODUCTS, headers=HEADERS, data=payload)

        if response:
            product_details = json.loads(response.text)["DATA"]

            if product_details == "NO DATA FOUND":
                logging.warning(f"Invoice Number: {number} is Invalid !!!")
            else:
                product_details = product_details["dsGRNDetails"]["Table"] if "GRN" in number \
                    else product_details["dtGRNDetails"]

                for product_detail in product_details:
                    invoice["Products"].append(product_detail)
        else:
            logging.error(f'An error has occurred !!! \nStatus: {response.status_code} \nFor reason: {response.reason}')

    with open(INVOICE_PATH, "w") as invoice_file:
        json.dump(invoice_reader, invoice_file)

    logging.info("Product data scrapping done.")


def json_to_csv():
    # -*- coding: utf-8 -*-
    """ Before
    get_products_from_invoices() should be called before

    ''' After Call
    Part Numbers with the quantities will be in the `ADJUSTMENT_PATH`
    """
    with open(INVOICE_PATH, "r") as invoice_file:
        invoice_reader = json.load(invoice_file)
    products = invoice_reader["Invoice"]["Products"]

    with open(ADJUSTMENT_PATH, "w") as adj_csv_file:
        field_names = ("Product/Internal Reference", "Counted Quantity")
        adj_writer = csv.DictWriter(adj_csv_file, fieldnames=field_names, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
        adj_writer.writeheader()

        for product in products:
            product_number = product["STR_PART_NO"] if "STR_PART_NO" in product else product["STR_PART_CODE"]
            product_count = product["INT_QUANTITY"] if "INT_QUANTITY" in product else product["INT_QUATITY"]

            adj_writer.writerow({"Product/Internal Reference": product_number,
                                 "Counted Quantity": float(product_count)})

    merge_duplicates()
    logging.info("Product data modeling done.")


def merge_duplicates():
    df = pandas.read_csv(ADJUSTMENT_PATH, header=0)
    df["Counted Quantity"] = df.groupby(["Product/Internal Reference"])["Counted Quantity"].transform('sum')
    df.drop_duplicates(subset=["Product/Internal Reference"], inplace=True, keep="last")
    df.to_csv(ADJUSTMENT_PATH, index=False)


def inventory_adjustment():
    # -*- coding: utf-8 -*-
    """ Before
    json_to_csv() should be called before to get the adjustment file

    After Call
    Final file to upload will be available at `ADJUSTMENT_PATH`
    """
    products = []

    with open(INVENTORY_PATH, "r") as inventory_file, open(ADJUSTMENT_PATH, "r") as adjustment_file:
        inventory_reader = list(csv.DictReader(inventory_file))
        adjustment_reader = list(csv.DictReader(adjustment_file))

    for adjustment_product in adjustment_reader:
        exists = False
        adjustment_number = adjustment_product["Product/Internal Reference"]
        adjustment_quantity = float(adjustment_product["Counted Quantity"])

        for inventory_product in inventory_reader:
            inventory_number = inventory_product["Product/Internal Reference"]
            inventory_quantity = float(inventory_product["Counted Quantity"])

            if adjustment_number == inventory_number:
                exists = True
                inventory_product["Counted Quantity"] = inventory_quantity + adjustment_quantity
                products.append(inventory_product)
                break

        if not exists:
            logging.warning(f"Product Number: {adjustment_number} is Invalid !!!")

    with open(ADJUSTMENT_PATH, mode='w') as adjustment_file:
        field_names = ("ID", "Product/ID", "Product/Internal Reference", "Counted Quantity")
        adjustment_writer = csv.DictWriter(adjustment_file, fieldnames=field_names, delimiter=',', quotechar='"',
                                           quoting=csv.QUOTE_MINIMAL)
        adjustment_writer.writeheader()

        for product in products:
            adjustment_writer.writerow(product)

    logging.info("Inventory Adjustment done.")


# -*- Function Calls -*-
# get_grn_for_invoice()
# get_products_from_invoices()
json_to_csv()
# merge_duplicates()
# inventory_adjustment()
