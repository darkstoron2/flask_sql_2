import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Hazards(SqlAlchemyBase):
    __tablename__ = 'hazards'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    jobs_title = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("jobs.id"), nullable=True)
    hazard = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
