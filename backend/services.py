import models, schemas, database as db
import sqlalchemy.orm as orm
import passlib.hash as hash
import jwt
import fastapi
import fastapi.security as security

JWT_SECRET = 'mysupersecret'
oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/api/token")

def create_database():
    return db.Base.metadata.create_all(bind=db.engine)

def get_db():
    db_session = db.SessionLocal()

    try:
        yield db_session
    finally:
        db_session.close()

async def get_user_by_email(email: str, db: orm.Session):
    return db.query(models.User).filter(models.User.email == email).first()

async def create_user(user: schemas.UserCreate, db: orm.Session):
    user_obj = models.User(
        email=user.email, hashed_password=hash.bcrypt.hash(user.hashed_password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def get_current_user(
        db: orm.Session = fastapi.Depends(get_db),
        token: str = fastapi.Depends(oauth2schema)
    ):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("id")
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user is None:
            raise fastapi.HTTPException(status_code=401, detail="Usuário não encontrado")
    except jwt.ExpiredSignatureError:
        raise fastapi.HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise fastapi.HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        raise fastapi.HTTPException(status_code=401, detail="Erro de autenticação")

    return schemas.User.model_validate(user, from_attributes=True)

async def authenticate_user(email: str, password: str, db: orm.Session):
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user

async def create_token(user: models.User):
    user_obj = schemas.User.model_validate(user, from_attributes=True)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer")

async def create_task(user: schemas.User, db: orm.Session, task: schemas.TaskCreate):
    task_obj = models.Task(**task.dict(), owner_id = user.id)
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)

    return schemas.Task.model_validate(task_obj, from_attributes=True)

async def get_tasks(user: schemas.User, db: orm.Session):
    tasks = db.query(models.Task).filter_by(owner_id = user.id)
    return list(map(schemas.Task.model_validate, tasks))
