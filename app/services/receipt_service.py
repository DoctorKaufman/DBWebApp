from datetime import datetime

from app.controllers.dtos.create.check_creation import ReceiptCreationDTO
from app.controllers.handler.exceptions import CheckCreationException
from app.controllers.mapper.mapper import ReceiptMapper
from app.model.dto.receipt import ReceiptDTO
from app.model.dto.receipt_ext import ReceiptExtDTO
from app.model.dto.sale import SaleDTO
from app.model.repository.customer_card import CustomerCardRepository
from app.model.repository.receipt import ReceiptRepository
from app.model.repository.sale import SaleRepository
from app.model.repository.store_product import StoreProductRepository


class ReceiptService:
    def __init__(self, receipt_repository: ReceiptRepository, sales_repository: SaleRepository,
                 store_product_repository: StoreProductRepository, customer_repository: CustomerCardRepository):
        self.receipt_repository = receipt_repository
        self.sales_repository = sales_repository
        self.store_product_repository = store_product_repository
        self.customer_repository = customer_repository

    def get_receipt_columns(self):
        return ReceiptMapper.map_columns(self.receipt_repository.get_column_names())

    def select_by_check_num(self, check_number):
        receipt = self.receipt_repository.select_receipt_ext(check_number)
        products = self.sales_repository.select_check_sale_ext(receipt.check_number)
        receipt.set_sales_info(products)
        return receipt

    def get_all_receipts(self, pageable):
        receipts = self.receipt_repository.select_all_receipts_ext(pageable)
        for receipt in receipts:
            self.find_check_products(receipt)
        return receipts

    def get_all_receipts_with_condition(self, recept_pageable):
        receipts = self.receipt_repository.select_cashier_receipts_ext(recept_pageable)
        for receipt in receipts:
            self.find_check_products(receipt)
        return receipts

    def get_sum_of_checks_period(self, recept_pageable):
        return self.receipt_repository.calculate_total_sales_by_cashier(recept_pageable)

    def create_receipt(self, receipt_creation_dto: ReceiptCreationDTO):
        total_price = self.calculate_total_price(receipt_creation_dto.bought_products)
        vat = total_price * 0.2
        if receipt_creation_dto.card_number:
            c_percent = self.customer_repository.get_customer_percent(receipt_creation_dto.card_number)
            total_price *= (100.0 - c_percent) / 100.0
        total_price += vat
        date = datetime.now()
        receipt_dto = ReceiptDTO(0, receipt_creation_dto.id_employee, receipt_creation_dto.card_number,
                                 date, total_price, vat)
        receipt = self.receipt_repository.insert_receipt(receipt_dto)
        try:
            bought_products = self.merge_items(receipt_creation_dto.bought_products)
            for prod in bought_products:
                self.write_off_products(prod.upc, prod.amount)
                self.sales_repository.insert_sale(SaleDTO(prod.upc, receipt.check_number, prod.amount, prod.price))
        except CheckCreationException as e:
            self.delete_receipt(receipt.check_number)
            raise e
    #     TODO what to return

    def merge_items(self, bought_products):
        merged_items = {}
        for product in bought_products:
            upc = product.upc
            if upc in merged_items:
                merged_items[upc].set_amount(merged_items[upc].amount + product.amount)
            else:
                merged_items[upc] = product
        return list(merged_items.values())

    def write_off_products(self, upc, amount):
        store_product = self.store_product_repository.select_store_product(upc)
        new_amount = store_product.products_number - amount
        if new_amount < 0:
            print(f"Trying to write off too much products. Amount in storage: {store_product.products_number}. "
                  f"Amount in receipt: {amount}")
            raise CheckCreationException("Can't write off too much product from storage")
        store_product.set_products_number(store_product.products_number - amount)
        self.store_product_repository.update_store_product(store_product)

    def calculate_total_price(self, bought_products):
        total_price = 0
        for elem in bought_products:
            total_price += elem.amount * elem.price
        return total_price

    def find_check_products(self, receipt: ReceiptExtDTO):
        products = self.sales_repository.select_check_sale_ext(receipt.check_number)
        receipt.set_sales_info(products)

    def delete_receipt(self, check_num):
        self.receipt_repository.delete_receipt(check_num)
