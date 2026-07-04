-- NocoDB / PostgreSQL Database Schema for Invoice Processing

-- 1. Invoices Table
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    vendor VARCHAR(255) NOT NULL,
    vendor_uid VARCHAR(255),
    vendor_iban VARCHAR(255),
    invoice_number VARCHAR(255) NOT NULL,
    invoice_date DATE,
    due_date DATE,
    net_amount NUMERIC(15, 2),
    vat_amount NUMERIC(15, 2),
    vat_percent NUMERIC(5, 2),
    gross_amount NUMERIC(15, 2),
    currency VARCHAR(10) DEFAULT 'USD',
    cost_center VARCHAR(255) DEFAULT 'General',
    status VARCHAR(50) DEFAULT 'Draft', -- 'Draft', 'Fully Approved', 'Rejected', 'Needs Review'
    send_for_approval BOOLEAN DEFAULT FALSE,
    selected_departments VARCHAR(255),
    original_pdf_url TEXT, -- Or an attachment column in NocoDB
    confidence_score NUMERIC(5, 4),
    anomalies TEXT, -- JSON or comma-separated
    email_sender VARCHAR(255),
    email_subject TEXT,
    email_received_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Unique constraint to help with Duplicate Detection (Invoice Number + Vendor)
-- Note: NocoDB handles unique constraints via its UI.
ALTER TABLE invoices ADD CONSTRAINT unique_invoice_vendor UNIQUE (invoice_number, vendor);

-- 2. Line Items Table
CREATE TABLE line_items (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    quantity NUMERIC(10, 2) NOT NULL,
    unit_price NUMERIC(15, 2) NOT NULL,
    total NUMERIC(15, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Audit Logs Table
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(100), -- e.g., 'Invoice'
    entity_id INTEGER,
    action VARCHAR(255) NOT NULL, -- e.g., 'Email Received', 'AI Processing Complete', 'Approved', 'Rejected'
    details TEXT, -- JSON representation of changes or errors
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Note for NocoDB Setup:
-- 1. Create a new project in NocoDB connecting to a PostgreSQL/MySQL database, or use the default SQLite.
-- 2. You can execute this SQL script in your database before connecting NocoDB, and NocoDB will auto-sync the tables.
-- 3. Alternatively, you can create these tables manually via the NocoDB UI with the exact column names above.
-- 4. For `original_pdf_url`, use NocoDB's "Attachment" column type if you prefer uploading files directly.
