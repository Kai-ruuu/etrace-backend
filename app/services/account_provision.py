from fastapi import UploadFile, Form, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.account import *
from app.core.exceptions import *
from app.core.settings import settings
from app.core.enums import Action, AccountRole
from app.repositories.school import SchoolRepository
from app.repositories.account import AccountRepository
from app.repositories.profile import ProfileRepository
from app.utils.logging import Logger
from app.utils.storage import Upload, UploadManager, DestFolder
from app.utils.password import hash_password, generate_password
from app.models.account import Account
from app.models.dean_profile import DeanProfile
from app.models.company_profile import CompanyProfile
from app.models.peso_staff_profile import PesoStaffProfile
from app.models.system_admin_profile import SystemAdminProfile


class AccountProvisionService:
    def __init__(self, db: AsyncSession, role: AccountRole) -> None:
        self.db = db
        self.role = role
        self.account_repo = AccountRepository(self.db, self.role)
        self.profile_repo = ProfileRepository(self.db, self.role)
        
        match self.role:
            case AccountRole.DEAN:
                self.school_repo = SchoolRepository(self.db)
            case AccountRole.ALUMNI:
                self.upload_manager = UploadManager()
            case AccountRole.COMPANY:
                self.upload_manager = UploadManager()

    
    async def bootstap_default_system_admin(self) -> None:
        if self.role != AccountRole.SYSTEM_ADMIN:
            raise ValueError("Service role must be AccountRole.SYSTEM_ADMIN in order to bootstrap.")
        
        try:
            db_account = await self.account_repo.get_by_email(settings.APP_DEFAULT_SYSAD_EMAIL)
            
            if db_account:
                Logger.info("Default System Administrator's account and profile already exists.")
                return
            
            hashed_password = hash_password(settings.APP_DEFAULT_SYSAD_PASS)

            account = await self.account_repo.create(Account(
                email=settings.APP_DEFAULT_SYSAD_EMAIL,
                password=hashed_password,
                role=AccountRole.SYSTEM_ADMIN,
            ))
            
            await self.profile_repo.create(SystemAdminProfile(
                account_id=account.id,
                first_name=settings.APP_DEFAULT_SYSAD_FIRST_NAME,
                last_name=settings.APP_DEFAULT_SYSAD_LAST_NAME
            ))
            
            await self.db.commit()
            
            Logger.success("Default System Administrator's account and profile has been created.")
            
        except:
            await self.db.rollback()
            Logger.error("Unable to create Default System Administrator's account and profile.")
            raise
    
    
    async def create_system_admin(
        self,
        user: Account,
        system_admin: SystemAdminAccountIn,
        as_pymodel: bool = False
    ) -> tuple[Account, SystemAdminProfile] | SystemAdminAccountOut:
        if self.role != AccountRole.SYSTEM_ADMIN:
            raise ValueError("Service role must be AccountRole.SYSTEM_ADMIN in order to create a System Administrator.")
        
        user.permissions.raise_unauthorized_if_excludes(Action.CREATE_SYSTEM_ADMINS)
        
        try:
            db_account = await self.account_repo.get_by_email(system_admin.email)

            if db_account:
                raise ACCOUNT_ALREADY_EXISTS_EXCEPTION
            
            hashed_password = hash_password(generate_password())

            account = await self.account_repo.create(Account(
                email=system_admin.email,
                password=hashed_password,
                role=AccountRole.SYSTEM_ADMIN,
            ))
            
            profile = await self.profile_repo.create(SystemAdminProfile(
                account_id=account.id,
                first_name=system_admin.first_name,
                middle_name=system_admin.middle_name,
                last_name=system_admin.last_name
            ))
            
            await self.db.commit()

            account = await self.account_repo.get_by_email(system_admin.email)
            
            return SystemAdminAccountOut.model_validate(account) if as_pymodel else (account, profile)
        except HTTPException:
            raise
        except Exception as e:
            await self.db.rollback()
            Logger.error(f"Unable to create System Administrator's account and profile - {repr(e)}")
            raise UNABLE_TO_REGISTER_ACCOUNT_EXCEPTION
    
    
    async def create_peso_staff(
        self,
        user: Account,
        peso_staff: PesoStaffAccountIn,
        as_pymodel: bool = False
    ) -> tuple[Account, PesoStaffProfile] | PesoStaffAccountOut:
        if self.role != AccountRole.PESO_STAFF:
            raise ValueError("Service role must be AccountRole.PESO_STAFF in order to create a PESO Staff.")
        
        user.permissions.raise_unauthorized_if_excludes(Action.CREATE_PESO_STAFFS)
        
        try:
            db_account = await self.account_repo.get_by_email(peso_staff.email)

            if db_account:
                raise ACCOUNT_ALREADY_EXISTS_EXCEPTION
            
            hashed_password = hash_password(generate_password())

            account = await self.account_repo.create(Account(
                email=peso_staff.email,
                password=hashed_password,
                role=AccountRole.PESO_STAFF,
            ))
            
            profile = await self.profile_repo.create(PesoStaffProfile(
                account_id=account.id,
                first_name=peso_staff.first_name,
                middle_name=peso_staff.middle_name,
                last_name=peso_staff.last_name
            ))
            
            await self.db.commit()
            
            account = await self.account_repo.get_by_email(peso_staff.email)
            
            return PesoStaffAccountOut.model_validate(account) if as_pymodel else (account, profile)
        except HTTPException:
            raise
        except Exception as e:
            await self.db.rollback()
            Logger.error(f"Unable to create PESO Staff's account and profile - {repr(e)}")
            raise UNABLE_TO_REGISTER_ACCOUNT_EXCEPTION


    async def create_dean(
        self,
        user: Account,
        dean: DeanAccountIn,
        as_pymodel: bool = False
    ) -> tuple[Account, DeanProfile] | DeanAccountOut:
        if self.role != AccountRole.DEAN:
            raise ValueError("Service role must be AccountRole.DEAN in order to create a Dean.")
        
        user.permissions.raise_unauthorized_if_excludes(Action.CREATE_DEANS)
        
        try:
            db_schools = await self.school_repo.get_all()

            if len(db_schools) == 0:
                raise SCHOOLS_EMPTY_EXCEPTION
            
            db_school = await self.school_repo.get_by_id(dean.school_id)

            if not db_school:
                raise SCHOOL_NOT_FOUND_EXCEPTION
            
            db_account = await self.account_repo.get_by_email(dean.email)

            if db_account:
                raise ACCOUNT_ALREADY_EXISTS_EXCEPTION
            
            # [mark] refactor after the maling service has been implemented
            plain_password = generate_password()
            Logger.info(f"Dean creds:\nEmail: {dean.email}\nPassword: {plain_password}")
            
            hashed_password = hash_password(plain_password)

            account = await self.account_repo.create(Account(
                email=dean.email,
                password=hashed_password,
                role=AccountRole.DEAN,
            ))
            
            profile = await self.profile_repo.create(DeanProfile(
                account_id=account.id,
                school_id=dean.school_id,
                first_name=dean.first_name,
                middle_name=dean.middle_name,
                last_name=dean.last_name
            ))
            
            await self.db.commit()

            account = await self.account_repo.get_by_email(dean.email)
            
            return DeanAccountOut.model_validate(account) if as_pymodel else (account, profile)
        except HTTPException:
            raise
        except Exception as e:
            await self.db.rollback()
            Logger.error(f"Unable to create Dean's account and profile - {repr(e)}")
            raise UNABLE_TO_REGISTER_ACCOUNT_EXCEPTION


    async def create_company(
        self,
        email: str=Form(...), 
        password: str=Form(...),
        name: str=Form(...),
        address: str=Form(...),
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
        as_pymodel: bool = False
    ) -> tuple[Account, CompanyProfile] | CompanyAccountOut:
        if self.role != AccountRole.COMPANY:
            raise ValueError("Service role must be AccountRole.COMPANY in order to create a company.")
        
        await self.upload_manager.stage_uploads([
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
            db_account = await self.account_repo.get_by_email(email)

            if db_account:
                raise ACCOUNT_ALREADY_EXISTS_EXCEPTION
            
            hashed_password = hash_password(password)

            account = await self.account_repo.create(Account(
                email=email,
                password=hashed_password,
                role=AccountRole.COMPANY,
            ))
            
            profile = await self.profile_repo.create(CompanyProfile(
                account_id=account.id,
                name=name,
                address=address,
                logo_filename=self.upload_manager.get_staged_file_name(DestFolder.LOGO),
                sec_filename=self.upload_manager.get_staged_file_name(DestFolder.SEC),
                profile_filename=self.upload_manager.get_staged_file_name(DestFolder.PROFILE),
                business_permit_filename=self.upload_manager.get_staged_file_name(DestFolder.BUSINESS_PERMIT),
                list_of_vacancies_filename=self.upload_manager.get_staged_file_name(DestFolder.LIST_OF_VACANCIES),
                cert_from_dole_filename=self.upload_manager.get_staged_file_name(DestFolder.CERT_FROM_DOLE),
                cert_of_no_pending_case_filename=self.upload_manager.get_staged_file_name(DestFolder.CERT_OF_NO_PENDING_CASE),
                reg_dti_cda_filename=self.upload_manager.get_staged_file_name(DestFolder.REG_DTI_CDA),
                reg_of_est_filename=self.upload_manager.get_staged_file_name(DestFolder.REG_OF_EST),
                reg_philjobnet_filename=self.upload_manager.get_staged_file_name(DestFolder.REG_PHILJOBNET),
            ))
            
            await self.db.commit()
            await self.upload_manager.commit()

            account = await self.account_repo.get_by_email(email)
            
            return CompanyAccountOut.model_validate(account) if as_pymodel else (account, profile)
        except HTTPException:
            self.upload_manager.rollback()
            raise
        except Exception as e:
            self.upload_manager.rollback()
            await self.db.rollback()
            Logger.error(f"Unable to create Company's account and profile - {repr(e)}")
            raise UNABLE_TO_REGISTER_ACCOUNT_EXCEPTION


