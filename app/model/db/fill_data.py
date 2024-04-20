import psycopg2
from faker import Faker
from faker.providers.phone_number import Provider
import random
from datetime import datetime, timedelta

# Connect to your PostgreSQL database
'''conn_params = {
    'dbname': "Supermarket_Zlagoda",
    'user': "postgres",
    'password': "qawsed_Kli",
    'host': "localhost",
    'port': "5432"
}'''

'''conn = psycopg2.connect(
    dbname="zlagoda",
    user="postgres",
    password="qawsed_2A42_pzkpfw_V",
    host="db-zlagoda.cf4hhnfg01ca.eu-central-1.rds.amazonaws.com",
    port="5432"
)'''

"""conn = psycopg2.connect(
    dbname="DB_Zlagoda",
    user="DB_Zlagoda_owner",
    password="85rkPbEFmuDM",
    host="ep-aged-recipe-a2f1iyj1.eu-central-1.aws.neon.tech",
    # port="85"
)"""


class UkrainePhoneNumberProvider(Provider):
    """
    A Provider for Ukrainian phone numbers.
    """
    def ukraine_phone_number(self):
        return f'+380{self.random_number(digits=9)}'

conn_params = {
    "host": "ep-aged-recipe-a2f1iyj1.eu-central-1.aws.neon.tech",
    "database": "DB_Zlagoda",
    "user": "DB_Zlagoda_owner",
    "password": "85rkPbEFmuDM"
}

conn = psycopg2.connect(**conn_params)

# Create a cursor object
cur = conn.cursor()

# Instantiate Faker to generate fake data
fake = Faker()

fake.add_provider(UkrainePhoneNumberProvider)
print(fake.ukraine_phone_number())

# Instantiate Faker to generate fake data with Ukrainian locale
# fake = Faker('uk_UA')

# Function to generate fake employee data
# Counter for sequential keys
employee_counter = 1
customer_card_counter = 1
receipt_counter = 1
product_counter = 1
store_product_counter = 1
sale_counter = 1


# Function to generate fake employee data
def generate_employee_data():
    global employee_counter
    id_employee = f'EMP{str(employee_counter).zfill(3)}'
    employee_counter += 1
    empl_surname = fake.last_name()[:50]  # Limiting to 50 characters
    empl_name = fake.first_name()[:50]    # Limiting to 50 characters
    empl_patronymic = fake.first_name()[:50]  # Limiting to 50 characters
    empl_role = random.choice(['Manager', 'Supervisor', 'Clerk'])
    salary = round(random.uniform(1000, 5000), 2)
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=65)
    date_of_start = fake.date_between(start_date='-5y', end_date='today')
    # phone_number = fake.phone_number()[:13]  # Limiting to 13 characters
    phone_number = fake.ukraine_phone_number()[:13]  # Limiting to 13 characters
    fake.ukraine_phone_number()
    city = fake.city()[:50]  # Limiting to 50 characters
    street = fake.street_name()[:50]  # Limiting to 50 characters
    zip_code = fake.zipcode()[:9]  # Limiting to 9 characters
    return (id_employee, empl_surname, empl_name, empl_patronymic, empl_role, salary, date_of_birth, date_of_start, phone_number, city, street, zip_code)


# Function to generate fake customer card data
def generate_customer_card_data():
    global customer_card_counter
    card_number = f'CARD{str(customer_card_counter).zfill(3)}'
    customer_card_counter += 1
    cust_surname = fake.last_name()[:50]  # Limiting to 50 characters
    cust_name = fake.first_name()[:50]    # Limiting to 50 characters
    cust_patronymic = fake.first_name()[:50]  # Limiting to 50 characters
    phone_number = fake.phone_number()[:13]  # Limiting to 13 characters
    city = fake.city()[:50]  # Limiting to 50 characters
    street = fake.street_name()[:50]  # Limiting to 50 characters
    zip_code = fake.zipcode()[:9]  # Limiting to 9 characters
    c_percent = random.randint(1, 20)
    return (card_number, cust_surname, cust_name, cust_patronymic, phone_number, city, street, zip_code, c_percent)


# Function to generate fake receipt data
def generate_receipt_data():
    global receipt_counter
    check_number = f'CHK{str(receipt_counter).zfill(3)}'
    receipt_counter += 1
    id_employee = random.choice(employees)[0]
    card_number = random.choice(customer_cards)[0]
    print_date = fake.date_time_this_year()
    sum_total = round(random.uniform(10, 500), 2)
    vat = round(sum_total * 0.2, 2)
    return (check_number, id_employee, card_number, print_date, sum_total, vat)


# Function to generate fake category data
def generate_category_data():
    category_name = fake.word()[:50]  # Limiting to 50 characters
    return (category_name,)


# Function to generate fake product data
'''def generate_product_data():
    global product_counter
    product_name = fake.word()[:50]  # Limiting to 50 characters
    p_characteristics = fake.sentence()[:100]  # Limiting to 100 characters
    product_counter += 1
    return (product_name, p_characteristics)'''


# Function to generate fake product data
def generate_product_data():
    category_number = random.choice(categories)[0]
    product_name = fake.word()[:50]  # Limiting to 50 characters
    p_characteristics = fake.sentence()[:100]  # Limiting to 100 characters
    return (category_number, product_name, p_characteristics)

# Function to generate fake store product data
def generate_store_product_data():
    global store_product_counter
    UPC = f'UPC{str(store_product_counter).zfill(3)}'
    store_product_counter += 1
    # UPC_prom = random.choice(store_products)[0] if random.random() < 0.5 and store_products else None
    UPC_prom = None
    id_product = random.choice(products)[0]
    selling_price = round(random.uniform(10, 500), 2)
    products_number = random.randint(1, 100)
    promotional_product = random.choice([True, False])
    return (UPC, UPC_prom, id_product, selling_price, products_number, promotional_product)

# Function to generate fake sale data
def generate_sale_data():
    global sale_counter
    UPC = random.choice(store_products)[0]
    check_number = random.choice(receipts)[0]
    product_number = random.randint(1, 10)
    selling_price = round(random.uniform(10, 500), 2)
    sale_counter += 1
    return (UPC, check_number, product_number, selling_price)


# Populate Employee table
for _ in range(10):
    try:
        cur.execute("""
            INSERT INTO Employee (empl_surname, empl_name, empl_patronymic, empl_role, salary, date_of_birth, date_of_start, phone_number, city, street, zip_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, generate_employee_data()[1:])
        conn.commit()
    except (psycopg2.errors.UniqueViolation, psycopg2.errors.InFailedSqlTransaction) as e:
        print(e)
    finally:
        conn.commit()

# Retrieve existing employee data
cur.execute("SELECT id_employee FROM Employee")
employees = cur.fetchall()

# Populate Customer_Card table
for _ in range(10):
    try:
        cur.execute("""
            INSERT INTO Customer_Card (cust_surname, cust_name, cust_patronymic, phone_number, city, street, zip_code, c_percent)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, generate_customer_card_data()[1:])
        conn.commit()
    except (psycopg2.errors.UniqueViolation, psycopg2.errors.InFailedSqlTransaction) as e:
        print(e)
    finally:
        conn.commit()

# Retrieve existing customer card data
cur.execute("SELECT card_number FROM Customer_Card")
customer_cards = cur.fetchall()

# Populate Category table
for _ in range(10):
    try:
        cur.execute("""
            INSERT INTO Category (category_name)
            VALUES (%s)
        """, generate_category_data())
        conn.commit()
    except (psycopg2.errors.UniqueViolation, psycopg2.errors.InFailedSqlTransaction) as e:
        print(e)
    finally:
        conn.commit()

# Populate Receipt table
for _ in range(20):
    try:
        cur.execute("""
            INSERT INTO Receipt (id_employee, card_number, print_date, sum_total, vat)
            VALUES (%s, %s, %s, %s, %s)
        """, generate_receipt_data()[1:])
        conn.commit()
    except (psycopg2.errors.UniqueViolation, psycopg2.errors.InFailedSqlTransaction) as e:
        print(e)
    finally:
        conn.commit()

# Retrieve existing employee data
cur.execute("SELECT category_number FROM Category")
categories = cur.fetchall()

# Populate Product table
for _ in range(20):
    try:
        cur.execute("""
            INSERT INTO Product (category_number, product_name, p_characteristics)
            VALUES (%s, %s, %s)
        """, generate_product_data())
        conn.commit()
    except (psycopg2.errors.UniqueViolation, psycopg2.errors.InFailedSqlTransaction) as e:
        print(e)
    finally:
        conn.commit()

# Retrieve existing employee data
cur.execute("SELECT id_product FROM Product")
products = cur.fetchall()

# Populate Store_Product table
for _ in range(50):
    try:
        cur.execute("""
            INSERT INTO Store_Product (UPC_prom, id_product, selling_price, products_number, promotional_product)
            VALUES (%s, %s, %s, %s, %s)
        """, generate_store_product_data()[1:])
        conn.commit()
    except (psycopg2.errors.UniqueViolation, psycopg2.errors.InFailedSqlTransaction) as e:
        print(e)
    finally:
        conn.commit()

# Retrieve existing receipt data
cur.execute("SELECT check_number FROM Receipt")
receipts = cur.fetchall()

# Retrieve existing product data
cur.execute("SELECT id_product FROM Product")
products = cur.fetchall()

# Retrieve existing store product data
cur.execute("SELECT UPC FROM Store_Product")
store_products = cur.fetchall()

# Populate Sale table
for _ in range(200):
    try:
        cur.execute("""
            INSERT INTO Sale (UPC, check_number, product_number, selling_price)
            VALUES (%s, %s, %s, %s)
        """, generate_sale_data())
        conn.commit()
    except (psycopg2.errors.UniqueViolation, psycopg2.errors.InFailedSqlTransaction) as e:
        print(e)
    finally:
        conn.commit()

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

