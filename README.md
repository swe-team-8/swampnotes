# swampnotes
The team 8 repository for the swampnotes project

Before stating to code, you should install dependencies/set up your virtual environment (vscode) as outlined below. Dm me if you have any issues.

Python version: 3.11.1

cd apps/api

py -3.11 -m venv .venv # Create a virtual environment
.\.venv\Scripts\activate # Activate the virtual env.

python -m pip install -U pip (once in the venv)
python -m pip install -r requirements.txt 

Congratulations you have all the requirements installed

# for VS code select the venv's Python interpreter (3.11)
ctrl + shift + p -> Python:Select Interpreter
.\apps\api\.venv\Scripts\python.exe # Select this one or wherever python.exe lives within your venv

What else should you install?
vscode extensions (recommended): ESlint, Prettier, Tailwind CSS Intellisense, Python, Ruff, Even Better TOML

-git
-Node 20 LTS (20.18.1)
-nvm if you need to hop between node versions
-pnpm (package manager)
-npm (11.6.1) 
-Docker Desktop
-openssl
-AWS CLI
-PostgreSQL (version 18)

Docker compose (spin up the necessary containers): 
Make sure you're running this from the location of the docker-compose.yaml file
Or its path relative to the current directory location
docker compose -f docker-compose.yaml up -d      

Creating an alembic revision:
cd apps/api (make it from this location)
alembic revision --autogenerate -m "some title here"

Pulling an alembic revision from remote:
cd apps/api
alembic upgrade head

Now that I've finished configuring everything, here's how to go about spinning up our web app:

Terminal 1: 
cd apps/api
uvicorn src.main:app --reload --port 8000

Terminal 2:
cd apps/web
pnpm dev

This boots up our front/back-end, the database should already be up and running (via the containers/postgres) otherwise the terminal 1 step won't launch.

Navigate to http://localhost:3000 and you should see the front page! It's just the default Next.js page.tsx right now but here's where we'll see our changes in real time.