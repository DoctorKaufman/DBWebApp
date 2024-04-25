import psycopg2
from psycopg2 import sql
from psycopg2.errors import InFailedSqlTransaction, ForeignKeyViolation
from app.model.dto.store_product import StoreProductDTO
from app.model.dto.store_product_drop_list_position import StoreProductDropListPositionDTO
from app.model.dto.store_product_extended import StoreProductExtendedDTO
from app.model.dto.store_product_sales import StoreProductSalesDTO


class StoreProductRepository:
    """
    Repository class for managing store products in the database.
    """

    SELECT_ALL_STORE_PRODUCTS_QUERY = sql.SQL("SELECT * FROM store_product ORDER BY {} {}")
    SELECT_ALL_STORE_PRODUCTS_EXTENDED_QUERY = sql.SQL("SELECT sp.upc, sp.upc_prom, sp.id_product, p.product_name, "
                                                       "sp.selling_price, sp.products_number, sp.promotional_product "
                                                       "FROM store_product AS sp "
                                                       "INNER JOIN product AS p "
                                                       "ON sp.id_product = p.id_product "
                                                       "ORDER BY {} {}")
    SELECT_QUERY_TEMPLATE_EXT = sql.SQL("SELECT sp.upc, sp.upc_prom, sp.id_product, p.product_name, "
                                        "sp.selling_price, sp.products_number, sp.promotional_product "
                                        "FROM store_product AS sp "
                                        "INNER JOIN product AS p "
                                        "ON sp.id_product = p.id_product "
                                        "WHERE SIMILARITY({0}, %s) > 0.2 "
                                        "ORDER BY {1} {2}")
    SELECT_QUERY_TEMPLATE_EXT_BOOL = sql.SQL("SELECT sp.upc, sp.upc_prom, sp.id_product, p.product_name, "
                                             "sp.selling_price, sp.products_number, sp.promotional_product "
                                             "FROM store_product AS sp "
                                             "INNER JOIN product AS p "
                                             "ON sp.id_product = p.id_product "
                                             "WHERE sp.promotional_product = %s "
                                             "ORDER BY {0} {1}")
    SELECT_QUERY_TEMPLATE_EXT_BY_COL = sql.SQL("SELECT sp.upc, sp.upc_prom, sp.id_product, p.product_name, "
                                             "sp.selling_price, sp.products_number, sp.promotional_product "
                                             "FROM store_product AS sp "
                                             "INNER JOIN product AS p "
                                             "ON sp.id_product = p.id_product "
                                             "WHERE {0} = %s "
                                             "ORDER BY {1} {2}")
    SELECT_STORE_PRODUCT_DROP_LIST_QUERY = sql.SQL("SELECT spr.upc, pr.product_name "
                                                   "FROM store_product as spr "
                                                   "INNER JOIN product as pr "
                                                   "ON spr.id_product = pr.id_product")
    SELECT_STORE_PRODUCT_QUERY = sql.SQL("SELECT * FROM store_product WHERE UPC = %s")
    SELECT_STORE_PRODUCT_PROMOTIONAL_QUERY = sql.SQL("SELECT sp.upc, sp.upc_prom, sp.id_product, p.product_name, "
                                                     "sp.selling_price, sp.products_number, sp.promotional_product "
                                                     "FROM store_product AS sp "
                                                     "INNER JOIN product AS p "
                                                     "ON sp.id_product = p.id_product "
                                                     "WHERE promotional_product = %s")
    INSERT_STORE_PRODUCT_QUERY = sql.SQL("INSERT INTO store_product (UPC_prom, id_product, selling_price, "
                                         "products_number, promotional_product) "
                                         "VALUES (%s, %s, %s, %s, %s) RETURNING UPC")
    UPDATE_STORE_PRODUCT_QUERY = sql.SQL("UPDATE store_product SET UPC_prom = %s, id_product = %s, "
                                         "selling_price = %s, products_number = %s, promotional_product = %s "
                                         "WHERE UPC = %s RETURNING UPC")
    DELETE_STORE_PRODUCT_QUERY = sql.SQL("DELETE FROM store_product WHERE UPC = %s")
    GET_PRODUCT_SALES_QUERY = sql.SQL("SELECT sp.UPC, p.product_name, SUM(s.product_number) AS total_quantity_sold "
                                      "FROM Sale s "
                                      "INNER JOIN Store_Product sp ON s.UPC = sp.UPC "
                                      "INNER JOIN Product p ON sp.id_product = p.id_product "
                                      "INNER JOIN Receipt r ON s.check_number = r.check_number "
                                      "WHERE SIMILARITY(p.product_name, %s) > 0.2 "
                                      "AND DATE(r.print_date) >= %s "
                                      "AND DATE(r.print_date) <= %s "
                                      "GROUP BY sp.UPC, p.product_name")
    GET_COLUMN_NAMES_QUERY = sql.SQL("SELECT cols.column_name, "
                                     "CASE WHEN tc.constraint_type = 'PRIMARY KEY' THEN FALSE ELSE TRUE END "
                                     "FROM information_schema.columns AS cols "
                                     "LEFT JOIN information_schema.key_column_usage AS pkuse "
                                     "ON cols.table_schema = pkuse.constraint_schema "
                                     "AND cols.table_name = pkuse.table_name "
                                     "AND cols.column_name = pkuse.column_name "
                                     "LEFT JOIN information_schema.table_constraints AS tc "
                                     "ON pkuse.constraint_schema = tc.constraint_schema "
                                     "AND pkuse.constraint_name = tc.constraint_name "
                                     "WHERE cols.table_name = 'store_product'")
    GET_PRIMARY_KEY_NAME_QUERY = sql.SQL("SELECT cols.column_name FROM information_schema.columns AS cols "
                                         "JOIN information_schema.key_column_usage AS pkuse "
                                         "ON cols.table_schema = pkuse.constraint_schema "
                                         "AND cols.table_name = pkuse.table_name "
                                         "AND cols.column_name = pkuse.column_name "
                                         "JOIN information_schema.table_constraints AS tc "
                                         "ON pkuse.constraint_schema = tc.constraint_schema "
                                         "AND pkuse.constraint_name = tc.constraint_name "
                                         "WHERE cols.table_name = 'store_product' "
                                         "AND tc.constraint_type = 'PRIMARY KEY'")

    non_string_columns = {'upc', 'upc_prom', 'id_product', 'selling_price', 'products_number', 'promotional_product'}

    def __init__(self, conn):
        """
        Initialize StoreProductRepository with a database connection.

        Parameters:
            conn: psycopg2 connection object.
        """
        self.conn = conn

    def select_all_store_products(self, pageable):
        """
        Select all store products from the database.

        Parameters:
            pageable: Pageable class object containing parameters for ordering.

        Returns:
            Tuple of StoreProductDTO objects representing store products.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(
                StoreProductRepository.SELECT_ALL_STORE_PRODUCTS_QUERY.format(sql.Identifier(pageable.column),
                                                                              sql.SQL(pageable.order)))
            store_products = []
            for store_product_data in cursor.fetchall():
                store_products.append(StoreProductDTO(store_product_data[0], store_product_data[1],
                                                      store_product_data[2], store_product_data[3],
                                                      store_product_data[4], store_product_data[5]))
        return tuple(store_products)

    def select_all_store_products_extended(self, pageable):
        """
        Select all store products from the database with additional 'product_name' field.

        Parameters:
            pageable: Pageable class object containing parameters for ordering.

        Returns:
            Tuple of StoreProductExtendedDTO objects representing store products.
        """
        with self.conn.cursor() as cursor:
            if pageable.search_column and pageable.search_value:
                if pageable.search_column not in self.non_string_columns:
                    search_query = self.SELECT_QUERY_TEMPLATE_EXT.format(
                        sql.Identifier(pageable.search_column),
                        sql.SQL(pageable.column),
                        sql.SQL(pageable.order)
                    )
                    cursor.execute(search_query, (pageable.search_value,))
                else:
                    search_query = self.SELECT_QUERY_TEMPLATE_EXT_BY_COL.format(
                        sql.Identifier(pageable.search_column),
                        sql.SQL(pageable.column),
                        sql.SQL(pageable.order)
                    )
                    cursor.execute(search_query, (pageable.search_value,))
            else:
                cursor.execute(
                    StoreProductRepository.SELECT_ALL_STORE_PRODUCTS_EXTENDED_QUERY.format(
                        sql.Identifier(pageable.column),
                        sql.SQL(pageable.order)))
            store_products = []
            for store_product_data in cursor.fetchall():
                store_products.append(StoreProductExtendedDTO(store_product_data[0], store_product_data[1],
                                                              store_product_data[2], store_product_data[3],
                                                              store_product_data[4], store_product_data[5],
                                                              store_product_data[6]))
        return tuple(store_products)

    def select_promotional_products(self, is_promotional):
        with self.conn.cursor() as cursor:
            cursor.execute(StoreProductRepository.SELECT_STORE_PRODUCT_PROMOTIONAL_QUERY, (is_promotional,))
            store_products = []
            for store_product_data in cursor.fetchall():
                store_products.append(StoreProductExtendedDTO(store_product_data[0], store_product_data[1],
                                                              store_product_data[2], store_product_data[3],
                                                              store_product_data[4], store_product_data[5],
                                                              store_product_data[6]))
            return tuple(store_products)

    def select_store_products_drop_list(self):
        """
        Select all store products from the database to form drop list

        Returns:
            Tuple of StoreProductDropListPositionDTO objects representing products
            drop list positions.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(StoreProductRepository.SELECT_STORE_PRODUCT_DROP_LIST_QUERY)
            products = [StoreProductDropListPositionDTO(s_product_data[0], s_product_data[1]) for s_product_data in
                        cursor.fetchall()]
        return tuple(products)

    def select_store_product(self, upc):
        """
        Select a store product by its UPC.

        Parameters:
            upc: UPC of the store product.

        Returns:
            StoreProductDTO object representing the selected store product, or None if not found.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(StoreProductRepository.SELECT_STORE_PRODUCT_QUERY, (upc,))
            store_product_data = cursor.fetchone()
        if store_product_data:
            return StoreProductDTO(store_product_data[0], store_product_data[1],
                                   store_product_data[2], store_product_data[3],
                                   store_product_data[4], store_product_data[5])
        return None

    def insert_store_product(self, store_product):
        """
        Insert a new store product into the database.

        Parameters:
            store_product: StoreProductDTO object representing the store product to insert.

        Returns:
            StoreProductDTO object representing the inserted store product, or None if insertion fails.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(StoreProductRepository.INSERT_STORE_PRODUCT_QUERY,
                           (store_product.upc_prom, store_product.id_product, store_product.selling_price,
                            store_product.products_number, store_product.promotional_product))
            upc = cursor.fetchone()[0]
            self.conn.commit()
        cursor.close()
        if upc:
            return StoreProductDTO(upc, store_product.upc_prom, store_product.id_product,
                                   store_product.selling_price, store_product.products_number,
                                   store_product.promotional_product)
        return None

    def update_store_product(self, store_product):
        """
        Update an existing store product in the database.

        Parameters:
            store_product: StoreProductDTO object representing the store product to update.

        Returns:
            StoreProductDTO object representing the updated store product, or None if update fails.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(StoreProductRepository.UPDATE_STORE_PRODUCT_QUERY,
                           (store_product.upc_prom, store_product.id_product, store_product.selling_price,
                            store_product.products_number, store_product.promotional_product,
                            store_product.upc))
            self.conn.commit()

    def delete_store_product(self, upc):
        """
        Delete a store product from the database.

        Parameters:
            upc: UPC of the store product to delete.

        Returns:
            True if deletion succeeds, False otherwise.
        """
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(StoreProductRepository.DELETE_STORE_PRODUCT_QUERY, (upc,))
                self.conn.commit()
            except (ForeignKeyViolation, InFailedSqlTransaction):
                self.conn.rollback()
                return False
        return True

    def get_product_sales_over_period(self, pageable):
        """
        Get the total quantity of a product sold over a certain period.

        Parameters:
            pageable: The ProductSalesInputDTO containing product ID, start date, and end date.

        Returns:
            ProductSalesDTO object containing the UPC, product name, and total quantity sold over the period.
        """
        value = pageable.value
        start_date = pageable.start_date
        end_date = pageable.end_date

        with self.conn.cursor() as cursor:
            cursor.execute(StoreProductRepository.GET_PRODUCT_SALES_QUERY, (
                value,
                start_date,
                end_date
            ))
            row = cursor.fetchone()
            if row:
                upc, product_name, total_quantity_sold = row
                # return StoreProductSalesDTO(upc, product_name, total_quantity_sold)
                return total_quantity_sold
            else:
                return 0

    def get_column_names(self):
        """
        Get column names of the 'store_product' table in the database.

        Returns:
            Dictionary where keys are column names and values indicate if the column is a primary key.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(StoreProductRepository.GET_COLUMN_NAMES_QUERY)
            column_info = {row[0]: row[1] for row in cursor.fetchall()}
        return column_info

    def get_column_names_extended(self):
        """
        Get column names of the extended select query in the database.

        Returns:
            Dictionary where keys are column names and values indicate if the column is a primary key.
        """
        column_info = self.get_column_names()
        column_info['product_name'] = True
        return column_info

    def get_primary_key_name(self):
        """
        Get the name of the primary key column in the 'store_product' table.

        Returns:
            String representing the name of the primary key column, or None if not found.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(StoreProductRepository.GET_PRIMARY_KEY_NAME_QUERY)
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                return None
