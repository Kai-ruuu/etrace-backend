from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query, Request

from app.utils.api import limiter
from app.models.all import Account
from app.enums.all import AccountRole
from app.database import get_db
from app.utils.authorization import allow_roles
from app.crud.school import (
    get_schools,
    create_school as svc_create_school,
    update_school_by_id,
    archive_school_by_id,
    restore_school_by_id
)
from app.crud.account import (
    get_system_admin_accounts,
    get_dean_accounts,
    get_peso_staff_accounts,
    get_company_accounts,
    get_alumni_accounts,
    create_system_admin_account,
    create_dean_account,
    create_peso_staff_account,
    disable_system_admin_account_by_id,
    disable_dean_account_by_id,
    disable_peso_staff_account_by_id,
    disable_company_account_by_id,
    disable_alumni_account_by_id,
    enable_system_admin_account_by_id,
    enable_dean_account_by_id,
    enable_peso_staff_account_by_id,
    enable_company_account_by_id,
    enable_alumni_account_by_id
)
from app.schemas.account import *
from app.schemas.school import SchoolIn, SchoolOut, SchoolUpdate

router = APIRouter(tags=["System Administrator"], prefix="/api/system-admin")



# SYSTEM ADMIN
@router.get("/", tags=["Tested"])
@limiter.limit("10/minute")
def get_all_system_admins(
    request: Request,
    db: Session=Depends(get_db),
    is_disabled: bool | None=Query(None),
    search: str | None=Query(None),
    page: int=Query(1, ge=1),
    size: int=Query(20, ge=20, le=100),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> dict:
    return get_system_admin_accounts(db=db, user=user, is_disabled=is_disabled, search=search, page=page, size=size, as_pymodels=True)

@router.post("/", tags=["Tested"])
@limiter.limit("10/minute")
def create_system_admin(
    request: Request,
    payload: SystemAdminAccountIn,
    db: Session=Depends(get_db),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> SystemAdminAccountOut:
    return create_system_admin_account(db=db, payload=payload, user=user, as_pymodel=True)

@router.patch("/{id}/disable", tags=["Tested"])
@limiter.limit("10/minute")
def disable_system_admin(
    request: Request,
    id: int,
    db: Session=Depends(get_db),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> SystemAdminAccountOut:
    return disable_system_admin_account_by_id(db=db, id=id, user=user, as_pymodel=True)

@router.patch("/{id}/enable", tags=["Tested"])
@limiter.limit("10/minute")
def enable_system_admin(
    request: Request,
    id: int,
    db: Session=Depends(get_db),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> SystemAdminAccountOut:
    return enable_system_admin_account_by_id(db=db, id=id, user=user, as_pymodel=True)



# DEAN
@router.get("/dean", tags=["Tested"])
@limiter.limit("10/minute")
def get_all_deans(
    request: Request,
    db: Session=Depends(get_db),
    is_disabled: bool | None=Query(None),
    search: str | None=Query(None),
    page: int=Query(1, ge=1),
    size: int=Query(20, ge=20, le=100),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> dict:
    return get_dean_accounts(db=db, user=user, is_disabled=is_disabled, search=search, page=page, size=size, as_pymodels=True)

@router.post("/dean", tags=["Tested"])
@limiter.limit("10/minute")
def create_dean(
    request: Request,
    payload: DeanAccountIn,
    db: Session=Depends(get_db),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> DeanAccountOut:
    return create_dean_account(db=db, payload=payload, user=user, as_pymodel=True)

@router.patch("/dean/{id}/disable", tags=["Tested"])
@limiter.limit("10/minute")
def disable_dean(
    request: Request,
    id: int,
    db: Session=Depends(get_db),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> DeanAccountOut:
    return disable_dean_account_by_id(db=db, id=id, user=user, as_pymodel=True)

@router.patch("/dean/{id}/enable", tags=["Tested"])
@limiter.limit("10/minute")
def enable_dean(
    request: Request,
    id: int,
    db: Session=Depends(get_db),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> DeanAccountOut:
    return enable_dean_account_by_id(db=db, id=id, user=user, as_pymodel=True)
    


# PESO Staff
@router.get("/peso-staff", tags=["Tested"])
@limiter.limit("10/minute")
def get_all_peso_staffs(
    request: Request,
    db: Session=Depends(get_db),
    is_disabled: bool | None=Query(None),
    search: str | None=Query(None),
    page: int=Query(1, ge=1),
    size: int=Query(20, ge=20, le=100),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> dict:
    return get_peso_staff_accounts(db=db, user=user, is_disabled=is_disabled, search=search, page=page, size=size, as_pymodels=True)

@router.post("/peso-staff", tags=["Tested"])
@limiter.limit("10/minute")
def create_peso_staff(
    request: Request,
    payload: PesoStaffAccountIn,
    db: Session=Depends(get_db),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> PesoStaffAccountOut:
    return create_peso_staff_account(db=db, payload=payload, user=user, as_pymodel=True)

@router.patch("/peso-staff/{id}/disable", tags=["Tested"])
@limiter.limit("10/minute")
def disable_dean(
    request: Request,
    id: int,
    db: Session=Depends(get_db),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> PesoStaffAccountOut:
    return disable_peso_staff_account_by_id(db=db, id=id, user=user, as_pymodel=True)

@router.patch("/peso-staff/{id}/enable", tags=["Tested"])
@limiter.limit("10/minute")
def enable_dean(
    request: Request,
    id: int,
    db: Session=Depends(get_db),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> PesoStaffAccountOut:
    return enable_peso_staff_account_by_id(db=db, id=id, user=user, as_pymodel=True)
    


# Company
@router.get("/company", tags=["Tested"])
@limiter.limit("10/minute")
def get_all_companies(
    request: Request,
    db: Session=Depends(get_db),
    is_disabled: bool | None=Query(None),
    search: str | None=Query(None),
    page: int=Query(1, ge=1),
    size: int=Query(20, ge=20, le=100),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> dict:
    return get_company_accounts(db=db, user=user, is_disabled=is_disabled, search=search, page=page, size=size, as_pymodels=True)

@router.patch("/company/{id}/disable", tags=["Tested"])
@limiter.limit("10/minute")
def disable_company(
    request: Request,
    id: int,
    db: Session=Depends(get_db),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> CompanyAccountOut:
    return disable_company_account_by_id(db=db, id=id, user=user, as_pymodel=True)

@router.patch("/company/{id}/enable", tags=["Tested"])
@limiter.limit("10/minute")
def enable_company(
    request: Request,
    id: int,
    db: Session=Depends(get_db),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> CompanyAccountOut:
    return enable_company_account_by_id(db=db, id=id, user=user, as_pymodel=True)



# Alumni
@router.get("/alumni")
@limiter.limit("10/minute")
def get_all_alumni(
    request: Request,
    db: Session=Depends(get_db),
    is_disabled: bool | None=Query(None),
    search: str | None=Query(None),
    page: int=Query(1, ge=1),
    size: int=Query(20, ge=20, le=100),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> dict:
    return get_alumni_accounts(db=db, user=user, is_disabled=is_disabled, search=search, page=page, size=size, as_pymodels=True)

@router.patch("/alumni/{id}/disable")
@limiter.limit("10/minute")
def disable_alumni(
    request: Request,
    id: int,
    db: Session=Depends(get_db),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> AlumniAccountOut:
    return disable_alumni_account_by_id(db=db, id=id, user=user, as_pymodel=True)

@router.patch("/alumni/{id}/enable")
@limiter.limit("10/minute")
def enable_alumni(
    request: Request,
    id: int,
    db: Session=Depends(get_db),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> AlumniAccountOut:
    return enable_alumni_account_by_id(db=db, id=id, user=user, as_pymodel=True)



# School
@router.get("/school", tags=["Tested"])
@limiter.limit("10/minute")
def get_all_schools(
    request: Request,
    db: Session=Depends(get_db),
    is_archived: bool | None=Query(None),
    search: str | None=Query(None),
    page: int=Query(1, ge=1),
    size: int=Query(20, ge=20, le=100),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> dict:
    return get_schools(db=db, user=user, is_archived=is_archived, search=search, page=page, size=size, as_pymodels=True)

@router.post("/school", tags=["Tested"])
@limiter.limit("10/minute")
def create_school(
    request: Request,
    payload: SchoolIn,
    db: Session=Depends(get_db),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> SchoolOut:
    return svc_create_school(db=db, payload=payload, user=user, as_pymodel=True)

@router.patch("/school/{id}", tags=["Tested"])
@limiter.limit("10/minute")
def update_school(
    request: Request,
    id: int,
    payload: SchoolUpdate,
    db: Session=Depends(get_db),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> SchoolOut:
    return update_school_by_id(db=db, id=id, payload=payload, user=user, as_pymodel=True)

@router.patch("/school/{id}/archive", tags=["Tested"])
@limiter.limit("10/minute")
def archive_school(
    request: Request,
    id: int,
    db: Session=Depends(get_db),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> SchoolOut:
    return archive_school_by_id(db=db, id=id, user=user, as_pymodel=True)

@router.patch("/school/{id}/restore", tags=["Tested"])
@limiter.limit("10/minute")
def restore_school(
    request: Request,
    id: int,
    db: Session=Depends(get_db),
    user: Account=Depends(allow_roles([AccountRole.SYSTEM_ADMINISTRATOR]))
) -> SchoolOut:
    return restore_school_by_id(db=db, id=id, user=user, as_pymodel=True)


