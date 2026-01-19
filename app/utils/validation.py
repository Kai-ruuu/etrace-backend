import pandas as pd
from pathlib import Path

from app.core.exceptions import *
from app.utils.logging import Logger
from app.utils.storage import UploadManager, DestFolder


async def validate_and_transform_graduate_record(temp_path: Path, upload_manager: UploadManager) -> None:
    try:
        df = pd.read_csv(temp_path)

        # transform column names to lowercase
        df.columns = [col.lower() for col in df.columns]
        
        date_columns = {"birthday"}
        optional_columns = {"middle name"}
        required_columns = {
            "full name",
            "student number",
            "birthplace",
            "last name",
            "first name",
            "gender",
            "full address",
            "contact number"
        } | date_columns
        must_have_columns =  required_columns |  optional_columns | date_columns
        present_columns = {column.lower() for column in df.columns}

        # raise if there are missing must have columns
        if not must_have_columns <= present_columns:
            missing_columns = must_have_columns - present_columns
            RAISE_CSV_MISSING_COLUMNS_EXCEPTION(missing_columns)
        
        # raise if there are any required columns that's missing a value
        for column in required_columns:
            if column in df.columns:
                if df[column].astype(str).str.strip().replace("nan", "").eq("").any():
                    RAISE_CSV_MISSING_COLUMN_VALUE_EXCEPTION(column)
        
        # normalize any date format to mm/dd/yyyy
        for column in date_columns:
            if column in df.columns:
                # parse and normalize as datetime
                as_datetime = pd.to_datetime(df[column], errors="coerce")
                # key the date only and discard the time
                as_dateonly = as_datetime.dt.normalize()
                # trimmed
                as_lowered = str(as_dateonly).lower()

                # raise if the date cannot be parsed properly
                if "nat" in as_lowered or "nan" in as_lowered:
                    RAISE_CSV_INCONSISTENT_DATE_FORMAT_EXCEPTION(column)
                
                # save the date-only column value
                df[column] = as_dateonly
        
        # save as temp-csv
        df.to_csv(temp_path, index=False)
    except HTTPException:
        await upload_manager.rollback()
        raise
    except Exception as e:
        Logger.error(f"Graduate Record cannot be read - {repr(e)}")
        await upload_manager.rollback()
        RAISE_FILE_CANNOT_BE_READ_EXCEPTION(DestFolder.RECORD.value)