import os
import logging

from dotenv import find_dotenv, load_dotenv
from enums import EnvVariable

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATA_DIR = f"{ROOT_DIR}/data"

LOG_LEVEL = logging.DEBUG

log = logging.getLogger(__name__)


def configure_env():
    """
    Configure environment variables
    """
    load_dotenv(find_dotenv(f"{ROOT_DIR}/.env"))


ODOO_SERVER_URL = os.getenv(EnvVariable.odoo_server_url)
ODOO_SERVER_USERNAME = os.getenv(EnvVariable.odoo_server_username)
ODOO_SERVER_API_KEY = os.getenv(EnvVariable.odoo_server_api_key)
ODOO_DATABASE_NAME = os.getenv(EnvVariable.odoo_database_name)

DPMC_ERP_URL = os.getenv(EnvVariable.dpmc_server_url)
# DPMC_ERP_PRODUCT_INQUIRE_URL = f"{DPMC_ERP_URL}/PADEALER/PADLRItemInquiry/Inquire"