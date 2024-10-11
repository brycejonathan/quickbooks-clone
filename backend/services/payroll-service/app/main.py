"""
Main module for the Payroll Service.

This module initializes the FastAPI app and defines the endpoints for managing employees
and processing payroll.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, crud, utils, database
import logging

# Initialize FastAPI app
app = FastAPI(title="Payroll Service", description="Employee and payroll management endpoints")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db():
    """
    Dependency to get a database connection.
    """
    db = database.get_connection()
    try:
        yield db
    finally:
        db.close()


# Employee Endpoints

@app.post("/employees/", response_model=schemas.Employee, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db=Depends(get_db)):
    """
    Create a new employee.

    Parameters:
    - employee: EmployeeCreate schema containing employee details.

    Returns:
    - Employee schema of the newly created employee.
    """
    try:
        result = crud.create_employee(db, employee)
        return result
    except Exception as e:
        logger.exception("Error creating employee")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/employees/{employee_id}", response_model=schemas.Employee)
def read_employee(employee_id: int, db=Depends(get_db)):
    """
    Retrieve an employee by ID.

    Parameters:
    - employee_id: ID of the employee.

    Returns:
    - Employee schema of the retrieved employee.
    """
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


# Payroll Endpoints

@app.post("/payroll/", response_model=schemas.PayrollRecord, status_code=status.HTTP_201_CREATED)
def process_payroll(payroll_request: schemas.PayrollCreate, db=Depends(get_db)):
    """
    Process payroll for an employee.

    Parameters:
    - payroll_request: PayrollCreate schema containing payroll details.

    Returns:
    - PayrollRecord schema of the processed payroll.
    """
    try:
        result = crud.create_payroll_record(db, payroll_request)
        return result
    except Exception as e:
        logger.exception("Error processing payroll")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/payroll/{payroll_id}", response_model=schemas.PayrollRecord)
def read_payroll(payroll_id: int, db=Depends(get_db)):
    """
    Retrieve a payroll record by ID.

    Parameters:
    - payroll_id: ID of the payroll record.

    Returns:
    - PayrollRecord schema of the retrieved payroll.
    """
    payroll_record = crud.get_payroll_record(db, payroll_id)
    if not payroll_record:
        raise HTTPException(status_code=404, detail="Payroll record not found")
    return payroll_record
