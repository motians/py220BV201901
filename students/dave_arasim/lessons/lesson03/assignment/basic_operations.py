'''
Create customers database 'customers.db'.
Add/search/update/delete/list data in customers.db.
'''

from customers_model import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_database(*args):
    ''' Create customers database 'customers.db' '''
    logger.info('Build class Customers from the model in the database\n')

    database.create_tables([Customers])
    database.close()


def add_customer(*args):
    ''' Add customer to customers database '''
    logger.info(f'Adding customer to database: {args[0]}')

    try:
        if args[1] != '':
            customer = (args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7])
    except Exception as e:
        customer = args[0]

    logger.info(f'customer: {customer}')

    CUSTOMER_ID = 0
    NAME = 1
    LASTNAME = 2
    HOME_ADDR = 3
    PHONE_NUMBER = 4
    EMAIL = 5
    STATUS = 6
    CRED_LIMIT = 7
    
    # status will be stored as boolean value
    if (customer[STATUS] != True) and (customer[STATUS] != False):
        if customer[STATUS].lower() == 'active':
            customer_status = True
        else:
            customer_status = False
    else:
        customer_status = customer[STATUS]

    try:
        with database.transaction():
            new_cust = Customers.create(
                customer_id=customer[CUSTOMER_ID],
                name=customer[NAME],
                lastname=customer[LASTNAME],
                home_addr=customer[HOME_ADDR],
                phone_number=customer[PHONE_NUMBER],
                email=customer[EMAIL],
                status=customer_status,
                cred_limit=customer[CRED_LIMIT])
            new_cust.save()

            logger.info('Database add successful\n')
    except Exception as e:
        logger.info(f'Error 1 creating Customer ID: {customer[CUSTOMER_ID]}')
        logger.info('It must already be in the database?\n')

    database.close()


def search_customer(*args):
    ''' Search for customer in customers database '''
    logger.info(f'Searching for customer in database: {args[0]}')

    cust_id = args[0]
    
    try:
        search_cust = Customers.get(Customers.customer_id == cust_id)
        return_cust = {
            'name': search_cust.name,
            'lastname': search_cust.lastname,
            'email': search_cust.email,
            'phone_number': search_cust.phone_number}
    except Exception:
        return_cust = {}
#        raise ValueError('NoCustomer')  DKA enable for pytest testing
        logger.info(f'NoCustomer: Error 2 searching Customer ID: {cust_id}')
        logger.info('It must not be in the database?\n')

    logger.info('Here is the customer found:')
    logger.info(f'{return_cust}\n')

    database.close()

    return return_cust


def delete_customer(*args):
    ''' Delete customer from customers database '''
    logger.info(f'Deleting customer from database: {args[0]}')

    cust_id = args[0]
    delete_success = False

    try:
        cust_to_delete = Customers.get(Customers.customer_id == cust_id)
        cust_to_delete.delete_instance()

        logger.info('Database delete successful\n')
        delete_success = True
    except Exception:
 #       raise ValueError('NoCustomer')  DKA enable for pytest testing
        logger.info(f'NoCustomer: Error 3 deleting Customer ID: {cust_id}')
        logger.info('It must not be in the database?\n')

    database.close()

    return delete_success


def update_customer_credit(*args):
    ''' Update customer record in customers database '''
    logger.info(f'Search and update customers record: {args[0]}')

    cust_id = args[0]
    update_type = args[1]

    try:
        search_cust = Customers.get(Customers.customer_id == cust_id)

        if update_type == 'status':
            search_cust.status = args[2]
        elif update_type == 'cred_limit':
            search_cust.cred_limit = args[2]
        else:
            search_cust.cred_limit = args[1]

        search_cust.save()

        logger.info('Record update successful\n')
    except Exception:
#        raise ValueError('NoCustomer')  DKA enable for pytest testing
        logger.info(f'NoCustomer: Error 4 searching Customer ID: {cust_id}')
        logger.info('It must not be in the database?\n')

    database.close()


def list_active_customers(*args):
    ''' Count active customers in customers database '''
    logger.info('Counting active customers in the database')

    count_cust = 0

    try:
        for customer in Customers:
            if customer.status:
                count_cust += 1
    except Exception as e:
        count_cust = 0
        logger.info(f'No active customers found\n')

    logger.info(f'Here is the count of active customers: {count_cust}\n')

    database.close()

    return count_cust


def show_customers(*args):
    ''' Show all customers in the customers database '''
    logger.info('Read and print all customers records:')

    for customer in Customers:
        logger.info(f'ID:{customer.customer_id}, FN:{customer.name}, ' +\
                    f'LN:{customer.lastname}, AD:{customer.home_addr}, ' +\
                    f'PH:{customer.phone_number}, EM:{customer.email}, ' +\
                    f'ST:{customer.status}, CR:{customer.cred_limit}')

    print()
