import datetime as dt
import database as db
import bcrypt
import sqlalchemy as sql
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base


class User(db.Base):
    __tablename__ = 'users'
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    email = sql.Column(sql.String, unique=True, index=True)
    hashed_password = sql.Column(sql.String)
    extend_existing = True
    tasks = orm.relationship("Task", back_populates="owner")

    def verify_password(self, password:str):
        #return hash.bcrypt.verify(password, self.hashed_password)
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))

class Status(sql.Enum):
    finalizado = 'Finalizado'
    backlog = 'Em Backlog'
    em_progresso = 'Em Progresso'

class Task(db.Base):
    __tablename__ = 'tasks'
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    name = sql.Column(sql.String, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey('users.id'))
    owner = orm.relationship("User", back_populates="tasks")
    description = sql.Column(sql.String, index=True)
    #situation = sql.Column(enum.Enum(Status.backlog, Status.em_progresso, Status.finalizado, names="Status"), nullable = False, default = Status.em_progresso)
    situation = sql.Column(sql.Enum(Status.backlog, Status.em_progresso, Status.finalizado))
    # situation = sql.Column(
    #     sql.Enum(Status, name="status"),
    #     nullable = False,
    #     default = Status.in_progress.name
    # )
    BR_TZ = dt.timezone(dt.timedelta(hours=-3))
    date_created = sql.Column(sql.DateTime, default=dt.datetime.now(BR_TZ))
    date_last_updated = sql.Column(sql.DateTime, default=dt.datetime.now(BR_TZ))
    date_start = sql.Column(sql.DateTime, default=dt.datetime.now(BR_TZ))
    date_end = sql.Column(sql.DateTime, default=dt.datetime.now(BR_TZ))