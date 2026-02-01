from json import loads, JSONDecodeError
from fastapi import UploadFile, Form, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.logging import Logger
from app.utils.storage import Upload, UploadManager, DestFolder
from app.core.exceptions import *
from app.core.enums import AccountRole, Action
from app.repositories.school import SchoolRepository
from app.repositories.profile import ProfileRepository
from app.repositories.occupation_state import OccupationStateRepository
from app.models.account import Account
from app.models.dean_profile import DeanProfile
from app.models.alumni_profile import AlumniProfile
from app.models.company_profile import CompanyProfile
from app.models.peso_staff_profile import PesoStaffProfile
from app.models.system_admin_profile import SystemAdminProfile
from app.schemas.dean_profile import DeanProfileOut, DeanProfileIn
from app.schemas.alumni_profile import AlumniProfileOut, AlumniProfileIn
from app.schemas.company_profile import CompanyProfileOut, CompanyProfileIn
from app.schemas.peso_staff_profile import PesoStaffProfileOut, PesoStaffProfileIn
from app.schemas.system_admin_profile import SystemAdminProfileOut, SystemAdminProfileIn


class ProfileService:
    def __init__(self, db: AsyncSession, role: AccountRole) -> None:
        self.db = db
        self.role = role
        self.school_repo = SchoolRepository(self.db)
        self.profile_repo = ProfileRepository(self.db, role)
        self.upload_manager = UploadManager()
        self.occupation_state_repo = OccupationStateRepository(self.db)
        
    
    async def update(
        self,
        user: Account,
        profile: SystemAdminProfileIn | DeanProfileIn | PesoStaffProfileIn,
        as_py_model: bool = False
    ) -> (
        SystemAdminProfile |
        DeanProfile |
        PesoStaffProfile |
        SystemAdminProfileOut |
        DeanProfileOut |
        PesoStaffProfileOut
    ):
        if user.is_default_system_admin:
            raise ACCOUNT_SHOULD_NOT_BE_MODIFIED_EXCEPTION
    
        db_profile = await self.profile_repo.get_by_account_id(user.id)
        
        if not db_profile:
            raise PROFILE_NOT_FOUND_EXCEPTION
        
        try:
            updated_db_profile = await self.profile_repo.update(db_profile.id, profile)
            return self.ProfilePymodel.model_validate(updated_db_profile) if as_py_model else updated_db_profile
        except HTTPException as e:
            await self.db.rollback()
            raise e
        except Exception:
            await self.db.rollback()
            raise PROFILE_CANNOT_BE_UPDATED_EXCEPTION

    
    async def update_dean_school_by_id(
        self,
        user: Account,
        profile_id: int,
        school_id: int,
        as_pymodel: bool = False
    ) -> DeanProfile | DeanProfileOut:
        user.permissions.raise_unauthorized_if_excludes(Action.UPDATE_DEAN_SCHOOL)

        db_school = await self.school_repo.get_by_id(school_id)

        if not db_school:
            raise SCHOOL_NOT_FOUND_EXCEPTION

        db_dean_profile = await self.profile_repo.get_by_id(profile_id)

        if not db_dean_profile:
            raise PROFILE_NOT_FOUND_EXCEPTION
        
        try:
            updated_db_profile = await self.profile_repo.update_dean_school_by_id(profile_id, school_id)
            return DeanProfileOut.model_validate(updated_db_profile) if as_pymodel else updated_db_profile
        except HTTPException as e:
            await self.db.rollback()
            raise e
        except Exception:
            await self.db.rollback()
            raise PROFILE_CANNOT_BE_UPDATED_EXCEPTION
    
    
    async def update_as_company(
        self,
        user: Account,
        name: str | None = Form(None),
        address: str | None = Form(None),
        logo_file: UploadFile | None = File(None),
        sec_file: UploadFile | None = File(None),
        profile_file: UploadFile | None = File(None),
        business_permit_file: UploadFile | None = File(None),
        list_of_vacancies_file: UploadFile | None = File(None),
        cert_from_dole_file: UploadFile | None = File(None),
        cert_of_no_pending_case_file: UploadFile | None = File(None),
        reg_dti_cda_file: UploadFile | None = File(None),
        reg_of_est_file: UploadFile | None = File(None),
        reg_philjobnet_file: UploadFile | None = File(None),
        as_pymodel: bool = False
    ) -> CompanyProfile | CompanyProfileOut:
        db_company_profile = await self.profile_repo.get_by_account_id(user.id)

        if not db_company_profile:
            raise PROFILE_NOT_FOUND_EXCEPTION
    
        await self.upload_manager.stage_uploads([
            Upload(
                logo_file,
                DestFolder.LOGO,
                {"image/png", "image/jpg", "image/jpeg"},
                required=False,
                update_target_filename=db_company_profile.logo_filename
            ),
            Upload(
                sec_file,
                DestFolder.SEC,
                {"application/pdf"},
                required=False,
                update_target_filename=db_company_profile.sec_filename
            ),
            Upload(
                profile_file,
                DestFolder.PROFILE,
                {"application/pdf"},
                required=False,
                update_target_filename=db_company_profile.profile_filename
            ),
            Upload(
                business_permit_file,
                DestFolder.BUSINESS_PERMIT,
                {"application/pdf"},
                required=False,
                update_target_filename=db_company_profile.business_permit_filename
            ),
            Upload(
                list_of_vacancies_file,
                DestFolder.LIST_OF_VACANCIES,
                {"application/pdf"},
                required=False,
                update_target_filename=db_company_profile.list_of_vacancies_filename
            ),
            Upload(
                cert_from_dole_file,
                DestFolder.CERT_FROM_DOLE,
                {"application/pdf"},
                required=False,
                update_target_filename=db_company_profile.cert_from_dole_filename
            ),
            Upload(
                cert_of_no_pending_case_file,
                DestFolder.CERT_OF_NO_PENDING_CASE,
                {"application/pdf"},
                required=False,
                update_target_filename=db_company_profile.cert_of_no_pending_case_filename
            ),
            Upload(
                reg_dti_cda_file,
                DestFolder.REG_DTI_CDA,
                {"application/pdf"},
                required=False,
                update_target_filename=db_company_profile.reg_dti_cda_filename
            ),
            Upload(
                reg_of_est_file,
                DestFolder.REG_OF_EST,
                {"application/pdf"},
                required=False,
                update_target_filename=db_company_profile.reg_of_est_filename
            ),
            Upload(
                reg_philjobnet_file,
                DestFolder.REG_PHILJOBNET,
                {"application/pdf"},
                required=False,
                update_target_filename=db_company_profile.reg_philjobnet_filename
            ),
        ])
        
        new_profile = CompanyProfileIn(
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
        )
        
        try:
            updated_db_profile = await self.profile_repo.update(db_company_profile.id, new_profile)
            await self.upload_manager.commit()
            return self.ProfilePymodel.model_validate(updated_db_profile) if as_pymodel else updated_db_profile
        except HTTPException as e:
            await self.db.rollback()
            await self.upload_manager.rollback()
            raise e
        except Exception as e:
            await self.db.rollback()
            await self.upload_manager.rollback()
            Logger.error(f"Unable to update profile - {repr(e)}")
            raise PROFILE_CANNOT_BE_UPDATED_EXCEPTION
    
    
    async def update_as_alumni(
        self,
        user: Account,
        address: str | None = Form(None),
        phone_number: str | None = Form(None),
        profile_picture_file: UploadFile | None = File(None),
        curriculum_vitae_file: UploadFile | None = File(None),
        as_pymodel: bool = False
    ) -> AlumniProfile | AlumniProfileOut:
        db_alumni_profile = await self.profile_repo.get_by_account_id(user.id)

        if not db_alumni_profile:
            raise PROFILE_NOT_FOUND_EXCEPTION
    
        await self.upload_manager.stage_uploads([
            Upload(
                profile_picture_file,
                DestFolder.PROFILE_PICTURE,
                {"image/png", "image/jpg", "image/jpeg"},
                required=False,
                update_target_filename=db_alumni_profile.profile_picture_filename
            ),
            Upload(
                curriculum_vitae_file,
                DestFolder.CURRICULUM_VITAE,
                {"application/pdf"},
                required=False,
                update_target_filename=db_alumni_profile.curriculum_vitae_filename
            )
        ])
        
        new_profile = AlumniProfileIn(
            address=address,
            phone_number=phone_number,
            profile_picture_filename=self.upload_manager.get_staged_file_name(DestFolder.PROFILE_PICTURE),
            curriculum_vitae_filename=self.upload_manager.get_staged_file_name(DestFolder.CURRICULUM_VITAE),
        )
        
        try:
            updated_db_profile = await self.profile_repo.update(db_alumni_profile.id, new_profile)
            await self.upload_manager.commit()
            return self.ProfilePymodel.model_validate(updated_db_profile) if as_pymodel else updated_db_profile
        except HTTPException as e:
            await self.db.rollback()
            await self.upload_manager.rollback()
            raise e
        except Exception as e:
            await self.db.rollback()
            await self.upload_manager.rollback()
            Logger.error(f"Unable to update profile - {repr(e)}")
            raise PROFILE_CANNOT_BE_UPDATED_EXCEPTION
    
    
    @property
    def ProfilePymodel(self):
        match self.role:
            case AccountRole.DEAN: return DeanProfileOut
            case AccountRole.ALUMNI: return AlumniProfileOut
            case AccountRole.COMPANY: return CompanyProfileOut
            case AccountRole.PESO_STAFF: return PesoStaffProfileOut
            case AccountRole.SYSTEM_ADMIN: return SystemAdminProfileOut
            case _: raise ValueError("Invalid role value.")
