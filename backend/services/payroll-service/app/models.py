"""
Database models for the Payroll Service.

Defines SQL statements for creating the employees and payroll_records tables.
"""

employee_table_creation = """
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    position VARCHAR(100),
    salary NUMERIC(12, 2) NOT NULL,
    date_hired DATE NOT NULL
);
"""

payroll_record_table_creation = """
CREATE TABLE IF NOT EXISTS payroll_records (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id),
    pay_date DATE NOT NULL,
    gross_pay NUMERIC(12, 2) NOT NULL,
    net_pay NUMERIC(12, 2) NOT NULL,
    deductions NUMERIC(12, 2) NOT NULL,
    taxes NUMERIC(12, 2) NOT NULL
);
"""
