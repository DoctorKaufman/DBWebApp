-- Create table Employee
CREATE TABLE Employee (
    id_employee SERIAL PRIMARY KEY,
    empl_surname VARCHAR(50) NOT NULL,
    empl_name VARCHAR(50) NOT NULL,
    empl_patronymic VARCHAR(50),
    empl_role VARCHAR(10) NOT NULL,
    salary DECIMAL(13,4) NOT NULL,
    date_of_birth DATE NOT NULL,
    date_of_start DATE NOT NULL,
    phone_number VARCHAR(13) NOT NULL,
    city VARCHAR(50) NOT NULL,
    street VARCHAR(50) NOT NULL,
    zip_code VARCHAR(9) NOT NULL
);

-- Create table Employee_Account
CREATE TABLE Employee_Account (
    login VARCHAR(50) PRIMARY KEY,
    id_employee INT UNIQUE,
    password_hash VARCHAR(255), -- Storing password hash instead of plain password for security
    FOREIGN KEY (id_employee) REFERENCES Employee(id_employee)
);

-- Create table Customer_Card
CREATE TABLE Customer_Card (
    card_number SERIAL PRIMARY KEY,
    cust_surname VARCHAR(50) NOT NULL,
    cust_name VARCHAR(50) NOT NULL,
    cust_patronymic VARCHAR(50),
    phone_number VARCHAR(13) NOT NULL,
    city VARCHAR(50),
    street VARCHAR(50),
    zip_code VARCHAR(9),
    c_percent INT NOT NULL
);

-- Create table Category
CREATE TABLE Category (
    category_number SERIAL PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL
);

-- Create table Receipt
CREATE TABLE Receipt (
    check_number SERIAL PRIMARY KEY,
    id_employee INT NOT NULL REFERENCES Employee(id_employee) ON UPDATE CASCADE ON DELETE NO ACTION,
    card_number INT REFERENCES Customer_Card(card_number) ON UPDATE CASCADE ON DELETE NO ACTION,
    print_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    sum_total DECIMAL(13,4) NOT NULL,
    vat DECIMAL(13,4) NOT NULL
);

-- Create table Product
CREATE TABLE Product (
    id_product SERIAL PRIMARY KEY,
    category_number INT NOT NULL REFERENCES Category(category_number) ON UPDATE CASCADE ON DELETE NO ACTION,
    product_name VARCHAR(50) NOT NULL,
    p_characteristics VARCHAR(100) NOT NULL
);

-- Create table Store_Product
CREATE TABLE Store_Product (
    UPC SERIAL PRIMARY KEY,
    UPC_prom INT REFERENCES Store_Product(UPC) ON UPDATE CASCADE ON DELETE SET NULL,
    id_product INT NOT NULL REFERENCES Product(id_product) ON UPDATE CASCADE ON DELETE NO ACTION,
    selling_price DECIMAL(13,4) NOT NULL,
    products_number INT NOT NULL,
    promotional_product BOOLEAN NOT NULL
);

-- Create table Sale
CREATE TABLE Sale (
    UPC INT NOT NULL,
    check_number INT NOT NULL,
    product_number INT NOT NULL,
    selling_price DECIMAL(13,4) NOT NULL,
    PRIMARY KEY (UPC, check_number),
    FOREIGN KEY (UPC) REFERENCES Store_Product(UPC) ON UPDATE CASCADE ON DELETE NO ACTION,
    FOREIGN KEY (check_number) REFERENCES Receipt(check_number) ON UPDATE CASCADE ON DELETE CASCADE
);

