import sys
from typing import List
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.orm import Session

from src.exceptions import NotFoundException

from src.schemas.schemas import InputModel

def get_all(db: Session, model: DeclarativeMeta, **kwargs) -> List[DeclarativeMeta]:
    query = db.query(model)
    if "between" in kwargs:
        query = query.filter(kwargs["between"][0].between(kwargs["between"][1], kwargs["between"][2]))
        del kwargs["between"]
    if "in_" in kwargs:
        query = query.filter(kwargs["in_"][0].in_(kwargs["in_"][1]))
        del kwargs["in_"]
    if kwargs:
        query = query.filter_by(**kwargs)
    return query.all()

def get_by_id(db: Session, model: DeclarativeMeta, id: int) -> DeclarativeMeta:
    data = db.query(model).get(id)
    if data == None:
        raise NotFoundException(f"{model.__tablename__} not found").with_traceback(sys.exc_info()[2])
    return data


def create(db: Session, model: DeclarativeMeta, data: InputModel) -> DeclarativeMeta:
    new_data = model(**data.__dict__)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data