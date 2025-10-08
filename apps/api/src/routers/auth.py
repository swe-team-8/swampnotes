from fastapi import APIRouter, Depends, HTTPException, FastAPI, Body  # noqa: F401
from pwdlib import PasswordHash

import apps.api.src.jwt_handler as jwt
from apps.api.src.models import UserLogin, User

# Skeleton authentication provider code
router = APIRouter()

users = []
password_hash = PasswordHash.recommended()

admins = ["admin@ufl.edu"]

# Replace with the correct way to determine if a user is an admin.
def is_admin(userID: str):
    return userID in admins


@router.post("/user/signup")
def signup(user: User = Body(default=None)):
    user.password = password_hash.hash(user.password) # Hash the password, we won't store passwords
    users.append(user) # TODO: Replace with a more permanent way of creating a user
    # TODO: Confirm email is valid and unique
    # TODO: Confirm that the user can sign up as their specified role
    return jwt.sign(user.email, is_admin(user.email))


def is_valid_login(attempt: UserLogin):
    # TODO: Replace with a proper way to verify login
    for user in users:
        if attempt.email == user.email and password_hash.verify(attempt.password, user.password):
            return True
    return False


@router.post("/user/login")
def login(user: UserLogin = Body(default=None)):
    if is_valid_login(user):
        return jwt.sign(user.email, is_admin(user.email))
    else:
        return {"error": "Incorrect email or password. Please try again."}


# An example function to check if a user is logged in
# Will show "You are logged in" to verified users,
# "You are not logged in" to unverified users.
# Use this example for future functions, like posting notes
# Or making transactions.
# Notice that all you need to do is add the argument:
# "dependencies=[Depends(jwt.jwtBearer())]"
@router.get("/amiloggedin", dependencies=[Depends(jwt.jwtBearer())])
def am_i_logged_in():
    return {"Success": "You are logged in!"}

# This is an example of how to verify if a user is an admin given their token.
@router.get("/amianadmin", dependencies=[Depends(jwt.jwtBearer())])
def am_i_an_admin(token_data: str = Depends(jwt.jwtBearer())):
    token = jwt.decode(token_data)
    return {"Decoded token": token, "am_i_admin": token["admin"]}