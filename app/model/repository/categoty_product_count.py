from psycopg2 import sql

from app.model.dto.category_product_count import CategoryProductCountDTO


class CategoryProductCountRepository:
    CATEGORY_PRODUCT_COUNT_QUERY = sql.SQL("""
        SELECT 
            c.category_number,
            c.category_name,
            COALESCE(SUM(CASE WHEN sp.promotional_product THEN 1 ELSE 0 END), 0) AS promotional_products_count,
            COALESCE(SUM(CASE WHEN NOT sp.promotional_product THEN 1 ELSE 0 END), 0) AS non_promotional_products_count
        FROM Category c
        LEFT JOIN Product p 
        ON c.category_number = p.category_number
        LEFT JOIN Store_Product sp 
        ON p.id_product = sp.id_product
        GROUP BY c.category_number, c.category_name;
    """)

    def __init__(self, conn):
        self.conn = conn

    def get_category_product_counts(self):
        with self.conn.cursor() as cursor:
            cursor.execute(CategoryProductCountRepository.CATEGORY_PRODUCT_COUNT_QUERY)
            rows = cursor.fetchall()
            counts = []
            for row in rows:
                count = CategoryProductCountDTO(*row)
                counts.append(count)
        return tuple(counts)

