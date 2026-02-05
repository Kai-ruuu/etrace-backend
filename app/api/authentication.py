from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Request, Response, Depends, UploadFile, Form, File

from app.models.account import Account
from app.utils.rate_limiting import limiter
from app.core.dependencies import get_current_user
from app.core.dependencies import get_db
from app.core.enums import AccountRole, AlumniEmploymentStatus
from app.schemas.account import (
    CompanyAccountOut,
    AlumniAccountOut
)
from app.schemas.authentication import (
    Token,
    LoginCredentials
)
from app.services.authentication import AuthenticationService
from app.services.account_provision import AccountProvisionService


router = APIRouter(tags=["all"], prefix="/api/v1/authentication")


@router.post("/login")
@limiter.limit("10/minute")
async def login(
    request: Request,
    response: Response,
    form_data: LoginCredentials,
    db: AsyncSession=Depends(get_db),
):
    authentication_service = AuthenticationService(db)
    return await authentication_service.login(response, form_data)


@router.post("/logout")
@limiter.limit("10/minute")
async def logout(
    request: Request,
    response: Response,
    db: AsyncSession=Depends(get_db),
    user: Account = Depends(get_current_user)
):
    authentication_service = AuthenticationService(db)
    return authentication_service.logout(response)


@router.get("/me")
@limiter.limit("10/minute")
async def me(
    request: Request,
    db: AsyncSession=Depends(get_db),
    user: Account = Depends(get_current_user)
):
    authentication_service = AuthenticationService(db)
    return authentication_service.current_user_to_pymodel(user)


@router.post("/register/company", response_model=CompanyAccountOut)
@limiter.limit("10/minute")
async def register_as_company(
    request: Request,
    email: str=Form(..., min_length=4, max_length=255),     # [mark] review
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


@router.post("/register/alumni", response_model=AlumniAccountOut)
@limiter.limit("10/minute")
async def register_as_alumni(
    request: Request,
    email: str=Form(..., min_length=4, max_length=255),     # [mark] review
    password: str=Form(..., min_length=8, max_length=65),
    name_extension: str | None = Form(None),
    first_name: str = Form(..., min_length=1, max_length=100),
    middle_name: str | None = Form(None),
    last_name: str = Form(..., min_length=1, max_length=100),
    address: str = Form(..., min_length=1, max_length=515),
    phone_number: str = Form(..., min_length=8, max_length=15),
    course_id: int = Form(...),
    year_graduated: int = Form(..., ge=1000),
    employment_status: AlumniEmploymentStatus = Form(AlumniEmploymentStatus.UNEMPLOYED),
    occupations: str = Form(...),
    socials: str = Form(...),
    profile_picture_file: UploadFile | None = File(None),
    curriculum_vitae_file: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db)
) -> AlumniAccountOut:
    service = AccountProvisionService(db, AccountRole.ALUMNI)
    return await service.create_alumni(
        email,
        password,
        name_extension,
        first_name,
        middle_name,
        last_name,
        address,
        phone_number,
        course_id,
        year_graduated,
        employment_status,
        occupations,
        socials,
        profile_picture_file,
        curriculum_vitae_file,
        True
    )


