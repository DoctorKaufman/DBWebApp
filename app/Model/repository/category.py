import psycopg2
from psycopg2 import sql
from app.model.dto.category import CategoryDTO


class CategoryRepository:
    def __init__(self, conn):
        self.conn = conn

    def select_all_categories(self):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM category")
        cursor.execute(query)
        categories = []
        for category_data in cursor.fetchall():
            categories.append(CategoryDTO(category_data[0], category_data[1]))
        cursor.close()
        return categories

    def select_category(self, category_number):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM category WHERE category_number = %s")
        cursor.execute(query, (category_number,))
        category_data = cursor.fetchone()
        cursor.close()
        if category_data:
            return CategoryDTO(category_data[0], category_data[1])
        return None

    def insert_category(self, category):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO category (category_number, category_name) VALUES (%s, %s)")
        cursor.execute(query, (category.category_number, category.category_name))
        self.conn.commit()
        cursor.close()

    def update_category(self, category):
        cursor = self.conn.cursor()
        query = sql.SQL("UPDATE category SET category_name = %s WHERE category_number = %s")
        cursor.execute(query, (category.category_name, category.category_number))
        self.conn.commit()
        cursor.close()

    def delete_category(self, category_number):
        cursor = self.conn.cursor()
        query = sql.SQL("DELETE FROM category WHERE category_number = %s")
        cursor.execute(query, (category_number,))
        self.conn.commit()
        cursor.close()
