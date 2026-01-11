from app.core.settings import settings
from app.core.enums import Action, AccountRole
from app.core.exceptions import UNAUTHORIZED_ACCESS_EXCEPION

class Permissions:
    def __init__(self, account):
        self.account = account
        self.actions = set()

        match self.account.role:
            case AccountRole.SYSTEM_ADMIN:
                self.actions.update({
                    Action.CREATE_DEANS,
                    Action.READ_DEANS,
                    Action.ENABLE_DISABLE_DEANS,
                    Action.CREATE_PESO_STAFFS,
                    Action.READ_PESO_STAFFS,
                    Action.ENABLE_DISABLE_PESO_STAFFS,
                    Action.CREATE_SCHOOLS,
                    Action.READ_SCHOOLS,
                    Action.ARCHIVE_RESTORE_SCHOOLS,
                })
                
                if self._is_default_sysad:
                    self.actions.update({
                        Action.CREATE_SYSTEM_ADMINS,
                        Action.READ_SYSTEM_ADMINS,
                        Action.ENABLE_DISABLE_SYSTEM_ADMINS
                    })
    
    def can(self, action: Action) -> bool:
        return action in self.actions
    
    def raise_unauthorized_if_excludes(self, action: Action) -> None:
        if not self.can(action):
            raise UNAUTHORIZED_ACCESS_EXCEPION
    
    @property
    def _is_default_sysad(self):
        return self.account.role == AccountRole.SYSTEM_ADMIN and self.account.email == settings.APP_DEFAULT_SYSAD_EMAIL

