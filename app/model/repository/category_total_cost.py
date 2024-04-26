import psycopg2
from psycopg2 import sql
from psycopg2.errors import InFailedSqlTransaction, ForeignKeyViolation

from app.model.dto.category_total_cost import CategoryTotalCostDTO


class CategoryTotalCostRepository:
    CATEGORY_TOTAL_COST_QUERY = sql.SQL("""
        SELECT 
            c.category_number,
            c.category_name,
            COALESCE(SUM(sp.selling_price * sp.products_number), 0) AS total_cost,
            COALESCE(SUM(sp.products_number), 0) AS total_quantity
        FROM 
            Category c
        LEFT JOIN 
            Product p ON c.category_number = p.category_number
        LEFT JOIN 
            Store_Product sp ON p.id_product = sp.id_product
        GROUP BY 
            c.category_number, c.category_name
        HAVING 
            COALESCE(SUM(sp.selling_price * sp.products_number), 0) > %s
        ORDER BY
            total_cost DESC;
    """)

    def __init__(self, conn):
        self.conn = conn

    def get_category_total_cost(self, given_number):
        with self.conn.cursor() as cursor:
            cursor.execute(CategoryTotalCostRepository.CATEGORY_TOTAL_COST_QUERY, (given_number,))
            rows = cursor.fetchall()
            categories = []
            for row in rows:
                category = CategoryTotalCostDTO(*row)
                categories.append(category)
        return tuple(categories)

