from pathlib import Path
from typing import List

from fastapi import APIRouter, Body, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from .core import send_email
from .schema import EmailPayload

router = APIRouter()


@router.post(
    "/email/",
    summary="寄Email"
)
async def post_email(
    email_payload: EmailPayload = Body(...),
    upload_file_list: List[UploadFile] = File(None, description="附加檔案"),
):
    attachment_filename_list = [
        upload_file.filename
        for upload_file in upload_file_list
    ]
    attachment_list = [
        upload_file.file.read()
        for upload_file in upload_file_list
    ]
    send_email(
        email_payload,
        dict(zip(attachment_filename_list, attachment_list)),
    )
