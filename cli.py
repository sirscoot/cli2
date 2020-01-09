import argparse
import datetime
import sqlite3 as db
import time
import csv




#filters all transactions based on customer id
def get_transaction_by_customer_id(c, id):
    c.execute(r"SELECT * FROM transactions WHERE customer_name=(SELECT customer_name FROM customers WHERE customer_id=?)", [id])
    write_to_csv(c)

#shows all transactions filtered by customer name
def get_transactions_by_name(c, name):
    c.execute(r"SELECT * FROM transactions WHERE customer_name=?", [name])
    write_to_csv(c)


#shows all transactions filted by date
def get_transaction_by_date(c, date):
    c.execute(r"SELECT * from transactions WHERE order_date=?", [date])
    write_to_csv(c)

def write_to_csv(c):
    with open('results.csv', 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(['Transactions:'])
        csvWriter.writerows(c.fetchmany(15))

      
def main():
    conn = db.connect('transactions-2010.db')
    c = conn.cursor()

    #create the parser argument
    parser = argparse.ArgumentParser(description="Transaction manager")
    group = parser.add_mutually_exclusive_group()


    group.add_argument("-n", "--name", type=str, help="Filters transactions based on date")

    group.add_argument("-i", "--id", type=int, help="Filters transactions based customer id")

    parser.add_argument("-d", "--date", type=str, help="Filters transactions based on order date")


    args = parser.parse_args()



    if args.name:
        print(get_transactions_by_name(c, args.name))
        print("Data written to file")
    if args.id:
        print(get_transaction_by_customer_id(c, args.id))
        print("Data written to file")
    if args.date:
        print(get_transaction_by_date(c, args.date))
        print("Data written to file")

    conn.close()


if __name__ == "__main__":
    main()