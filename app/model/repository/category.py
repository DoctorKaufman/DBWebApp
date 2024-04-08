import psycopg2
from psycopg2 import sql
from psycopg2.errors import InFailedSqlTransaction, ForeignKeyViolation
from app.model.dto.category import CategoryDTO


class CategoryRepository:
    """
    Repository class for managing categories in the database.
    """

    SELECT_ALL_CATEGORIES_QUERY = sql.SQL("SELECT * FROM category ORDER BY {} {}")
    SELECT_CATEGORY_QUERY = sql.SQL("SELECT * FROM category WHERE category_number = %s")
    INSERT_CATEGORY_QUERY = sql.SQL("INSERT INTO category (category_name) VALUES (%s) RETURNING category_number")
    UPDATE_CATEGORY_QUERY = sql.SQL("UPDATE category SET category_name = %s WHERE category_number = %s")
    DELETE_CATEGORY_QUERY = sql.SQL("DELETE FROM category WHERE category_number = %s")
    EXISTS_CATEGORY_QUERY = sql.SQL("SELECT category_number FROM category WHERE category_name ILIKE %s")
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
                                     "WHERE cols.table_name = 'category'")

    def __init__(self, conn):
        """
        Initialize CategoryRepository with a database connection.

        Parameters:
            conn: psycopg2 connection object.
        """
        self.conn = conn

    def select_all_categories(self, pageable):
        """
        Select all categories from the database.

        Returns:
            Tuple of CategoryDTO objects representing categories.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(CategoryRepository.SELECT_ALL_CATEGORIES_QUERY.format(sql.Identifier(pageable.column),
                                                                                 sql.SQL(pageable.order)))
            categories = [CategoryDTO(category_data[0], category_data[1]) for category_data in cursor.fetchall()]
        return tuple(categories)

    def select_category(self, category_number):
        """
        Select a category by its category number.

        Parameters:
            category_number: Category number to select.

        Returns:
            CategoryDTO object representing the selected category, or None if not found.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(CategoryRepository.SELECT_CATEGORY_QUERY, (category_number,))
            category_data = cursor.fetchone()
        if category_data:
            return CategoryDTO(category_data[0], category_data[1])
        return None

    def insert_category(self, category):
        """
        Insert a new category into the database.

        Parameters:
            category: CategoryDTO object representing the category to insert.

        Returns:
            CategoryDTO object representing the inserted category, or None if insertion fails.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(CategoryRepository.INSERT_CATEGORY_QUERY, (category.category_name,))
            category_number = cursor.fetchone()[0]
            self.conn.commit()
        if category_number:
            return CategoryDTO(category_number, category.category_name)
        return None

    def update_category(self, category):
        """
        Update a category in the database.

        Parameters:
            category: CategoryDTO object representing the category to update.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(CategoryRepository.UPDATE_CATEGORY_QUERY, (category.category_name, category.category_number))
            self.conn.commit()

    def delete_category(self, category_number):
        """
        Delete a category from the database.

        Parameters:
            category_number: Category number to delete.

        Returns:
            True if deletion succeeds, False otherwise.
        """
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(CategoryRepository.DELETE_CATEGORY_QUERY, (category_number,))
                self.conn.commit()
            except (ForeignKeyViolation, InFailedSqlTransaction):
                self.conn.rollback()
                return False
        return True

    def exists_category(self, category_name):
        """
        Check if a category with the given name exists in the database.

        Parameters:
            category_name: Name of the category to check.

        Returns:
            True if the category exists, False otherwise.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(CategoryRepository.EXISTS_CATEGORY_QUERY, (category_name,))
            category_number = cursor.fetchone()
        if category_number:
            return True
        return False

    def get_column_names(self):
        """
        Get column names of the 'category' table in the database.

        Returns:
            Dictionary where keys are column names and values indicate if the column is a primary key.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(CategoryRepository.GET_COLUMN_NAMES_QUERY)
            column_info = {row[0]: row[1] for row in cursor.fetchall()}
        return column_info
