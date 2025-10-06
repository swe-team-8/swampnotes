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

