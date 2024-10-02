import fastapi
import fastapi.security as security
import sqlalchemy.orm as orm
import services, schemas
from pydantic import TypeAdapter
from typing import List

app = fastapi.FastAPI()

@app.post("/api/users")
async def create_user(
    user: schemas.UserCreate,
    db: orm.Session = fastapi.Depends(services.get_db)
    ):
    db_user = await services.get_user_by_email(user.email, db)

    if db_user:
        raise fastapi.HTTPException(status_code=400, detail="Email já cadastrado.")

    user = await services.create_user(user, db)

    return await services.create_token(user)

@app.post("/api/token", response_model=dict)
async def create_token(
    form_data: security.OAuth2PasswordRequestForm = fastapi.Depends(),
    db: orm.Session = fastapi.Depends(services.get_db)
    ):

    user = await services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise fastapi.HTTPException(status_code=401, detail="Credenciais Inválidas.") 

    return await services.create_token(user)

@app.get("/api/users/me", response_model = schemas.User)
async def get_user(user: schemas.User = fastapi.Depends(services.get_current_user)):
    return user

@app.post("/api/tasks", response_model = schemas.Task)
async def create_task(
    task: schemas.TaskCreate,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db)
    ):

    return await services.create_task(user=user, db=db, task=task)


@app.get("/api/tasks", response_model = List[schemas.Task])
async def get_tasks(
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db)
    ):
        tasks = await services.get_tasks(user=user, db=db)
        adapter = TypeAdapter(List[schemas.Task])
        validated_tasks = adapter.validate_python(tasks)
        return validated_tasks
