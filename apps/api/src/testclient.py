import requests
from models import User

# NOTE: RUNNING THE FILE MULTIPLE TIMES BEFORE RESTARTING THE SERVER
# MAY CAUSE ISSUES, BECAUSE THERE IS CURRENTLY NOT AN IMPLEMENTATION
# TO CHECK IF A USER ALREADY EXISTS BEFORE SIGNING UP.

# Use this file to see how to handle the jwt token.
# Ideally what is done here should be done in js.
# This file simulated a client.

# Prints "{'detail': 'Not authenticated'}"
print("Am I logged in? (No):", requests.get("http://localhost:8000/amiloggedin").json())

# Prints "{'error': 'Incorrect email or password. Please try again.'}"
print("Let me log in (user doesn't exist):", requests.post("http://localhost:8000/user/login",
                                    json={"email": "idontexist@ufl.edu", "password": "Nothing"}).json())

new_user = User()
new_user.email = "johndoe@ufl.edu"
new_user.password = "abc123"
new_user.id = 0
new_user.name = "John Doe"
new_user.school = "UFL"

# Create the token after signing up and *save* it for later use.
print("Let me sign up, Token: ", end="")
token = requests.post("http://localhost:8000/user/signup", json=new_user.model_dump()).json()['User Token']
print(token)

# {'detail': 'Not authenticated'}
print("Am I logged in? (Yes, but I didn't pass the token):", requests.get("http://localhost:8000/amiloggedin").json())

# {'Success': 'You are logged in!'}
print("Am I logged in? (Yes, and I passed the token):", requests.get("http://localhost:8000/amiloggedin",
                                                                    headers={"Authorization": f"Bearer {token}"}).json())

# Let me try to log in and save the new token
print("Let me log in (wrong password):", requests.post("http://localhost:8000/user/login",
                      json={"email": "johndoe@ufl.edu", "password":"WRONG"}).json())

token = requests.post("http://localhost:8000/user/login",
                      json={"email": "johndoe@ufl.edu", "password":"abc123"}).json()['User Token']

print("Using new token:")
print("Let me log in, Token:", token)

print("Am I logged in? (Yes, and I passed the token):", requests.get("http://localhost:8000/amiloggedin",
                                                                    headers={"Authorization": f"Bearer {token}"}).json())

print("Am I an admin? (no): ", requests.get("http://localhost:8000/amianadmin",
                                                                    headers={"Authorization": f"Bearer {token}"}).json())

new_user = User()
new_user.email = "admin@ufl.edu"
new_user.password = "abc123"
new_user.id = 0
new_user.name = "John Doe"
new_user.school = "UFL"

print("Let me sign up (admin), Token: ", end="")
token = requests.post("http://localhost:8000/user/signup", json=new_user.model_dump()).json()['User Token']
print(token)

print("Am I an admin? (yes): ", requests.get("http://localhost:8000/amianadmin",
                                                                    headers={"Authorization": f"Bearer {token}"}).json())