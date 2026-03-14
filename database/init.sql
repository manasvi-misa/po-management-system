-- Create
CREATE DATABASE po_management;

-- Connecting
\c po_management;

-- Table 1 Vendors
CREATE TABLE vendors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(100) NOT NULL,
    rating NUMERIC(2,1) CHECK (rating >= 0 AND rating <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2 Products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    sku VARCHAR(50) UNIQUE NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL,
    stock_level INTEGER DEFAULT 0,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 3 Purchase Orders
CREATE TABLE purchase_orders (
    id SERIAL PRIMARY KEY,
    reference_no VARCHAR(50) UNIQUE NOT NULL,
    vendor_id INTEGER REFERENCES vendors(id) ON DELETE RESTRICT,
    total_amount NUMERIC(10,2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'Draft' CHECK (status IN ('Draft','Pending','Approved','Rejected')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 4 PO Items (products inside a PO)
CREATE TABLE po_items (
    id SERIAL PRIMARY KEY,
    po_id INTEGER REFERENCES purchase_orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL,
    subtotal NUMERIC(10,2) NOT NULL
);

-- Sample vendors
INSERT INTO vendors (name, contact, rating) VALUES
('Tech Supplies Co.', 'techsupplies@email.com', 4.5),
('Global Parts Ltd.', 'globalparts@email.com', 3.8),
('FastShip Inc.', 'fastship@email.com', 4.2);

-- Sample products
INSERT INTO products (name, sku, unit_price, stock_level, category) VALUES
('Laptop Stand', 'SKU-001', 29.99, 100, 'Electronics'),
('Wireless Mouse', 'SKU-002', 15.49, 200, 'Electronics'),
('Office Chair', 'SKU-003', 199.99, 50, 'Furniture'),
('Desk Lamp', 'SKU-004', 34.99, 150, 'Furniture'),
('USB Hub', 'SKU-005', 22.99, 80, 'Electronics');