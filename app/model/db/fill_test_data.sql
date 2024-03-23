-- Populate Employee table
INSERT INTO Employee (id_employee, empl_surname, empl_name, empl_patronymic, empl_role, salary, date_of_birth, date_of_start, phone_number, city, street, zip_code)
VALUES 
('EMP001', 'Smith', 'John', 'William', 'Manager', 5000.0000, '1980-05-15', '2020-01-01', '+1234567890', 'New York', 'Main St', '10001'),
('EMP002', 'Johnson', 'Emily', 'Grace', 'Cashier', 3000.0000, '1990-08-20', '2020-02-15', '+1987654321', 'Los Angeles', 'Elm St', '90001'),
('EMP003', 'Garcia', 'Carlos', NULL, 'Salesman', 3500.0000, '1985-11-10', '2020-03-10', '+1765432109', 'Chicago', 'Oak St', '60601');

-- Populate Customer_Card table
INSERT INTO Customer_Card (card_number, cust_surname, cust_name, cust_patronymic, phone_number, city, street, zip_code, c_percent)
VALUES 
('CARD001', 'Brown', 'Emma', 'Elizabeth', '+1122334455', 'Houston', 'Maple St', '77001', 5),
('CARD002', 'Martinez', 'Jose', NULL, '+9988776655', 'Miami', 'Palm St', '33101', 10),
('CARD003', 'Jones', 'Sophia', 'Rose', '+5544332211', 'San Francisco', 'Cedar St', '94101', 0);

-- Populate Category table
INSERT INTO Category (category_name)
VALUES 
('Electronics'),
('Clothing'),
('Grocery');

-- Populate Product table
INSERT INTO Product (category_number, product_name, p_characteristics)
VALUES 
(1, 'Smartphone', 'Brand: XYZ, RAM: 8GB, Storage: 128GB'),
(2, 'T-Shirt', 'Color: Blue, Size: M'),
(3, 'Rice', 'Basmati Rice, 5kg Pack');

-- Populate Store_Product table
INSERT INTO Store_Product (UPC, UPC_prom, id_product, selling_price, products_number, promotional_product)
VALUES 
('123456789012', NULL, 1, 699.99, 50, FALSE),
('234567890123', NULL, 2, 19.99, 100, TRUE),
('345678901234', '234567890123', 3, 9.99, 200, FALSE);

-- Populate Receipt table
INSERT INTO Receipt (check_number, id_employee, card_number, print_date, sum_total, vat)
VALUES 
('CHK001', 'EMP001', 'CARD001', '2024-03-15 10:30:00', 759.98, 59.98),
('CHK002', 'EMP002', 'CARD002', '2024-03-15 11:45:00', 39.98, 3.98),
('CHK003', 'EMP003', NULL, '2024-03-15 13:15:00', 99.80, 9.80);

-- Populate Sale table
INSERT INTO Sale (UPC, check_number, product_number, selling_price)
VALUES 
('123456789012', 'CHK001', 1, 699.99),
('234567890123', 'CHK002', 2, 19.99),
('345678901234', 'CHK003', 3, 9.99);