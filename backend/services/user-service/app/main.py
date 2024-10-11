"""
Main module for the User Service.

This module initializes the FastAPI app and defines the endpoints for user registration,
authentication, and user profile management.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, crud, auth, database, utils
import logging
from fastapi.security import OAuth2PasswordRequestForm

# Initialize FastAPI app
app = FastAPI(title="User Service", description="User management endpoints")

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


@app.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db=Depends(get_db)):
    """
    Register a new user.

    Parameters:
    - user: UserCreate schema containing user registration data.

    Returns:
    - User schema of the newly created user.
    """
    try:
        db_user = crud.get_user_by_email(db, user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = utils.get_password_hash(user.password)
        user.password = hashed_password
        return crud.create_user(db, user)
    except Exception as e:
        logger.exception("Error registering user")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/login", response_model=schemas.Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    """
    Authenticate a user and return a JWT token.

    Parameters:
    - form_data: OAuth2PasswordRequestForm containing username and password.

    Returns:
    - Token schema containing the access token and token type.
    """
    try:
        user = crud.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token = auth.create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.exception("Error during login")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Get the current authenticated user's information.

    Returns:
    - User schema of the current user.
    """
    return current_user
