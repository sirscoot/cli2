import argparse
import datetime
import sqlite3 as db
import time

conn = db.connect('transactions-2010.db')
c = conn.cursor()


#filters all transactions based on customer id
def get_transaction_by_customer_id(id):
    c.execute(r"SELECT * FROM transactions WHERE customer_name=(SELECT customer_name FROM customers WHERE customer_id=?)", [id])
    output = c.fetchmany(15)
    conn.close()
    return output
    

#shows all transactions filtered by customer name
def get_transactions_by_name(name):
    c.execute(r"SELECT * FROM transactions WHERE customer_name=?", [name])
    output = c.fetchmany(15)
    conn.close()
    return output

#shows all transactions filted by date
def get_transaction_by_date(date):
    c.execute(r"SELECT * from transactions WHERE order_date=?", [date])
    output = c.fetchmany(15)
    conn.close()
    return output

def write_to_csv(args):
    c.execute(r"SELECT * from transactions")
    output = c.fetchmany(15)
    conn.close()
    return output

def main():
    #create the parser argument
    parser = argparse.ArgumentParser(description="Transaction manager")
    group = parser.add_mutually_exclusive_group()


    group.add_argument("-n", "--name", type=str, help="Filters transactions based on date")

    group.add_argument("-i", "--id", type=int, help="Filters transactions based customer id")

    parser.add_argument("-d", "--date", type=str, help="Filters transactions based on order date")

    parser.add_argument("-w", "--write", action="store_true", help="Write data to csv file")

    args = parser.parse_args()



    if args.name:
        print(get_transactions_by_name(args.name))
    if args.id:
        print(get_transaction_by_customer_id(args.id))
    if args.date:
        print(get_transaction_by_date(args.date))
    if args.write:
        f = open("transactions.csv", "a")
        f.write(str(write_to_csv(args)))
        print("Data saved")



if __name__ == "__main__":
    main()