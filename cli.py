import argparse
import datetime
import sqlite3 as db
import time
import csv


#filters all transactions based on customer id
def get_transaction_by_customer_id(c, id):
    c.execute(r"SELECT * FROM transactions WHERE customer_name=(SELECT customer_name FROM customers WHERE customer_id=?)", [id])
    return c.fetchall()
    


#shows all transactions filtered by customer name
def get_transactions_by_name(c, name):
    c.execute(r"SELECT * FROM transactions WHERE customer_name=?", [name])
    return c.fetchall()
    


#shows all transactions filted by date
def get_transaction_by_date(c, date):
    c.execute(r"SELECT * FROM transactions WHERE order_date=?", [date])
    return c.fetchall()
    

#writes data to csv file
def write_to_csv(rows, output):
    with open(output, 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(['Transaction Id', 'Transaction Date', 'Transaction Price', 'Customer Name'])
        for row in rows:
            csvWriter.writerow(list(row))




def main():

    #create the parser argument
    parser = argparse.ArgumentParser(description="Transaction manager")
    group = parser.add_mutually_exclusive_group(required=True)


    group.add_argument("-n", "--name", type=str, help="Filters transactions based on date")

    group.add_argument("-i", "--id", type=int, help="Filters transactions based customer id")

    group.add_argument("-d", "--date", type=str, help="Filters transactions based on order date")

    parser.add_argument("-o", "--output", type=str, default='results.csv', help="Changes the default file name to desired file name")

    parser.add_argument("-f", "--filename", type=str, help="Opens selected database file")


    args = parser.parse_args()

    conn = db.connect(args.filename)
    c = conn.cursor()

    output_data = None
    if args.name:
        output_data = get_transactions_by_name(c, args.name)
    if args.id:
        output_data = get_transaction_by_customer_id(c, args.id)
    if args.date:
        output_data = get_transaction_by_date(c, args.date)
        

    write_to_csv(output_data, args.output)
    conn.close()


if __name__ == "__main__":
    main()