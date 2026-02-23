from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.schemas.account import AlumniAccountOut
from app.schemas.alumni_profile import AlumniOccupationLocationIn
from app.services.external.geocoding import GeocodingService
from app.repositories.account import AccountRepository
from app.repositories.profile import ProfileRepository
from app.core.exceptions import *
from app.core.enums import AccountRole
from app.core.enums import Action, AlumniApprovalStatus


class AlumniService(GeocodingService):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__()
        
        self.db = db
        self.account_repo = AccountRepository(self.db, AccountRole.ALUMNI)
        self.profile_repo = ProfileRepository(self.db, AccountRole.ALUMNI)
    
    
    async def geocode_occupation_location(self, user: Account, location: AlumniOccupationLocationIn) -> dict:
        user.permissions.raise_unauthorized_if_excludes(Action.GET_ALUMNI_LOCATION_INFO)

        return self.geocode(location.location)
    

    async def get_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Account | dict:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_ALUMNI)
        
        db_account = await self.account_repo.get_alumni_by_id(id)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION
        
        if not as_pymodel:
            return db_account
        
        dict_alumni_account = AlumniAccountOut.model_validate(db_account).model_dump()
        dict_alumni_account["alumni_profile"]["occupations"] = [
            {
                "title": state.occupation.title,
                "location": state.location,
                "is_current": state.is_current,
            }
            for state in db_account.alumni_profile.occupation_states
                if state.occupation
        ]
        dict_alumni_account["alumni_profile"]["socials"] = [
            {
                "platform": social.platform,
                "url": social.url
            }
            for social in db_account.alumni_profile.socials
        ]
        return dict_alumni_account
        

    async def get_by_email(self, user: Account, email: str, as_pymodel: bool = False) -> Account | AlumniAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_ALUMNI)
        
        db_account = await self.account_repo.get_by_email(email)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION
        
        return AlumniAccountOut.model_validate(db_account) if as_pymodel else db_account
        

    async def search(
        self,
        user: Account,
        approval_status: AlumniApprovalStatus | None = None,
        query: str | None = None,
        page: int = 1,
        page_size: int = 20
    ) -> dict:
        user.permissions.raise_unauthorized_if_excludes(Action.READ_ALUMNI)
        
        accounts, total, total_pages = await self.account_repo.search(query, page, page_size, dean_approval_status=approval_status)

        items = [AlumniAccountOut.model_validate(account) for account in accounts]
        
        return {
            "items": items,
            "total": total,
            "total_pages": total_pages,
            "page": page,
            "page_size": page_size,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    

    async def disable_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Account | AlumniAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.ENABLE_DISABLE_ALUMNI)

        db_account = await self.account_repo.get_by_id(id)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION
        
        if db_account.is_default_system_admin:
            raise ACCOUNT_SHOULD_NOT_BE_MODIFIED_EXCEPTION
        
        if db_account.is_disabled:
            raise ACCOUNT_ALREADY_DISABLED_EXCEPTION
        
        db_account = await self.account_repo.disable(db_account)

        return AlumniAccountOut.model_validate(db_account) if as_pymodel else db_account


    async def enable_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Account | AlumniAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.ENABLE_DISABLE_ALUMNI)

        db_account = await self.account_repo.get_by_id(id)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION

        if db_account.is_default_system_admin:
            raise ACCOUNT_SHOULD_NOT_BE_MODIFIED_EXCEPTION
        
        if not db_account.is_disabled:
            raise ACCOUNT_ALREADY_ENABLED_EXCEPTION
        
        db_account = await self.account_repo.enable(db_account)
    
        return AlumniAccountOut.model_validate(db_account) if as_pymodel else db_account


    async def approve_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Account | AlumniAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.APPROVE_ALUMNI)

        db_account = await self.account_repo.get_by_id(id)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION
        
        if db_account.alumni_profile.dean_approval_status == AlumniApprovalStatus.APPROVED:
            raise ALUMNI_ALREADY_APPROVED_EXCEPTION

        await self.profile_repo.approve_alumni(id)
        
        db_account = await self.account_repo.get_by_id(id)

        return AlumniAccountOut.model_validate(db_account) if as_pymodel else db_account


    async def reject_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Account | AlumniAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.REJECT_ALUMNI)

        db_account = await self.account_repo.get_by_id(id)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION
        
        if db_account.alumni_profile.dean_approval_status == AlumniApprovalStatus.REJECTED:
            raise ALUMNI_ALREADY_REJECTED_EXCEPTION

        await self.profile_repo.reject_alumni(id)
        
        db_account = await self.account_repo.get_by_id(id)

        return AlumniAccountOut.model_validate(db_account) if as_pymodel else db_account


    async def pend_by_id(self, user: Account, id: int, as_pymodel: bool = False) -> Account | AlumniAccountOut:
        user.permissions.raise_unauthorized_if_excludes(Action.PEND_ALUMNI)

        db_account = await self.account_repo.get_by_id(id)

        if not db_account:
            raise ACCOUNT_NOT_FOUND_EXCEPTION
        
        if db_account.alumni_profile.dean_approval_status == AlumniApprovalStatus.PENDING:
            raise ALUMNI_ALREADY_PENDING_EXCEPTION

        await self.profile_repo.pend_alumni(id)
        
        db_account = await self.account_repo.get_by_id(id)

        return AlumniAccountOut.model_validate(db_account) if as_pymodel else db_account


