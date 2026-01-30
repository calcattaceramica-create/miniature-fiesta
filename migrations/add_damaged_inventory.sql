-- Migration: Add Damaged Inventory Support
-- Date: 2026-01-27
-- Description: Adds damaged_quantity field to stocks table and creates damaged_inventory table

-- Add damaged_quantity column to stocks table
ALTER TABLE stocks ADD COLUMN damaged_quantity REAL DEFAULT 0.0;

-- Update existing stocks to set damaged_quantity to 0
UPDATE stocks SET damaged_quantity = 0.0 WHERE damaged_quantity IS NULL;

-- Create damaged_inventory table
CREATE TABLE IF NOT EXISTS damaged_inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    warehouse_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    reason VARCHAR(200),
    damage_type VARCHAR(50),
    cost_value REAL DEFAULT 0.0,
    notes TEXT,
    user_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products (id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Update available_quantity calculation to include damaged_quantity
-- Note: This will be handled by the application logic
-- available_quantity = quantity - reserved_quantity - damaged_quantity

