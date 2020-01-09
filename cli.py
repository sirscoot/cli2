import argparse
import datetime
import sqlite3 as db
import time
import csv

conn = db.connect('transactions-2010.db')
c = conn.cursor()


#filters all transactions based on customer id
def get_transaction_by_customer_id(id):
    c.execute(r"SELECT * FROM transactions WHERE customer_name=(SELECT customer_name FROM customers WHERE customer_id=?)", [id])
    with open('transactions_id.csv', 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(['Transactions by id:'])
        csvWriter.writerows(c.fetchmany(15))

#shows all transactions filtered by customer name
def get_transactions_by_name(name):
    c.execute(r"SELECT * FROM transactions WHERE customer_name=?", [name])
    with open('transactions_name.csv', 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(['Transactions by name:'])
        csvWriter.writerows(c.fetchmany(15))


#shows all transactions filted by date
def get_transaction_by_date(date):
    c.execute(r"SELECT * from transactions WHERE order_date=?", [date])
    with open('transactions_date.csv', 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(['Transactions by date:'])
        csvWriter.writerows(c.fetchmany(15))

        
def main():
    #create the parser argument
    parser = argparse.ArgumentParser(description="Transaction manager")
    group = parser.add_mutually_exclusive_group()


    group.add_argument("-n", "--name", type=str, help="Filters transactions based on date")

    group.add_argument("-i", "--id", type=int, help="Filters transactions based customer id")

    parser.add_argument("-d", "--date", type=str, help="Filters transactions based on order date")


    args = parser.parse_args()



    if args.name:
        print(get_transactions_by_name(args.name))
        print("Data written to file")
    if args.id:
        print(get_transaction_by_customer_id(args.id))
        print("Data written to file")
    if args.date:
        print(get_transaction_by_date(args.date))
        print("Data written to file")

    conn.close()


if __name__ == "__main__":
    main()