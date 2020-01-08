import argparse
import datetime
import sqlite3 as db
import time

conn = db.connect('transactions-2010.db')
c = conn.cursor()


#filters all transactions based on customer id
def get_transaction_by_customer_id(args):
    c.execute(r"SELECT * FROM transactions WHERE customer_name=(SELECT customer_name FROM customers WHERE customer_id=4)")
    return c.fetchmany(5)
    conn.close()

#shows all transactions filtered by customer name
def get_transactions_by_name(args):
    c.execute(r"SELECT * FROM transactions WHERE customer_name='aviato'")
    return c.fetchmany(5)
    conn.close()

#shows all transactions filted by date
def get_transaction_by_date(args):
    c.execute(r"SELECT * from transactions WHERE order_date='2010-12-30'")
    return c.fetchmany(5)
    conn.close()

def main():
    #create the parser argument
    parser = argparse.ArgumentParser(description="Transaction manager")

    parser.add_argument("-n", "--name", type=str, default=None, metavar=("name"), help="Filters transactions based on date")

    parser.add_argument("-i", "--id", type=str, default=None, help="Filters transactions based customer id")

    parser.add_argument("-d", "--date", type=str, default=None, help="Filters transactions based on order date")

    args = parser.parse_args()



    if args.name != None:
        print(get_transactions_by_name(args))
    elif args.id != None:
        print(get_transaction_by_customer_id(args))
    elif args.date != None:
        print(get_transaction_by_date(args))



if __name__ == "__main__":
    main()