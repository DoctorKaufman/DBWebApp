from app.controllers.mapper.mapper import ReceiptMapper


class ReceiptService:
    def __init__(self, receipt_repository, sales_repository):
        self.receipt_repository = receipt_repository
        self.sales_repository = sales_repository

    def get_receipt_columns(self):
        return ReceiptMapper.map_columns(self.receipt_repository.get_column_names())

    def get_all_receipts(self, pageable):
        # receipts = self.receipt_repository.select_all_receipts(pageable)
        receipts = self.receipt_repository.select_all_receipts_ext(pageable)
        for receipt in receipts:
            products = self.sales_repository.select_check_sale_ext(receipt.check_number)
            receipt.set_additional_info(products)
        # select_check_sale_ext
        return receipts
        # return receipts
        # receipts_dto = []
        # for receipt in receipts:
        #     sales_map = {}

