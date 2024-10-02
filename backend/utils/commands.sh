python -m pip install passlib SQLAlchemy fastapi pyjwt pydantic alembic

python -m pip install passlib pydantic

uvicorn main:app --reload

python -m pip freeze > requirements.txt

python -m pip install -r requirements.txt

python -m pip uninstall bcrypt

python -m pip install bcrypt==4.0.1

Set-ExecutionPolicy RemoteSigned -Scope Process

# Apague o arquivo do banco de dados existente
rm database.db
