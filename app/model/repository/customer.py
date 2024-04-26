from app.model.dto.customer_dto import CustomerDTO


class CustomerRepository:
    SELECT_CUSTOMER_QUERY = """
    WITH MostCommonProduct AS (
        SELECT
            r.card_number,
            sp.UPC AS most_common_product_UPC,
            ROW_NUMBER() OVER (PARTITION BY r.card_number ORDER BY COUNT(*) DESC) AS rn
        FROM
            Receipt r
        JOIN
            Sale s ON r.check_number = s.check_number
        JOIN
            Store_Product sp ON s.UPC = sp.UPC
        GROUP BY
            r.card_number, sp.UPC
    ),
    MostCommonProductName AS (
        SELECT
            r.card_number,
            p.id_product AS most_common_product_id,
            p.product_name AS most_common_product_name,
            ROW_NUMBER() OVER (PARTITION BY r.card_number ORDER BY COUNT(*) DESC) AS rn
        FROM
            Receipt r
        JOIN
            Sale s ON r.check_number = s.check_number
        JOIN
            Store_Product sp ON s.UPC = sp.UPC
        JOIN
            Product p ON sp.id_product = p.id_product
        GROUP BY
            r.card_number, p.id_product, p.product_name
    )
    SELECT
        cc.card_number,
        cc.cust_surname,
        cc.cust_name,
        cc.phone_number,
        COUNT(r.check_number) AS total_purchases,
        COALESCE(SUM(r.sum_total), 0) AS total_amount_spent,
        ROUND(COALESCE(AVG(r.sum_total), 0), 2) AS average_purchase_amount,
        mcp.most_common_product_UPC,
        mcpn.most_common_product_name
    FROM
        Customer_Card cc
    LEFT JOIN
        Receipt r ON cc.card_number = r.card_number
    LEFT JOIN
        Sale s ON r.check_number = s.check_number
    LEFT JOIN
        MostCommonProduct mcp ON cc.card_number = mcp.card_number AND mcp.rn = 1
    LEFT JOIN
        MostCommonProductName mcpn ON cc.card_number = mcpn.card_number AND mcpn.rn = 1
    GROUP BY
        cc.card_number,
        cc.cust_surname,
        cc.cust_name,
        cc.phone_number,
        mcp.most_common_product_UPC,
        mcpn.most_common_product_name
    HAVING
        COALESCE(SUM(r.sum_total), 0) > %s
    ORDER BY
        total_amount_spent DESC;
    """

    def __init__(self, conn):
        self.conn = conn

    def get_customers(self, min_amount):
        with self.conn.cursor() as cursor:
            cursor.execute(CustomerRepository.SELECT_CUSTOMER_QUERY, (min_amount,))
            customers = [
                CustomerDTO(
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]
                )
                for row in cursor.fetchall()
            ]
        return customers

