import cli
import sqlite3 as db

def test_customer_id_count(db_client, customer_id, expected_count):
    returned_rows = cli.get_transaction_by_customer_id(db_client, customer_id)

    if len(returned_rows) != expected_count:
        return False
    return True


if __name__ == "__main__":
    conn = db.connect('transactions-2010.db')
    c = conn.cursor()

    test_failed = False
    # Make one of these for each customer
    customer_id_count_test_cases = [[1, 31954]]
    for test_case in customer_id_count_test_cases:
        test_result = test_customer_id_count(c, test_case[0], test_case[1])
        if not test_result:
            test_failed = True
        print(f'TEST_CASE customer_id, input: {test_case[0]}, expected: {test_case[1]}, PASSED: {test_result}')

    if test_failed:
        print('Tests Failed.')
    else:
        print('Tests Passed.')

    # Make a test that validates for customer_name like the one above
    # Make a test that validates the counts for dates for --date and --datetrange
