from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Request, Form, UploadFile, File

from app.database import get_db
from app.schemas.access_token import Token
from app.schemas.account import CompanyAccountOut
from app.crud.account import create_company_account
from app.utils.api import limiter
from app.utils.authentication import authenticate_user

router = APIRouter(tags=["All Roles"], prefix="/api/authentication")

@router.post("/login")
@limiter.limit("10/minute")
def login(
    request: Request,
    db: Session=Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    return authenticate_user(db=db, form_data=form_data)

@router.post("/company/signup", tags=["Tested"])
@limiter.limit("10/minute")
def signup_as_a_company(
    request: Request,
    db: Session=Depends(get_db),
    email: str=Form(...), 
    password: str=Form(...),
    name: str=Form(...),
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
) -> CompanyAccountOut:
    return create_company_account(
        db=db,
        email=email,
        password=password,
        name=name,
        logo_file=logo_file,
        sec_file=sec_file,
        profile_file=profile_file,
        business_permit_file=business_permit_file,
        list_of_vacancies_file=list_of_vacancies_file,
        cert_from_dole_file=cert_from_dole_file,
        cert_of_no_pending_case_file=cert_of_no_pending_case_file,
        reg_dti_cda_file=reg_dti_cda_file,
        reg_of_est_file=reg_of_est_file,
        reg_philjobnet_file=reg_philjobnet_file,
        as_pymodel=True
    )

