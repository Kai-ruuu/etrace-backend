from sqlalchemy import or_, func, cast, String
from sqlalchemy.orm import Session, joinedload, selectinload

from app.exceptions import *
from app.models.all import School, Account
from app.utils.model import paginate, to_pymodels
from app.schemas.school import SchoolOut, SchoolIn, SchoolUpdate

def get_school_by_id(
    db: Session,
    id: int,
    *,
    allow_none: bool=False,
    as_pymodel: bool=False
) -> School | SchoolOut:
    school = db.query(School).filter(School.id == id).first()

    if not school and not allow_none:
        raise SCHOOL_NOT_FOUND_EXCEPTION
    
    if as_pymodel:
        return SchoolOut.model_validate(school)
    
    return school

def get_school_by_name(
    db: Session,
    name: str,
    *,
    allow_none: bool=False,
    as_pymodel: bool=False
) -> School | SchoolOut:
    school = db.query(School).filter(School.name == name).first()

    if not school and not allow_none:
        raise SCHOOL_NOT_FOUND_EXCEPTION
    
    if as_pymodel:
        return SchoolOut.model_validate(school)
    
    return school

def get_schools(
    db: Session,
    user: Account,
    *,
    is_archived: bool | None=None,
    search: str | None=None,
    page: int=1,
    size: int=20,
    as_pymodels: bool=False
) -> School | SchoolOut:
    if not user.can_manage_schools:
        raise UNAUTHORIZED_ACCESS_EXCEPTION

    query = db.query(School)
    
    if is_archived is not None:
        query = query.filter(School.is_archived == is_archived)

    if search:
        query = (
            query.distinct(School.id)
            .filter(School.name.ilike(f"%{search}%"))
        )
    
    total, schools = paginate(query, page=page, size=size, distinct_col=School.id)

    if as_pymodels:
        return {
            "page": page,
            "size": size,
            "total": total,
            "items": to_pymodels(schools, SchoolOut)
        }
    
    return schools

def create_school(
    db: Session,
    payload: SchoolIn,
    user: Account,
    *,
    as_pymodel: bool=False
) -> School | SchoolOut:
    if not user.can_manage_schools:
        raise UNAUTHORIZED_ACCESS_EXCEPTION
    
    if get_school_by_name(db=db, name=payload.name, allow_none=True):
        raise SCHOOL_ALREADY_EXISTS_EXCEPTION
    
    new_school = School(name=payload.name)
    db.add(new_school)
    db.commit()
    db.refresh(new_school)

    if as_pymodel:
        return SchoolOut.model_validate(new_school)
    
    return new_school

def update_school_by_id(
    db: Session,
    id: int,
    payload: SchoolUpdate,
    user: Account,
    *,
    as_pymodel: bool=False
) -> School | SchoolOut:
    if not user.can_manage_schools:
        raise UNAUTHORIZED_ACCESS_EXCEPTION
    
    # get school or block request if school is not found
    db_school = get_school_by_id(db=db, id=id, allow_none=False)
    db_school.name = payload.name
    db.commit()
    db.refresh(db_school)

    if as_pymodel:
        return SchoolOut.model_validate(db_school)
    
    return db_school

def archive_school_by_id(
    db: Session,
    id: int,
    user: Account,
    *,
    as_pymodel: bool=False
) -> School | SchoolOut:
    if not user.can_manage_schools:
        raise UNAUTHORIZED_ACCESS_EXCEPTION
    
    # get school or block request if school is not found
    db_school = get_school_by_id(db=db, id=id, allow_none=False)
    
    if db_school.is_archived:
        raise SCHOOL_ALREADY_ARCHIVED_EXCEPTION
    
    db_school.is_archived = True
    db.commit()
    db.refresh(db_school)

    if as_pymodel:
        return SchoolOut.model_validate(db_school)
    
    return db_school

def restore_school_by_id(
    db: Session,
    id: int,
    user: Account,
    *,
    as_pymodel: bool=False
) -> School | SchoolOut:
    if not user.can_manage_schools:
        raise UNAUTHORIZED_ACCESS_EXCEPTION
    
    # get school or block request if school is not found
    db_school = get_school_by_id(db=db, id=id, allow_none=False)
    
    if not db_school.is_archived:
        raise SCHOOL_ALREADY_RESTORED_EXCEPTION
    
    db_school.is_archived = False
    db.commit()
    db.refresh(db_school)

    if as_pymodel:
        return SchoolOut.model_validate(db_school)
    
    return db_school

