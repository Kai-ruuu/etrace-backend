import os
import magic
from enum import Enum
from PIL import Image
from uuid import uuid4
from pathlib import Path
from slugify import slugify
from fastapi import UploadFile
from shutil import copyfileobj

from app.exceptions import *

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
DEAN_RECORD_FOLDER_PATH = DEAN_FOLDER_PATH / "record" # graduate records

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
    for folder_name, fodler_path in paths.items():
        if not fodler_path.exists():
            fodler_path.mkdir(parents=True, exist_ok=True)
            print(f"[SETUP] {folder_name.replace("_", " ").title()} folder created.")
        else:
            print(f"[SETUP] {folder_name.replace("_", " ").title()} folder exists.")

class Upload:
    def __init__(
        self,
        file: UploadFile | None,
        dest_folder: DestFolder,
        allowed_mimes: set[str],
        required: bool=True,
        max_size: int=5,
        max_filename_length: int=50
    ):
        self.file: UploadFile = file
        self.dest_folder: DestFolder = dest_folder
        self.allowed_mimes = allowed_mimes
        self.required = required
        self.max_size = max_size
        self.max_filename_length = max_filename_length

def get_magic_mime_type(file: Upload) -> str:
    content = file.file.read(2048)
    mime = magic.from_buffer(content, mime=True)
    file.file.seek(0)
    return mime

def get_file_size(file: Upload) -> int:
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    return size

class UploadManager:
    def __init__(self, *, image_resize_size: tuple[float, float]=(400, 400)):
        self.staged_files_info = {}
        self.image_resize_size = image_resize_size
    
    def rollback(self) -> None:
        """Delete all the previously staged files."""
        
        for _dest_folder, info in self.staged_files_info.items():
            if not info:
                continue
            
            temp_file_path = info.get("temp_file_path")
            
            try:
                temp_file_path.unlink(missing_ok=True)
            except Exception as e:
                print(f"[DEBUG] Unable to delete file - {e}")
        
        self.staged_files_info.clear()
    
    def stage_upload(self, upload: Upload) -> None:
        """Stages an upload. If fails the checks and resizing, rollback."""
        
        # STEP 1: Checks
        
        # PHASE 1: file requiredness check
        if not upload.file:
            if upload.required:
                self.rollback()
                RAISE_FILE_NOT_PROVIDED_EXCEPTION_FOR(upload.dest_folder.value)
            
            self.staged_files_info[upload.dest_folder.value] = None
            return
        
        # PHASE 2: NAME LENGTH check
        # we need extra space for uuid characters, therefore we need to prevent them from sending long-named files
        if len(upload.file.filename) > upload.max_filename_length:
            self.rollback()
            RAISE_FILE_NAME_LENGTH_TOO_LONG_EXCEPTION_FOR(upload.dest_folder.value, upload.max_filename_length)
        
        # PHASE 3: FILE SIZE check
        if get_file_size(upload.file) > upload.max_size * 1024 * 1024:
            self.rollback()
            RAISE_FILE_SIZE_TOO_BIG_EXCEPTION_FOR(upload.dest_folder.value, upload.max_size)
        
        # PHASE 4: FILE VALIDITY check by mime type
        magic_mime = get_magic_mime_type(upload.file)
        
        if magic_mime not in upload.allowed_mimes:
            self.rollback()
            RAISE_FILE_TYPE_NOT_SUPPORTED_EXCEPTION_FOR(upload.dest_folder.value)
        
        # STEP 2: Transformation

        # PHASE 1: NAME NORMALIZATION
        stem = Path(upload.file.filename).stem
        fallback_ext = Path(upload.file.filename).suffix.replace(".", "").lower()
        ext = MIME_EXT.get(magic_mime, fallback_ext)
        new_filename = slugify(stem)
        new_filename = f"{new_filename}-{str(uuid4())[:13]}.{ext}"

        # PHASE 2.0: TEMP PATH ASSIGNMENT
        # (Path) storage folder
        temp_path = paths.get("temp")
        temp_path.mkdir(parents=True, exist_ok=True)
        temp_file_path = temp_path / new_filename
        
        # PHASE 2.1: REAL PATH ASSIGNMENT
        # (Path) final folder
        real_path = paths.get(upload.dest_folder.value)
        real_path.mkdir(parents=True, exist_ok=True)
        real_file_path = real_path / new_filename
        
        try:
            with temp_file_path.open("wb") as buffer:
                copyfileobj(upload.file.file, buffer)
        finally:
            upload.file.file.close()
        
        # PHASE 3: IMAGE RESIZING (for images only)
        # would also help us determine if the image file is a real image, (disguised ones can't be resized XD)
        if not magic_mime.startswith("image/"):
            return
            
        try:
            path = str(temp_file_path)
            
            with Image.open(path) as img:
                img.load()
                img.thumbnail(size=self.image_resize_size)
                img.save(temp_file_path)
        except Exception as e:
            print(f"[DEBUG] Cannot resize image - {repr(e)}")
            self.rollback()
            raise RAISE_IMAGE_FILE_CANNOT_BE_READ_EXCEPTION_FOR(upload.dest_folder.value)
        
        self.staged_files_info[upload.dest_folder.value] = {
            "filename": new_filename,
            "temp_file_path": temp_file_path,
            "real_file_path": real_file_path
        }
        print(self.staged_files_info[upload.dest_folder.value])
    
    def stage_uploads(self, uploads: list[Upload]) -> None:
        """Stage a list of uploads."""
        for upload in uploads:
            self.stage_upload(upload)
    
    def get_staged_file_name(self, dest_folder: DestFolder) -> str | None:
        info = self.staged_files_info.get(dest_folder.value)
        return info.get("filename") if info else None
    
    def commit(self) -> None:
        """Move the staged files from temp folder to their actuald designated folders."""
        
        for _dest_folder, info in self.staged_files_info.items():
            if not info:
                continue
        
            temp_file_path = info.get("temp_file_path")
            real_file_path = info.get("real_file_path")

            if temp_file_path.exists():
                os.replace(temp_file_path, real_file_path)
    
    