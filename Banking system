import random
import luhn
import sqlite3
conn = sqlite3.connect('card.s3db')  # create DB : card.s3db
cur = conn.cursor()  # create cursor object to execute
login_cardnum = ""
# cur.execute("DROP TABLE card")
# create table card inside card.s3db database with 4 fields NB id should autoincrement as primary key
cur.execute("""CREATE TABLE IF NOT EXISTS card (
    id INTEGER DEFAULT 0,
    number TEXT, 
    pin TEXT, 
    balance INTEGER DEFAULT 0)""")

conn.commit()  # commit DB changes


def check_sum(card_num):  # this doesn't get called - faulty luhn...
    res = [int(x) for x in str(card_num)]
    processed_numbers = [x*2 if i % 2 else x for i, x in enumerate(res)]
    more_processed_numbers = [(num - 9 if num > 9 else num) for num in processed_numbers]
    total_processed_numbers = sum(more_processed_numbers)
    check_sum_count = 0
    while total_processed_numbers % 10 != 0:
        total_processed_numbers = total_processed_numbers + 1
        check_sum_count += 1
    return check_sum_count


def create_account():
    root_iin_num = "400000"
    customer_num = str(random.randint(99999999, 999999999))
    checksum_digit = luhn.generate(root_iin_num + customer_num)
    account_num = root_iin_num + customer_num + str(checksum_digit)  # generates account number
    sql_select_query = """select * from card where id = ?"""
    cur.execute(sql_select_query, (account_num,))
    result = cur.fetchone()
    if result:
        create_account()
    else:
        pin = str(random.randint(999, 9999))
        cur.execute("INSERT INTO card (number, pin) VALUES(?, ?)", (account_num, pin))
    conn.commit()
    print("Your card has been created\nYour card number:", account_num, "\nYour card PIN:")
    print(pin)  # select pin from cards dbase


def log_in():
    user_input_card: str = str(input("Enter your card number:"))
    user_input_pin = str(input("Enter your PIN:"))
    cur.execute("SELECT number FROM card")
    result = cur.fetchall()
    result_flat_list = []
    for sublist in result:
        for item in sublist:
            result_flat_list.append(item)
    if user_input_card not in result_flat_list:
        print("Wrong card number or PIN!\n")
    cur.execute("SELECT pin FROM card")
    pin_result = cur.fetchall()
    pin_result_flat_list = []
    for sublist in pin_result:
        for item in sublist:
            pin_result_flat_list.append(item)
    if user_input_pin not in pin_result_flat_list:
        print("Wrong card number or PIN!\n")
    else:
        print("You have successfully logged in!\n")
        global login_cardnum
        login_cardnum = user_input_card
        check_balance()


def check_balance():
    user_input_balance = input("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n")
    if user_input_balance == str(1):
        cur.execute('SELECT balance FROM card WHERE number = ?', (login_cardnum,))
        balance_result = cur.fetchone()
        print("Balance:", balance_result[0], "\n")
        check_balance()
    elif user_input_balance == str(2):
        add_income()
    elif user_input_balance == str(3):
        do_transfer()
    elif user_input_balance == str(4):
        close_account()
    elif user_input_balance == str(5):
        print("You have successfully logged out!\n")
        pass
    elif user_input_balance == str(0):
        print("Bye!")
        exit()


def do_transfer():  # using login_cardnum
    user_input_transfer = input("1. Enter card number:\n")

    if luhn.verify(user_input_transfer):
        cur.execute("SELECT number FROM card")
        result = cur.fetchall()
        result_flat_list = []
        for sublist in result:
            for item in sublist:
                result_flat_list.append(item)
        if user_input_transfer not in result_flat_list:
            print("Such a card does not exist.\n")    # this is used twice - method?
            check_balance()
        else:
            user_input_transfer_amount = input("Enter how much money you want to transfer:\n")
    else:
        print("Probably you made a mistake in the card number. Please try again!\n")
        check_balance()

    cur.execute('SELECT balance FROM card WHERE number = ?', (login_cardnum,))
    balance_result = cur.fetchone()
    if int(user_input_transfer_amount) > balance_result[0]:
        print("Not enough money!")
        check_balance()
    else:
        cur.execute('SELECT balance FROM card WHERE number = ?', (user_input_transfer,))
        balance_result = cur.fetchone()
        new_transfer_balance = int(user_input_transfer_amount) + balance_result[0]
        cur.execute('UPDATE card SET balance = ? WHERE number = ?', (new_transfer_balance, user_input_transfer,))
        conn.commit()
        print("Success!\n")
        #  deduct amount and commit changes
        cur.execute('SELECT balance FROM card WHERE number = ?', (login_cardnum,))
        balance_result = cur.fetchone()
        post_transfer_balance = balance_result[0] - int(user_input_transfer_amount)
        cur.execute('UPDATE card SET balance = ? WHERE number = ?', (post_transfer_balance, login_cardnum,))
        conn.commit()
        check_balance()


def add_income():   # using login_cardnum
    cur.execute('SELECT balance FROM card WHERE number = ?', (login_cardnum,))
    balance_result = cur.fetchone()
    user_input_add_income = input("Enter income:")
    new_balance = int(user_input_add_income) + balance_result[0]
    cur.execute('UPDATE card SET balance = ? WHERE number = ?', (new_balance, login_cardnum,))
    conn.commit()
    print("Income was added!\n")
    check_balance()


def close_account():   # using login_cardnum
    cur.execute('DELETE FROM card WHERE number = ?', (login_cardnum,))
    conn.commit()
    print('The account has been closed!')
    pass


while True:
    user_input = input("1. Create an Account\n2. Log into account\n0. Exit\n")
    if user_input == str(1):
        create_account()
    elif user_input == str(2):
        log_in()
    elif user_input == str(0):
        print("Bye!")
        exit()
