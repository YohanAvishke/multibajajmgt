import logging
import requests
import pandas
import json

# -*- File Paths -*-
PRODUCT_PRICE_PATH = "../data/product/product.price.csv"
PRODUCT_EMPTY_STOCK_PRICE_PATH = "../data/product/product.price-empty-stock.csv"

# -*- Request URLs -*-
URL = "https://erp.dpg.lk/PADEALER/PADLRItemInquiry/Inquire"

# -*- Constants -*-
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
    'cookie': '.AspNetCore.Session=CfDJ8IZaSW4NiQFBjcUYf7vHo%2BVVeITVjRla%2B%2BLVCQfe34qcYXRgv9P7FSF3KtYfOEZHdkg'
              '%2BDysp8sfG4b9TjCP%2BFMYElu2ObPZJReZkX15DScoiAbHrZuL'
              '%2BIfCL4mj0hUYtiAVvSBYdDdnwLHZpzScsf8GBGgp35uQlWihAA93U4bKN; '
              '.AspNetCore.Antiforgery.mEZFPqlrlZ8=CfDJ8IZaSW4NiQFBjcUYf7vHo'
              '-WzO2BBbxDCjjuqPwcsYbKNWdMtLQC5RdyantvE4ZVTXQAuqKrZHo0ySvD5W5iYO9nPhiMDxeHNnA7LtsrhKBmULRgn3N3LnRWsDgfGmtYBzt30cLBj6BrvL5ZNF5viXV8',
    }

# -*- Main function -*-
if __name__ == "__main__":
    logging_format = "%(asctime)s: %(levelname)s - %(message)s"
    logging.basicConfig(format = logging_format, level = logging.INFO, datefmt = "%H:%M:%S")


# -*- Function -*-
def scrap_prices():
    product_reader = pandas.read_csv(PRODUCT_PRICE_PATH)

    for idx, product in product_reader.iterrows():
        if "Bajaj" in product["Point of Sale Category"] and pandas.isnull(product["Updated Cost"]):
            product_number = product['Internal Reference']

            payload = f"strPartNo_PAItemInq={product_number}&strFuncType=INVENTORYDATA&" \
                      "strPADealerCode_PAItemInq=AC2011063676&STR_FORM_ID=00602&STR_FUNCTION_ID=IQ&STR_PREMIS=KGL&" \
                      "STR_INSTANT=DLR&STR_APP_ID=00011"

            try:
                response = requests.request("POST", URL, headers = HEADERS, data = payload)
            except requests.exceptions.ConnectionError as e:
                logging.error(e)
                break

            if response:
                product_data = json.loads(response.text)["DATA"]

                if 'dblSellingPrice' in product_data and product_data["dblSellingPrice"]:
                    price = float(product_data["dblSellingPrice"])

                    product_reader.loc[idx, "Updated Sales Price"] = product_reader.loc[idx, "Updated Cost"] = price
                    logging.info(f"{idx + 1} - Product Number: {product_number}, Price: {price}")
                else:
                    product_reader.loc[idx, "Updated Sales Price"] = product_reader.loc[idx, "Sales Price"]
                    product_reader.loc[idx, "Updated Cost"] = product_reader.loc[idx, "Cost"]
                    logging.warning(f"Product Number: {product_number} is Invalid !!!")

                product_reader.to_csv(PRODUCT_PRICE_PATH, index = False)

            else:
                logging.error(f'An error has occurred !!! \nStatus: {response.status_code} \n'
                              f'For reason: {response.reason}')
                break
            # time.sleep(2)


def sort_products_by_price():
    df = pandas.read_csv(PRODUCT_EMPTY_STOCK_PRICE_PATH, header = 0)
    sorted_df = df.sort_values(by = "Sales Price", ascending = False)

    sorted_df.to_csv(PRODUCT_EMPTY_STOCK_PRICE_PATH, index = False)


def get_price_fluctuations():
    price_reader = pandas.read_csv(PRODUCT_PRICE_PATH, header = 0)
    a = price_reader[["Sales Price"]].eq(price_reader["Updated Sales Price"], axis = 0).assign(no = True)


# -*- Function Calls -*-
scrap_prices()
# sort_products_by_price()
