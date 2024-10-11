"""
CRUD operations for the Payroll Service using direct AWS RDS PostgreSQL connection.
"""

from . import schemas, utils
import logging

logger = logging.getLogger(__name__)


# Employee CRUD Operations

def create_employee(db, employee: schemas.EmployeeCreate):
    """
    Create a new employee.
    """
    cursor = db.cursor()
    sql = """
        INSERT INTO employees (full_name, email, position, salary, date_hired)
        VALUES (%s, %s, %s, %s, %s) RETURNING id;
    """
    params = (
        employee.full_name,
        employee.email,
        employee.position,
        employee.salary,
        employee.date_hired
    )
    cursor.execute(sql, params)
    employee_id = cursor.fetchone()[0]
    db.commit()
    cursor.close()
    return get_employee(db, employee_id)


def get_employee(db, employee_id: int):
    """
    Retrieve an employee by ID.
    """
    cursor = db.cursor()
    sql = """
        SELECT id, full_name, email, position, salary, date_hired
        FROM employees WHERE id = %s;
    """
    cursor.execute(sql, (employee_id,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return schemas.Employee(
            id=row[0],
            full_name=row[1],
            email=row[2],
            position=row[3],
            salary=row[4],
            date_hired=row[5]
        )
    return None


# Payroll CRUD Operations

def create_payroll_record(db, payroll_request: schemas.PayrollCreate):
    """
    Create a new payroll record.

    Calculates taxes and deductions, and inserts the record into the database.
    """
    cursor = db.cursor()
    # Retrieve employee salary
    employee = get_employee(db, payroll_request.employee_id)
    if not employee:
        raise Exception("Employee not found")

    gross_pay = employee.salary / 12  # Assuming monthly payroll
    taxes = utils.calculate_taxes(gross_pay)
    deductions = utils.calculate_deductions(gross_pay)
    net_pay = gross_pay - taxes - deductions

    sql = """
        INSERT INTO payroll_records (employee_id, pay_date, gross_pay, net_pay, deductions, taxes)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
    """
    params = (
        payroll_request.employee_id,
        payroll_request.pay_date,
        gross_pay,
        net_pay,
        deductions,
        taxes
    )
    cursor.execute(sql, params)
    payroll_id = cursor.fetchone()[0]
    db.commit()
    cursor.close()
    return get_payroll_record(db, payroll_id)


def get_payroll_record(db, payroll_id: int):
    """
    Retrieve a payroll record by ID.
    """
    cursor = db.cursor()
    sql = """
        SELECT id, employee_id, pay_date, gross_pay, net_pay, deductions, taxes
        FROM payroll_records WHERE id = %s;
    """
    cursor.execute(sql, (payroll_id,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return schemas.PayrollRecord(
            id=row[0],
            employee_id=row[1],
            pay_date=row[2],
            gross_pay=row[3],
            net_pay=row[4],
            deductions=row[5],
            taxes=row[6]
        )
    return None
