import os
import magic
import aiofiles
from enum import Enum
from PIL import Image
from uuid import uuid4
from pathlib import Path
from slugify import slugify
from fastapi import UploadFile

from app.core.exceptions import *
from app.utils.logging import Logger

MIME_EXT = {
    # images
    "image/jpeg": "jpeg",
    "image/png": "png",
    "image/gif": "gif",
    "image/webp": "webp",
    "image/bmp": "bmp",
    "image/tiff": "tiff",
    "image/x-icon": "ico",

    # pdfs
    "application/pdf": "pdf",

    # text
    "text/plain": "txt",
    "text/csv": "csv",
    "text/html": "html",
    "text/xml": "xml",

    # office documents
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/vnd.ms-excel": "xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    "application/vnd.ms-powerpoint": "ppt",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",

    # archives
    "application/zip": "zip",
    "application/x-tar": "tar",
    "application/x-gzip": "gz",
    "application/x-7z-compressed": "7z",
    "application/x-rar-compressed": "rar",

    # json / javascript
    "application/json": "json",
    "application/javascript": "js",
}

STORAGE_FOLDER_PATH = Path(__file__).parent.parent / "storage"
TEMP_STORAGE_FOLDER_PATH = STORAGE_FOLDER_PATH / "temp"
COMPANY_FOLDER_PATH = STORAGE_FOLDER_PATH / "company"
COMPANY_LOGO_FOLDER_PATH = COMPANY_FOLDER_PATH / "logo"
COMPANY_SEC_FOLDER_PATH = COMPANY_FOLDER_PATH / "sec"
COMPANY_PROFILE_FOLDER_PATH = COMPANY_FOLDER_PATH / "profile"
COMPANY_BUSINESS_PERMIT_FOLDER_PATH = COMPANY_FOLDER_PATH / "business_permit"
COMPANY_LIST_OF_VACANCIES_FOLDER_PATH = COMPANY_FOLDER_PATH / "list_of_vacancies"
COMPANY_CERT_FROM_DOLE_FOLDER_PATH = COMPANY_FOLDER_PATH / "cert_from_dole"
COMPANY_CERT_OF_NO_PENDING_CASE_FOLDER_PATH = COMPANY_FOLDER_PATH / "cert_of_no_pending_case"
COMPANY_REG_DTI_CDA_FOLDER_PATH = COMPANY_FOLDER_PATH / "reg_dti_cda"
COMPANY_REG_OF_EST_FOLDER_PATH = COMPANY_FOLDER_PATH / "reg_of_est"
COMPANY_REG_PHILJOBNET_FOLDER_PATH = COMPANY_FOLDER_PATH / "reg_philjobnet"
ALUMNI_FOLDER_PATH = STORAGE_FOLDER_PATH / "alumni"
ALUMNI_PROFILE_PICTURE_FOLDER_PATH = ALUMNI_FOLDER_PATH / "profile_picture"
ALUMNI_CURRICULUM_VITAE_PATH = ALUMNI_FOLDER_PATH / "curriculum_vitae"
DEAN_FOLDER_PATH = STORAGE_FOLDER_PATH / "dean"
DEAN_RECORD_FOLDER_PATH = DEAN_FOLDER_PATH / "record"

paths = {
    "storage": STORAGE_FOLDER_PATH,
    "temp": TEMP_STORAGE_FOLDER_PATH,
    "company": COMPANY_FOLDER_PATH,
    "logo": COMPANY_LOGO_FOLDER_PATH,
    "sec": COMPANY_SEC_FOLDER_PATH,
    "profile": COMPANY_PROFILE_FOLDER_PATH,
    "business_permit": COMPANY_BUSINESS_PERMIT_FOLDER_PATH,
    "list_of_vacancies": COMPANY_LIST_OF_VACANCIES_FOLDER_PATH,
    "cert_from_dole": COMPANY_CERT_FROM_DOLE_FOLDER_PATH,
    "cert_of_no_pending_case": COMPANY_CERT_OF_NO_PENDING_CASE_FOLDER_PATH,
    "reg_dti_cda": COMPANY_REG_DTI_CDA_FOLDER_PATH,
    "reg_of_est": COMPANY_REG_OF_EST_FOLDER_PATH,
    "reg_philjobnet": COMPANY_REG_PHILJOBNET_FOLDER_PATH,
    "alumni": ALUMNI_FOLDER_PATH,
    "profile_picture": ALUMNI_PROFILE_PICTURE_FOLDER_PATH,
    "curriculum_vitae": ALUMNI_CURRICULUM_VITAE_PATH,
    "dean": DEAN_FOLDER_PATH,
    "record": DEAN_RECORD_FOLDER_PATH
}

class DestFolder(str, Enum):
    LOGO = "logo"
    SEC = "sec"
    PROFILE = "profile"
    BUSINESS_PERMIT = "business_permit"
    LIST_OF_VACANCIES = "list_of_vacancies"
    CERT_FROM_DOLE = "cert_from_dole"
    CERT_OF_NO_PENDING_CASE = "cert_of_no_pending_case"
    REG_DTI_CDA = "reg_dti_cda"
    REG_OF_EST = "reg_of_est"
    REG_PHILJOBNET = "reg_philjobnet"
    PROFILE_PICTURE = "profile_picture"
    CURRICULUM_VITAE = "curriculum_vitae"
    RECORD = "record"


def initialize_storage() -> None:
    for folder_name, folder_path in paths.items():
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            Logger.success(f"{folder_name.replace('_', ' ').title()} folder created.")
        else:
            Logger.info(f"{folder_name.replace('_', ' ').title()} folder exists.")


class Upload:
    def __init__(
        self,
        file: UploadFile | None,
        dest_folder: DestFolder,
        allowed_mimes: set[str],
        required: bool = True,
        max_size: int = 5,
        max_filename_length: int = 50
    ):
        self.file: UploadFile | None = file
        self.dest_folder: DestFolder = dest_folder
        self.allowed_mimes = allowed_mimes
        self.required = required
        self.max_size = max_size
        self.max_filename_length = max_filename_length


class UploadManager:
    def __init__(self, *, image_resize_size: tuple[int, int] = (400, 400)):
        self.staged_files_info = {}
        self.image_resize_size = image_resize_size


    async def get_magic_mime_type(self, file: UploadFile) -> str:
        content = await file.read(2048)
        mime = magic.from_buffer(content, mime=True)
        file.file.seek(0)
        return mime


    async def get_file_size(self, file: UploadFile) -> int:
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0)
        return size

    
    async def rollback(self) -> None:
        for _dest_folder, info in self.staged_files_info.items():
            if not info:
                continue
            
            temp_file_path = info.get("temp_file_path")
            
            try:
                if temp_file_path.exists():
                    temp_file_path.unlink(missing_ok=True)
            except Exception as e:
                Logger.error(f"Unable to delete file - {e}")
        
        self.staged_files_info.clear()

    
    async def stage_upload(self, upload: Upload) -> None:
        # STEP 1: Checks
        
        # PHASE 1: file requiredness check
        if not upload.file:
            if upload.required:
                await self.rollback()
                raise FILE_NOT_PROVIDED_EXCEPTION(upload.dest_folder.value)
            
            self.staged_files_info[upload.dest_folder.value] = None
            return
        
        # PHASE 2: NAME LENGTH check
        if len(upload.file.filename) > upload.max_filename_length:
            await self.rollback()
            raise FILE_NAME_LENGTH_TOO_LONG_EXCEPTION(upload.dest_folder.value, upload.max_filename_length)
        
        # PHASE 3: FILE SIZE check
        file_size = await self.get_file_size(upload.file)
        if file_size > upload.max_size * 1024 * 1024:
            await self.rollback()
            raise FILE_SIZE_TOO_BIG_EXCEPTION(upload.dest_folder.value, upload.max_size)
        
        # PHASE 4: FILE VALIDITY check by mime type
        magic_mime = await self.get_magic_mime_type(upload.file)
        
        if magic_mime not in upload.allowed_mimes:
            await self.rollback()
            raise FILE_TYPE_NOT_SUPPORTED_EXCEPTION(upload.dest_folder.value)
        
        # STEP 2: Transformation

        # PHASE 1: NAME NORMALIZATION
        stem = Path(upload.file.filename).stem
        fallback_ext = Path(upload.file.filename).suffix.replace(".", "").lower()
        ext = MIME_EXT.get(magic_mime, fallback_ext)
        new_filename = slugify(stem)
        new_filename = f"{new_filename}-{str(uuid4())[:13]}.{ext}"

        # PHASE 2.0: TEMP PATH ASSIGNMENT
        temp_path = paths.get("temp")
        temp_path.mkdir(parents=True, exist_ok=True)
        temp_file_path = temp_path / new_filename
        
        # PHASE 2.1: REAL PATH ASSIGNMENT
        real_path = paths.get(upload.dest_folder.value)
        real_path.mkdir(parents=True, exist_ok=True)
        real_file_path = real_path / new_filename
        
        try:
            async with aiofiles.open(temp_file_path, "wb") as buffer:
                content = await upload.file.read()
                await buffer.write(content)
        finally:
            await upload.file.close()
        
        # PHASE 3: IMAGE RESIZING (for images only)
        if magic_mime.startswith("image/"):
            try:
                with Image.open(temp_file_path) as img:
                    img.load()
                    img.thumbnail(size=self.image_resize_size)
                    img.save(temp_file_path)
            except Exception as e:
                Logger.error(f"Cannot resize image - {repr(e)}")
                await self.rollback()
                raise IMAGE_FILE_CANNOT_BE_READ_EXCEPTION(upload.dest_folder.value)
        
        self.staged_files_info[upload.dest_folder.value] = {
            "filename": new_filename,
            "temp_file_path": temp_file_path,
            "real_file_path": real_file_path
        }

    
    async def stage_uploads(self, uploads: list[Upload]) -> None:
        for upload in uploads:
            await self.stage_upload(upload)

    
    def get_staged_file_name(self, dest_folder: DestFolder) -> str | None:
        info = self.staged_files_info.get(dest_folder.value)
        return info.get("filename") if info else None

    
    async def commit(self) -> None:
        for _dest_folder, info in self.staged_files_info.items():
            if not info:
                continue
        
            temp_file_path = info.get("temp_file_path")
            real_file_path = info.get("real_file_path")

            if temp_file_path.exists():
                os.replace(temp_file_path, real_file_path)

