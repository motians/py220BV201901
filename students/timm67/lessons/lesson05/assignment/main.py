from loguru import logger
from sys import stdout

from mongoengine import connect

from ingest_csv import ingest_customer_csv
from ingest_csv import ingest_product_csv
from ingest_csv import ingest_rental_csv

from database import show_available_products

CUST_CSV_FILENAME = 'customers.csv'
PROD_CSV_FILENAME = 'products.csv'
RNTL_CSV_FILENAME = 'rentals.csv'
#CSV_PATH_DBG = './lessons/lesson05/assignment/'
CSV_PATH_DBG = ''

def main():
    """
    Ensure you application will create an empty database if one doesn’t exist
    when the app is first run. Call it customers.db
    """

    # Standalone function to initialize logging
    logger.add(stdout, level='WARNING')
    logger.add("logfile_{time}.txt", level='INFO')
    logger.enable(__name__)

    " connect to the mongo db using mongoengine "
    connect('mongoengine_test', host='localhost', port=27017)

    ingest_customer_csv(CSV_PATH_DBG + CUST_CSV_FILENAME)
    ingest_product_csv(CSV_PATH_DBG + PROD_CSV_FILENAME)
    ingest_rental_csv(CSV_PATH_DBG + RNTL_CSV_FILENAME)

    db_dict = show_available_products()

    print(db_dict)

if  __name__ == '__main__':
    main()
