from app.model.dto.category import CategoryDTO
from app.model.repository.category import CategoryRepository


class CategoryInStockRepository:
    SELECT_CATEGORY_QUERY = """
    SELECT c.category_number, c.category_name
    FROM Category c
    WHERE EXISTS (
        SELECT *
        FROM Product p
        WHERE p.category_number = c.category_number
    ) 
    AND NOT EXISTS (
        SELECT *
        FROM Product p
        WHERE p.category_number = c.category_number
        AND NOT EXISTS (
            SELECT *
            FROM Store_Product sp
            WHERE sp.id_product = p.id_product
            AND sp.products_number > 0
        )
    );
    """

    def __init__(self, conn):
        self.conn = conn

    def get_categories(self):
        with self.conn.cursor() as cursor:
            cursor.execute(self.SELECT_CATEGORY_QUERY)
            categories = [
                CategoryDTO(row[0], row[1])
                for row in cursor.fetchall()
            ]
        return categories
