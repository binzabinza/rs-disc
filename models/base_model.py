from sqlalchemy.ext.declarative import declarative_base, declared_attr

import inflect
import re
from typing import TypeVar, Any, List
import abc

import db_manager as db

__all__ = [
    'Model'
]


_inflect_engine = inflect.engine()


T = TypeVar('T', bound='BaseModel')


Base = declarative_base()
"""Base model type."""


class Model(Base):
    """
    Base model class.
    """

    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        words = [
            word.lowercase()
            for word in
            re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', cls.__name__)
        ]
        words[-1] = _inflect_engine.plural(words[-1])
        return '_'.join(words)

    @classmethod
    def fetch_all(cls: T, session: db.Session = None) -> List[T]:
        if not session:
            with db.session_scope() as session:
                result = session.query(cls).all()
                session.expunge_all()
                return result
        else:
            return session.query(cls).all()

    @classmethod
    def fetch_by_primary(cls: T, primary: Any, session: db.Session = None) -> T:
        if not session:
            with db.session_scope() as session:
                result = session.query(cls).get(primary)
                session.expunge_all()
                return result
        else:
            return session.query(cls).get(primary)

    @classmethod
    def fetch_where(cls: T, session: db.Session = None, **kwargs):
        if not session:
            with db.session_scope() as session:
                result = session.query(cls).filter_by(**kwargs).all()
                session.expunge_all()
                return result
        else:
            return session.query(cls).filter_by(**kwargs).all()

    def save_in(self, session: db.Session):
        session.merge(self)

