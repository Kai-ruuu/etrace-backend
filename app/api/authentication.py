from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query, UploadFile, Form, File
from fastapi.security import OAuth2PasswordRequestForm

from app.models.account import Account
from app.core.enums import AccountRole
from app.core.dependencies import get_db
from app.schemas.authentication import Token
from app.schemas.account import CompanyAccountOut
from app.services.authentication import AuthenticationService
from app.core.dependencies import get_db, allow_roles
from app.services.account_provision import AccountProvisionService

router = APIRouter(tags=["all"], prefix="/api/v1/authentication")

@router.post("/login", response_model=Token, tags=["all: tested"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession=Depends(get_db)) -> Token:
    authentication_service = AuthenticationService(db)
    return await authentication_service.authenticate_user(form_data)

@router.post("/register/company", response_model=CompanyAccountOut, tags=["company: tested"])
async def register_as_company(
    email: str=Form(..., min_length=4, max_length=255),     # [MARK] Review
    password: str=Form(..., min_length=8, max_length=65),
    name: str=Form(..., min_length=1, max_length=255),
    address: str=Form(..., min_length=1, max_length=1025),
    logo_file: UploadFile | None=File(None),
    sec_file: UploadFile | None=File(None),
    profile_file: UploadFile | None=File(None),
    business_permit_file: UploadFile | None=File(None),
    list_of_vacancies_file: UploadFile | None=File(None),
    cert_from_dole_file: UploadFile | None=File(None),
    cert_of_no_pending_case_file: UploadFile | None=File(None),
    reg_dti_cda_file: UploadFile | None=File(None),
    reg_of_est_file: UploadFile | None=File(None),
    reg_philjobnet_file: UploadFile | None=File(None),
    db: AsyncSession = Depends(get_db)
) -> CompanyAccountOut:
    service = AccountProvisionService(db, AccountRole.COMPANY)
    return await service.create_company(
        email,
        password,
        name,
        address,
        logo_file,
        sec_file,
        profile_file,
        business_permit_file,
        list_of_vacancies_file,
        cert_from_dole_file,
        cert_of_no_pending_case_file,
        reg_dti_cda_file,
        reg_of_est_file,
        reg_philjobnet_file,
        True
    )


