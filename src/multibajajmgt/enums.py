from enum import Enum


class MultiBajajMgtEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


class EnvVariable(MultiBajajMgtEnum):
    odoo_server_url = "ODOO_SERVER_URL"
    odoo_server_api_key = "ODOO_SERVER_API_KEY"
    odoo_database_name = "ODOO_DATABASE_NAME"
    odoo_server_username = "ODOO_SERVER_USERNAME"
    dpmc_server_url = "DPMC_SERVER_URL"
    dpmc_server_username = "DPMC_SERVER_SERVER_USERNAME"
    dpmc_server_password = "DPMC_SERVER_PASSWORD"


class DocumentResourceExtension(MultiBajajMgtEnum):
    json = "json"
    csv = "csv"


class DocumentResourceType(MultiBajajMgtEnum):
    price_dpmc_all = "price-dpmc-all"
    invoice_dpmc = "invoice_dpmc"


class OdooCSVFieldName(MultiBajajMgtEnum):
    external_id = "External ID"
    internal_id = "Internal Reference"
    sales_price = "Sales Price"
    cost = "Cost"
    qty_available = "Quantity On Hand"


class OdooDBFieldName(MultiBajajMgtEnum):
    external_id = "external_id"
    internal_id = "default_code"
    sales_price = "list_price"
    cost = "standard_price"
    qty_available = "qty_available"


class ProductPriceStatus(MultiBajajMgtEnum):
    none = "none"
    up = "up"
    down = "down"
    equal = "equal"


class DPMCFieldName(MultiBajajMgtEnum):
    # Invoice
    invoice_no = "STR_INVOICE_NO"
    order_no = "STR_ORDER_NO"
    dlr_order_no = "STR_DLR_ORD_NO"
    mobile_no = "STR_MOBILE_INVOICE_NO"
    # Product
    part_code = "STR_PART_CODE"
    part_desc = "STR_DESC"
    part_qty = "INT_QUANTITY"
    unit_cost = "INT_UNIT_COST"
    total = "INT_TOTAL_PART_COST"
    ware_code = "WAREHOUSE_CODE"
    loc_code = "LOCATION_CODE"
    rack_code = "RACK_CODE"
    bin_code = "BIN_CODE"
    sbin_code = "SUBBIN_CODE"
    serial_base = "STR_SERIAL_BASE"


class InvoiceStatus(MultiBajajMgtEnum):
    failed = "Failed"
    success = "Success"
    multiple = "Multiple"


class InvoiceType(MultiBajajMgtEnum):
    invoice = "Invoice"
    order = "Order"
    mobile = "Mobile"


class InvoiceJSONFieldName(MultiBajajMgtEnum):
    # Invoice
    date = "Date"
    default_id = "Default ID"
    status = "Status"
    type = "Type"
    grn_id = "GRN ID"
    invoice_id = "Invoice ID"
    order_id = "Order ID"
    # Product
    products = "Products"
    part_code = "ID"
    part_desc = "Name"
    part_qty = "Quantity"
    unit_cost = "Unit Cost"
    total = "Total"