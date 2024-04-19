import psycopg2

conn_params = {
    'dbname': "Supermarket_Zlagoda",
    'user': "postgres",
    'password': "qawsed_Kli",
    'host': "localhost",
    'port': "5432"
}

'''conn_params = {
    "host": "ep-aged-recipe-a2f1iyj1.eu-central-1.aws.neon.tech",
    "database": "DB_Zlagoda",
    "user": "DB_Zlagoda_owner",
    "password": "85rkPbEFmuDM"
}'''

# Drop all tables
def drop_tables():
    try:
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()

        tables = ["Sale", "Receipt", "Store_Product", "Product", "Category", "Customer_Card", "Employee", "Employee_Account"]
        for table in tables:
            cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
            print(f"Table dropped: {table}")

        conn.commit()
        cur.close()
        conn.close()
        print("All tables dropped successfully.")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


if __name__ == "__main__":
    drop_tables()
