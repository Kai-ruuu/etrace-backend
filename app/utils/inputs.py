from email_validator import validate_email, EmailNotValidError

from app.core.exceptions import RAISE_INVALID_EMAIL_EXCEPTION


def validated_email(raw_email: str) -> str:
    try:
        return validate_email(raw_email).email
    except EmailNotValidError as e:
        raise RAISE_INVALID_EMAIL_EXCEPTION(str(e))
    except Exception:
        raise RAISE_INVALID_EMAIL_EXCEPTION()

