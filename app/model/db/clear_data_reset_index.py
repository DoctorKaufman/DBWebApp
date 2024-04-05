import psycopg2

# Connection params
"""conn_params = {
    "host": "jdbc:postgresql://db-zlagoda.cf4hhnfg01ca.eu-central-1.rds.amazonaws.com:5432/zlagoda",
    "database": "Supermarket_Zlagoda",
    "user": "postgres",
    "password": "qawsed_Kli"
}"""

conn_params = {
    "host": "ep-aged-recipe-a2f1iyj1.eu-central-1.aws.neon.tech",
    "database": "DB_Zlagoda",
    "user": "DB_Zlagoda_owner",
    "password": "85rkPbEFmuDM"
}

# Clear data
def clear_tables():
    try:
        # Set conn
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()

        # Deletion
        tables = ["Sale", "Receipt", "Store_Product", "Product", "Category", "Customer_Card", "Employee"]
        for table in tables:
            cur.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
            print(f"Data cleared from table: {table}")

        # Commit and close
        conn.commit()
        cur.close()
        conn.close()
        print("All data cleared successfully.")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


if __name__ == "__main__":
    clear_tables()
