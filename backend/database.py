import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm

DATABASE_URL = "sqlite:///./database.db"

engine = sql.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = sql.MetaData()
Base = declarative.declarative_base()

# Reflete as tabelas existentes e as remove
#metadata.reflect(bind=engine)
#metadata.drop_all(bind=engine)

