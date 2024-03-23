import psycopg2

# Connection params
conn_params = {
    "host": "localhost",
    "database": "Supermarket_Zlagoda",
    "user": "postgres",
    "password": "qawsed_Kli"
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
            cur.execute(f"DELETE FROM {table};")
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