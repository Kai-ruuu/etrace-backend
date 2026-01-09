from enum import Enum

class AccountRole(str, Enum):
    SYSTEM_ADMINISTRATOR = "SYSTEM_ADMINISTRATOR"
    DEAN = "DEAN"
    PESO_STAFF = "PESO_STAFF"
    COMPANY = "COMPANY"
    ALUMNI = "ALUMNI"

    @classmethod
    def is_valid(_class, role: str) -> bool:
        return role in _class._value2member_map_
    
    @classmethod
    def all(_class) -> list:
        return [_class.SYSTEM_ADMINISTRATOR, _class.DEAN, _class.PESO_STAFF, _class.COMPANY, _class.ALUMNI]

    @classmethod
    def as_display(_class, role: str) -> str:
        if not _class.is_valid(role):
            return None
        
        role_display_map = {
            _class.SYSTEM_ADMINISTRATOR: 'System Administrator',
            _class.PESO_STAFF: 'PESO Staff',
            _class.DEAN: 'Dean',
            _class.COMPANY: 'Company',
            _class.ALUMNI: 'Alumni',
        }
        
        return role_display_map[role]

