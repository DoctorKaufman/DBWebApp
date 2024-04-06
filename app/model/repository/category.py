import psycopg2
from psycopg2 import sql
from psycopg2.errors import InFailedSqlTransaction
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
        return tuple(categories)

    def select_category(self, category_number):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT * FROM category WHERE category_number = %s")
        cursor.execute(query, (category_number,))
        category_data = cursor.fetchone()
        cursor.close()
        if category_data:
            return CategoryDTO(category_data[0], category_data[1])
        return None

    """def insert_category(self, category):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO category (category_number, category_name) VALUES (%s, %s)")
        cursor.execute(query, (category.category_number, category.category_name))
        self.conn.commit()
        cursor.close()"""

    def insert_category(self, category):
        cursor = self.conn.cursor()
        query = sql.SQL("INSERT INTO category (category_name) VALUES (%s) RETURNING category_number")
        cursor.execute(query, (category.category_name,))
        category_number = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        if category_number:
            return CategoryDTO(category_number, category.category_name)
        return None

    def update_category(self, category):
        cursor = self.conn.cursor()
        query = sql.SQL("UPDATE category SET category_name = %s WHERE category_number = %s")
        cursor.execute(query, (category.category_name, category.category_number))
        self.conn.commit()
        cursor.close()

    def delete_category(self, category_number):
        cursor = self.conn.cursor()
        try:
            query = sql.SQL("DELETE FROM category WHERE category_number = %s")
            cursor.execute(query, (category_number,))
            self.conn.commit()
            cursor.close()
        except InFailedSqlTransaction as e:
            self.conn.rollback()
            cursor.close()
            return False
        finally:
            cursor.close()
        return True

    def exists_category(self, category_name):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT category_number FROM category WHERE category_name ILIKE %s")
        cursor.execute(query, (category_name,))
        category_number = cursor.fetchone()
        cursor.close()
        if category_number:
            return True
        return False

    def get_column_names(self):
        cursor = self.conn.cursor()
        query = sql.SQL("SELECT cols.column_name, "
                        "CASE WHEN tc.constraint_type = 'PRIMARY KEY' THEN FALSE ELSE TRUE END "
                        "FROM information_schema.columns AS cols "
                        "LEFT JOIN information_schema.key_column_usage AS pkuse "
                        "ON cols.table_schema = pkuse.constraint_schema "
                        "AND cols.table_name = pkuse.table_name "
                        "AND cols.column_name = pkuse.column_name "
                        "LEFT JOIN information_schema.table_constraints AS tc "
                        "ON pkuse.constraint_schema = tc.constraint_schema "
                        "AND pkuse.constraint_name = tc.constraint_name "
                        "WHERE cols.table_name = 'category'")
        cursor.execute(query)
        column_info = {row[0]: row[1] for row in cursor.fetchall()}
        cursor.close()
        return column_info
