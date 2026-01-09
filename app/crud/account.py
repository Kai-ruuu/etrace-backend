from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, func, cast, String
from sqlalchemy.orm import Session, joinedload, selectinload

from app.exceptions import *
from app.schemas.account import *
from app.enums.all import AccountRole
from app.models.all import *
from app.models.account import DEFAULT_SYSAD_EMAIL
from app.crud.school import get_school_by_id, get_schools
from app.utils.model import paginate, to_pymodels
from app.utils.password import hash_password, generate_password
from app.utils.storage import Upload, UploadManager, DestFolder

def get_account_by_id(
    db: Session,
    id: int,
    *,
    role: AccountRole | None=None,
    allow_none: bool=False,
    as_pymodel: bool=False
) -> Account | SystemAdminAccountOut:
    query = db.query(Account).options(joinedload(Account.system_admin_profile)).filter(Account.id == id)

    if role:
        query = query.filter(Account.role == role)
    
    account = query.first()

    if not account:
        if allow_none:
            return None
        raise ACCOUNT_NOT_FOUND_EXCEPTION
    
    if as_pymodel:
        return SystemAdminAccountOut.model_validate(account)
    
    return account

def get_account_by_email(
    db: Session,
    email: str,
    *,
    role: AccountRole | None=None,
    allow_none: bool=False,
    as_pymodel: bool=False
) -> Account | SystemAdminAccountOut:
    query = db.query(Account).options(joinedload(Account.system_admin_profile)).filter(Account.email == email)

    if role:
        query = query.filter(Account.role == role)
    
    account = query.first()

    if not account:
        if allow_none:
            return None
        raise ACCOUNT_NOT_FOUND_EXCEPTION
    
    if as_pymodel:
        return SystemAdminAccountOut.model_validate(account)
    
    return account

def get_system_admin_accounts(
    db: Session,
    user: Account,
    *,
    is_disabled: bool | None=None,
    search: str | None=None,
    page: int=1,
    size: int=20,
    as_pymodels: bool=False
) -> list[Account] | dict:
    if not user.can_read_system_admins:
        raise UNAUTHORIZED_ACCESS_EXCEPTION

    query = (
        db.query(Account)
        .options(selectinload(Account.system_admin_profile))
        .filter(
            Account.role == AccountRole.SYSTEM_ADMINISTRATOR,
            Account.email != DEFAULT_SYSAD_EMAIL
        )
    )

    if is_disabled is not None:
        query = query.filter(Account.is_disabled == is_disabled)
    
    if search:
        query = (
            query.distinct(Account.id)
            .join(SystemAdminProfile, SystemAdminProfile.account_id == Account.id)
            .filter(or_(
                Account.email.ilike(f"%{search}%"),
                SystemAdminProfile.first_name.ilike(f"%{search}%"),
                func.coalesce(SystemAdminProfile.middle_name, "").ilike(f"%{search}%"),
                SystemAdminProfile.last_name.ilike(f"%{search}%"),
            ))
        )
    
    total, accounts = paginate(query, page=page, size=size, distinct_col=Account.id)
    
    if as_pymodels:
        return {
            "page": page,
            "size": size,
            "total": total,
            "items": to_pymodels(accounts, SystemAdminAccountOut)
        }
        
    return accounts

def get_dean_accounts(
    db: Session,
    user: Account,
    *,
    is_disabled: bool | None=None,
    search: str | None=None,
    page: int=1,
    size: int=20,
    as_pymodels: bool=False
) -> list[Account] | dict:
    if not user.can_read_deans:
        raise UNAUTHORIZED_ACCESS_EXCEPTION

    query = (
        db.query(Account)
        .options(selectinload(Account.dean_profile))
        .filter(Account.role == AccountRole.DEAN)
    )

    if is_disabled is not None:
        query = query.filter(Account.is_disabled == is_disabled)
    
    if search:
        query = (
            query.distinct(Account.id)
            .join(DeanProfile, DeanProfile.account_id == Account.id)
            .join(School, School.id == DeanProfile.school_id)
            .filter(or_(
                Account.email.ilike(f"%{search}%"),
                School.name.ilike(f"%{search}%"),
                DeanProfile.first_name.ilike(f"%{search}%"),
                func.coalesce(DeanProfile.middle_name, "").ilike(f"%{search}%"),
                DeanProfile.last_name.ilike(f"%{search}%"),
            ))
        )
    
    total, accounts = paginate(query, page=page, size=size, distinct_col=Account.id)
    
    if as_pymodels:
        return {
            "page": page,
            "size": size,
            "total": total,
            "items": to_pymodels(accounts, DeanAccountOut)
        }

    return accounts

def get_peso_staff_accounts(
    db: Session,
    user: Account,
    *,
    is_disabled: bool | None=None,
    search: str | None=None,
    page: int=1,
    size: int=20,
    as_pymodels: bool=False
) -> list[Account] | dict:
    if not user.can_read_peso_staffs:
        raise UNAUTHORIZED_ACCESS_EXCEPTION

    query = (
        db.query(Account)
        .options(selectinload(Account.peso_staff_profile))
        .filter(Account.role == AccountRole.PESO_STAFF)
    )
    
    if is_disabled is not None:
        query = query.filter(Account.is_disabled == is_disabled)
    
    if search:
        query = (
            query.distinct(Account.id)
            .join(PesoStaffProfile, PesoStaffProfile.account_id == Account.id)
            .filter(or_(
                Account.email.ilike(f"%{search}%"),
                PesoStaffProfile.first_name.ilike(f"%{search}%"),
                func.coalesce(PesoStaffProfile.middle_name, "").ilike(f"%{search}%"),
                PesoStaffProfile.last_name.ilike(f"%{search}%"),
            ))
        )
    
    total, accounts = paginate(query, page=page, size=size, distinct_col=Account.id)
    
    if as_pymodels:
        return {
            "page": page,
            "size": size,
            "total": total,
            "items": to_pymodels(accounts, PesoStaffAccountOut)
        }
        
    return accounts

def get_company_accounts(
    db: Session,
    user: Account,
    *,
    is_disabled: bool | None=None,
    search: str | None=None,
    page: int=1,
    size: int=20,
    as_pymodels: bool=False
) -> list[Account] | dict:
    if not user.can_read_companies:
        raise UNAUTHORIZED_ACCESS_EXCEPTION

    query = (
        db.query(Account)
        .options(selectinload(Account.company_profile))
        .filter(Account.role == AccountRole.COMPANY)
    )
    
    if is_disabled is not None:
        query = query.filter(Account.is_disabled == is_disabled)
    
    if search:
        query = (
            query.distinct(Account.id)
            .join(CompanyProfile, CompanyProfile.account_id == Account.id)
            .filter(or_(
                CompanyProfile.name.ilike(f"%{search}%"),
                cast(CompanyProfile.sysad_approval_status, String).ilike(f"%{search}%"),
                cast(CompanyProfile.peso_staff_approval_status, String).ilike(f"%{search}%"),
                Account.email.ilike(f"%{search}%"),
            ))
        )
    
    total, accounts = paginate(query, page=page, size=size, distinct_col=Account.id)
    
    if as_pymodels:
        return {
            "page": page,
            "size": size,
            "total": total,
            "items": to_pymodels(accounts, CompanyAccountOut)
        }

    return accounts

def get_alumni_accounts(
    db: Session,
    user: Account,
    *,
    search: str | None=None,
    is_disabled: bool | None=None,
    page: int=1,
    size: int=20,
    as_pymodels: bool=False
) -> list[Account] | dict:
    if not user.can_read_alumni:
        raise UNAUTHORIZED_ACCESS_EXCEPTION

    query = (
        db.query(Account)
        .options(selectinload(Account.alumni_profile))
        .filter(Account.role == AccountRole.ALUMNI)
    )

    if is_disabled is not None:
        query = query.filter(Account.is_disabled == is_disabled)
    
    if search:
        query = (
            query.distinct(Account.id)
            .join(AlumniProfile, AlumniProfile.account_id == Account.id)
            .join(Course, Course.id == AlumniProfile.course_id)
            .filter(or_(
                Course.name.ilike(f"%{search}%"),
                Account.email.ilike(f"%{search}%"),
                AlumniProfile.first_name.ilike(f"%{search}%"),
                func.coalesce(AlumniProfile.middle_name, "").ilike(f"%{search}%"),
                AlumniProfile.last_name.ilike(f"%{search}%"),
                AlumniProfile.address.ilike(f"%{search}%"),
                AlumniProfile.phone_number.ilike(f"%{search}%"),
                cast(AlumniProfile.year_graduated, String).ilike(f"%{search}%"),
                cast(AlumniProfile.employment_status, String).ilike(f"%{search}%"),
                cast(AlumniProfile.dean_approval_status, String).ilike(f"%{search}%"),
            ))
        )
    
    total, accounts = paginate(query, page=page, size=size, distinct_col=Account.id)
    
    if as_pymodels:
        return {
            "page": page,
            "size": size,
            "total": total,
            "items": to_pymodels(accounts, AlumniAccountOut)
        }
    
    return accounts

def disable_system_admin_account_by_id(
    db: Session,
    id: int,
    user: Account,
    *,
    as_pymodel: bool=False
) -> Account | SystemAdminAccountOut:
    if not user.can_enable_or_disable_system_admins:
        raise UNAUTHORIZED_ACCESS_EXCEPTION
    
    # get account or block request if account is not found
    db_account = get_account_by_id(db=db, id=id, role=AccountRole.SYSTEM_ADMINISTRATOR, allow_none=False)

    # block request if the target account is the default system admin's account
    if db_account.is_default_system_admin:
        raise UNAUTHORIZED_ACCESS_EXCEPTION

    if db_account.is_disabled:
        raise ACCOUNT_ALREADY_DISABLED_EXCEPTION
    
    db_account.is_disabled = True
    db.commit()
    db.refresh(db_account, attribute_names=["system_admin_profile"])

    if as_pymodel:
        return SystemAdminAccountOut.model_validate(db_account)
    
    return db_account

def disable_dean_account_by_id(
    db: Session,
    id: int,
    user: Account,
    *,
    as_pymodel: bool=False
) -> Account | DeanAccountOut:
    if not user.can_enable_or_disable_deans:
        raise UNAUTHORIZED_ACCESS_EXCEPTION
    
    # get account or block request if account is not found
    db_account = get_account_by_id(db=db, id=id, role=AccountRole.DEAN, allow_none=False)

    # block request if the target account is the default system admin's account
    if db_account.is_default_system_admin:
        raise UNAUTHORIZED_ACCESS_EXCEPTION

    if db_account.is_disabled:
        raise ACCOUNT_ALREADY_DISABLED_EXCEPTION
    
    db_account.is_disabled = True
    db.commit()
    db.refresh(db_account, attribute_names=["dean_profile"])

    if as_pymodel:
        return DeanAccountOut.model_validate(db_account)
    
    return db_account

def disable_peso_staff_account_by_id(
    db: Session,
    id: int,
    user: Account,
    *,
    as_pymodel: bool=False
) -> Account | PesoStaffAccountOut:
    if not user.can_enable_or_disable_peso_staffs:
        raise UNAUTHORIZED_ACCESS_EXCEPTION
    
    # get account or block request if account is not found
    db_account = get_account_by_id(db=db, id=id, role=AccountRole.PESO_STAFF, allow_none=False)

    # block request if the target account is the default system admin's account
    if db_account.is_default_system_admin:
        raise UNAUTHORIZED_ACCESS_EXCEPTION

    if db_account.is_disabled:
        raise ACCOUNT_ALREADY_DISABLED_EXCEPTION
    
    db_account.is_disabled = True
    db.commit()
    db.refresh(db_account, attribute_names=["peso_staff_profile"])

    if as_pymodel:
        return PesoStaffAccountOut.model_validate(db_account)
    
    return db_account

def disable_company_account_by_id(
    db: Session,
    id: int,
    user: Account,
    *,
    as_pymodel: bool=False
) -> Account | CompanyAccountOut:
    if not user.can_enable_or_disable_companies:
        raise UNAUTHORIZED_ACCESS_EXCEPTION
    
    # get account or block request if account is not found
    db_account = get_account_by_id(db=db, id=id, role=AccountRole.COMPANY, allow_none=False)

    # block request if the target account is the default system admin's account
    if db_account.is_default_system_admin:
        raise UNAUTHORIZED_ACCESS_EXCEPTION

    if db_account.is_disabled:
        raise ACCOUNT_ALREADY_DISABLED_EXCEPTION
    
    db_account.is_disabled = True
    db.commit()
    db.refresh(db_account, attribute_names=["company_profile"])

    if as_pymodel:
        return CompanyAccountOut.model_validate(db_account)
    
    return db_account

def disable_alumni_account_by_id(
    db: Session,
    id: int,
    user: Account,
    *,
    as_pymodel: bool=False
) -> Account | AlumniAccountOut:
    if not user.can_enable_or_disable_alumni:
        raise UNAUTHORIZED_ACCESS_EXCEPTION
    
    # get account or block request if account is not found
    db_account = get_account_by_id(db=db, id=id, role=AccountRole.ALUMNI, allow_none=False)

    # block request if the target account is the default system admin's account
    if db_account.is_default_system_admin:
        raise UNAUTHORIZED_ACCESS_EXCEPTION

    if db_account.is_disabled:
        raise ACCOUNT_ALREADY_DISABLED_EXCEPTION
    
    db_account.is_disabled = True
    db.commit()
    db.refresh(db_account, attribute_names=["alumni_profile"])

    if as_pymodel:
        return AlumniAccountOut.model_validate(db_account)
    
    return db_account

def enable_system_admin_account_by_id(
    db: Session,
    id: int,
    user: Account,
    *,
    as_pymodel: bool=False
) -> Account | SystemAdminAccountOut:
    if not user.can_enable_or_disable_system_admins:
        raise UNAUTHORIZED_ACCESS_EXCEPTION
    
    # get account or block request if account is not found
    db_account = get_account_by_id(db=db, id=id, role=AccountRole.SYSTEM_ADMINISTRATOR, allow_none=False)

    # block request if the target account is the default system admin's account
    if db_account.is_default_system_admin:
        raise UNAUTHORIZED_ACCESS_EXCEPTION

    if not db_account.is_disabled:
        raise ACCOUNT_ALREADY_ENABLED_EXCEPTION
    
    db_account.is_disabled = False
    db.commit()
    db.refresh(db_account, attribute_names=["system_admin_profile"])

    if as_pymodel:
        return SystemAdminAccountOut.model_validate(db_account)
    
    return db_account

def enable_dean_account_by_id(
    db: Session,
    id: int,
    user: Account,
    *,
    as_pymodel: bool=False
) -> Account | DeanAccountOut:
    if not user.can_enable_or_disable_deans:
        raise UNAUTHORIZED_ACCESS_EXCEPTION
    
    # get account or block request if account is not found
    db_account = get_account_by_id(db=db, id=id, role=AccountRole.DEAN, allow_none=False)

    # block request if the target account is the default system admin's account
    if db_account.is_default_system_admin:
        raise UNAUTHORIZED_ACCESS_EXCEPTION

    if not db_account.is_disabled:
        raise ACCOUNT_ALREADY_ENABLED_EXCEPTION
    
    db_account.is_disabled = False
    db.commit()
    db.refresh(db_account, attribute_names=["dean_profile"])

    if as_pymodel:
        return DeanAccountOut.model_validate(db_account)
    
    return db_account

def enable_peso_staff_account_by_id(
    db: Session,
    id: int,
    user: Account,
    *,
    as_pymodel: bool=False
) -> Account | PesoStaffAccountOut:
    if not user.can_enable_or_disable_peso_staffs:
        raise UNAUTHORIZED_ACCESS_EXCEPTION
    
    # get account or block request if account is not found
    db_account = get_account_by_id(db=db, id=id, role=AccountRole.PESO_STAFF, allow_none=False)

    # block request if the target account is the default system admin's account
    if db_account.is_default_system_admin:
        raise UNAUTHORIZED_ACCESS_EXCEPTION

    if not db_account.is_disabled:
        raise ACCOUNT_ALREADY_ENABLED_EXCEPTION
    
    db_account.is_disabled = False
    db.commit()
    db.refresh(db_account, attribute_names=["peso_staff_profile"])

    if as_pymodel:
        return PesoStaffAccountOut.model_validate(db_account)
    
    return db_account

def enable_company_account_by_id(
    db: Session,
    id: int,
    user: Account,
    *,
    as_pymodel: bool=False
) -> Account | CompanyAccountOut:
    if not user.can_enable_or_disable_companies:
        raise UNAUTHORIZED_ACCESS_EXCEPTION
    
    # get account or block request if account is not found
    db_account = get_account_by_id(db=db, id=id, role=AccountRole.COMPANY, allow_none=False)

    # block request if the target account is the default system admin's account
    if db_account.is_default_system_admin:
        raise UNAUTHORIZED_ACCESS_EXCEPTION

    if not db_account.is_disabled:
        raise ACCOUNT_ALREADY_ENABLED_EXCEPTION
    
    db_account.is_disabled = False
    db.commit()
    db.refresh(db_account, attribute_names=["company_profile"])

    if as_pymodel:
        return CompanyAccountOut.model_validate(db_account)
    
    return db_account

def enable_alumni_account_by_id(
    db: Session,
    id: int,
    user: Account,
    *,
    as_pymodel: bool=False
) -> Account | AlumniAccountOut:
    if not user.can_enable_or_disable_alumni:
        raise UNAUTHORIZED_ACCESS_EXCEPTION
    
    # get account or block request if account is not found
    db_account = get_account_by_id(db=db, id=id, role=AccountRole.ALUMNI, allow_none=False)

    # block request if the target account is the default system admin's account
    if db_account.is_default_system_admin:
        raise UNAUTHORIZED_ACCESS_EXCEPTION

    if not db_account.is_disabled:
        raise ACCOUNT_ALREADY_ENABLED_EXCEPTION
    
    db_account.is_disabled = False
    db.commit()
    db.refresh(db_account, attribute_names=["alumni_profile"])

    if as_pymodel:
        return AlumniAccountOut.model_validate(db_account)
    
    return db_account

def create_system_admin_account(
    db: Session,
    payload: SystemAdminAccountIn,
    user: Account,
    *,
    as_pymodel: bool=False
) -> Account | SystemAdminAccountOut:
    if not user.can_create_system_admins:
        raise UNAUTHORIZED_ACCESS_EXCEPTION
    
    db_account = get_account_by_email(db, email=payload.email, allow_none=True)

    if db_account:
        raise ACCOUNT_ALREADY_EXISTS_EXCEPTION

    new_account_password = generate_password()
    print(f"[DEBUG] New System Admin Password: {new_account_password}")
    
    try:
        new_account = Account(
            role=AccountRole.SYSTEM_ADMINISTRATOR,
            email=payload.email,
            password=hash_password(new_account_password)
        )
        db.add(new_account)
        db.flush()

        new_profile = SystemAdminProfile(
            account_id=new_account.id,
            first_name=payload.first_name,
            middle_name=payload.middle_name,
            last_name=payload.last_name,
        )
        db.add(new_profile)
        db.commit()
        db.refresh(new_account, attribute_names=["system_admin_profile"])
        db.refresh(new_profile)

        if as_pymodel:
            return SystemAdminAccountOut.model_validate(new_account)
        
        return new_account
    finally:
        db.close()

def create_dean_account(
    db: Session,
    payload: DeanAccountIn,
    user: Account,
    *,
    as_pymodel: bool=False
) -> Account | DeanAccountOut:
    if not user.can_create_deans:
        raise UNAUTHORIZED_ACCESS_EXCEPTION
    
    if len(get_schools(db=db, user=user)) == 0:
        raise SCHOOLS_CURRENTLY_EMPTY_EXCEPTION
    
    # block request if school is not found
    get_school_by_id(db=db, id=payload.school_id, allow_none=False)

    new_account_password = generate_password()
    print(f"[DEBUG] New Dean Password: {new_account_password}")

    try:
        new_account = Account(
            role=AccountRole.DEAN,
            email=payload.email,
            password=hash_password(new_account_password)
        )
        db.add(new_account)
        db.flush()

        new_profile = DeanProfile(
            account_id=new_account.id,
            school_id=payload.school_id,
            first_name=payload.first_name,
            middle_name=payload.middle_name,
            last_name=payload.last_name,
        )
        db.add(new_profile)
        db.commit()
        db.refresh(new_account, attribute_names=["dean_profile"])
        db.refresh(new_profile)

        if as_pymodel:
            return DeanAccountOut.model_validate(new_account)
        
        return new_account
    finally:
        db.close()
    
def create_peso_staff_account(
    db: Session,
    payload: PesoStaffAccountIn,
    user: Account,
    *,
    as_pymodel: bool=False
) -> Account | PesoStaffAccountOut:
    if not user.can_create_peso_staffs:
        raise UNAUTHORIZED_ACCESS_EXCEPTION
    
    db_account = get_account_by_email(db, email=payload.email, allow_none=True)

    if db_account:
        raise ACCOUNT_ALREADY_EXISTS_EXCEPTION

    new_account_password = generate_password()
    print(f"[DEBUG] New PESO Staff Password: {new_account_password}")

    try:
        new_account = Account(
            role=AccountRole.PESO_STAFF,
            email=payload.email,
            password=hash_password(new_account_password)
        )
        db.add(new_account)
        db.flush()

        new_profile = PesoStaffProfile(
            account_id=new_account.id,
            first_name=payload.first_name,
            middle_name=payload.middle_name,
            last_name=payload.last_name,
        )
        db.add(new_profile)
        db.commit()
        db.refresh(new_account, attribute_names=["peso_staff_profile"])
        db.refresh(new_profile)

        return PesoStaffAccountOut.model_validate(new_account) if as_pymodel else new_account
    finally:
        db.close()

def create_company_account(
    db: Session,
    email: str, 
    password: str,
    name: str,
    logo_file: UploadFile | None=None,
    sec_file: UploadFile | None=None,
    profile_file: UploadFile | None=None,
    business_permit_file: UploadFile | None=None,
    list_of_vacancies_file: UploadFile | None=None,
    cert_from_dole_file: UploadFile | None=None,
    cert_of_no_pending_case_file: UploadFile | None=None,
    reg_dti_cda_file: UploadFile | None=None,
    reg_of_est_file: UploadFile | None=None,
    reg_philjobnet_file: UploadFile | None=None,
    *,
    as_pymodel: bool=False
) -> CompanyAccountOut:
    upload_manager = UploadManager()
    upload_manager.stage_uploads([
        Upload(file=logo_file, dest_folder=DestFolder.LOGO, allowed_mimes={"image/png", "image/jpg", "image/jpeg"}),
        Upload(file=sec_file, dest_folder=DestFolder.SEC, allowed_mimes={"application/pdf"}),
        Upload(file=profile_file, dest_folder=DestFolder.PROFILE, allowed_mimes={"application/pdf"}),
        Upload(file=business_permit_file, dest_folder=DestFolder.BUSINESS_PERMIT, allowed_mimes={"application/pdf"}),
        Upload(file=list_of_vacancies_file, dest_folder=DestFolder.LIST_OF_VACANCIES, allowed_mimes={"application/pdf"}),
        Upload(file=cert_from_dole_file, dest_folder=DestFolder.CERT_FROM_DOLE, allowed_mimes={"application/pdf"}),
        Upload(file=cert_of_no_pending_case_file, dest_folder=DestFolder.CERT_OF_NO_PENDING_CASE, allowed_mimes={"application/pdf"}),
        Upload(file=reg_dti_cda_file, dest_folder=DestFolder.REG_DTI_CDA, allowed_mimes={"application/pdf"}),
        Upload(file=reg_of_est_file, dest_folder=DestFolder.REG_OF_EST, allowed_mimes={"application/pdf"}),
        Upload(file=reg_philjobnet_file, dest_folder=DestFolder.REG_PHILJOBNET, allowed_mimes={"application/pdf"}),
    ])
    
    try:
        with db.begin():
            new_account = Account(
                role=AccountRole.COMPANY,
                email=email,
                password=hash_password(password)
            )
            db.add(new_account)
            db.flush()
            
            new_profile = CompanyProfile(
                account_id=new_account.id,
                name=name,
                logo_filename=upload_manager.get_staged_file_name(DestFolder.LOGO),
                sec_filename=upload_manager.get_staged_file_name(DestFolder.SEC),
                profile_filename=upload_manager.get_staged_file_name(DestFolder.PROFILE),
                business_permit_filename=upload_manager.get_staged_file_name(DestFolder.BUSINESS_PERMIT),
                list_of_vacancies_filename=upload_manager.get_staged_file_name(DestFolder.LIST_OF_VACANCIES),
                cert_from_dole_filename=upload_manager.get_staged_file_name(DestFolder.CERT_FROM_DOLE),
                cert_of_no_pending_case_filename=upload_manager.get_staged_file_name(DestFolder.CERT_OF_NO_PENDING_CASE),
                reg_dti_cda_filename=upload_manager.get_staged_file_name(DestFolder.REG_DTI_CDA),
                reg_of_est_filename=upload_manager.get_staged_file_name(DestFolder.REG_OF_EST),
                reg_philjobnet_filename=upload_manager.get_staged_file_name(DestFolder.REG_PHILJOBNET),
            )
            db.add(new_profile)

        db.refresh(new_account, attribute_names=["company_profile"])
        upload_manager.commit()

        return CompanyAccountOut.model_validate(new_account) if as_pymodel else new_account
    except IntegrityError as e:
        print(f"[DEBUG] Unable to create company's account - {e}")
        upload_manager.rollback()
        raise ACCOUNT_ALREADY_EXISTS_EXCEPTION
    except HTTPException:
        upload_manager.rollback()
        raise
    except Exception as e:
        upload_manager.rollback()
        print(f"[DEBUG] Unable to create company's account - {e}")
        raise ACCOUNT_UNABLE_TO_CREATE_EXCEPTION

