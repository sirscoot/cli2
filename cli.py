import argparse
import datetime
import sqlite3 as db
import csv


# filters all transactions based on customer id
def get_transaction_by_customer_id(c, id):
    c.execute(r"SELECT * FROM transactions WHERE customer_name=(SELECT customer_name FROM customers WHERE customer_id=?)", [id])
    return c.fetchall()



# shows all transactions filtered by customer name
def get_transactions_by_name(c, name):
    c.execute(r"SELECT * FROM transactions WHERE customer_name=?", [name])
    return c.fetchall()



# shows all transactions filted by date
def get_transaction_by_date(c, date):
    c.execute(r"SELECT * FROM transactions WHERE order_date=DATE(?)", [date])
    return c.fetchall()

# gives a range of order dates
def get_range_of_transactions(c, dateRange, customer_name=None, customer_id=None):
    split_date = dateRange.split(",")

    query_where = 'order_date BETWEEN DATE(?) AND DATE(?)'
    query_args = [split_date[0], split_date[1]]

    if customer_name is not None:
        query_where = f'{query_where} AND customer_name=?'
        query_args.append(customer_name)

    if customer_id is not None:
        query_where = f'{query_where} AND customer_name=(SELECT customer_name FROM customers WHERE customer_id=?)'
        query_args.append(customer_id)

    query_string = f"SELECT * FROM transactions WHERE {query_where}"
    c.execute(query_string, query_args)
    return c.fetchall()


# writes data to csv file
def write_to_csv(rows, output):
    with open(output, 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(['Transaction Id', 'Transaction Date', 'Transaction Price', 'Customer Name'])
        for row in rows:
            row_list = list(row)
            price_slice = str(row_list[2])
            priceSliceOne = price_slice[:-2]
            priceSliceTwo = price_slice[-2:]
            whole_price = f'{priceSliceOne}.{priceSliceTwo}'
            row_list[2] = whole_price
            csvWriter.writerow(row_list)

def main():

    # create the parser argument
    parser = argparse.ArgumentParser(description="Transaction manager")
    group = parser.add_mutually_exclusive_group()
    req_group = parser.add_mutually_exclusive_group()


    # parser argument
    group.add_argument("-n", "--name", type=str, help="Filters transactions based on date")
    group.add_argument("-i", "--id", type=int, help="Filters transactions based customer id")

    req_group.add_argument("-d", "--date", type=str, help="Filters transactions based on order date")
    req_group.add_argument("-r", "--daterange", type=str, help="Querys a range of transactions based off of order date")

    parser.add_argument("-o", "--output", type=str, default='results.csv', help="Changes the default file name to desired file name")
    parser.add_argument("-f", "--filename", type=str, help="Opens selected database file", required=True)


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
    if args.daterange and args.name:
        output_data = get_range_of_transactions(c, args.daterange, customer_name=args.name)
    if args.daterange and args.id:
        output_data = get_range_of_transactions(c, args.daterange, customer_id=args.id)
    if args.daterange and not args.id and not args.name:
        output_data = get_range_of_transactions(c, args.daterange)

    write_to_csv(output_data, args.output)
    conn.close()


if __name__ == "__main__":
    main()
