from pathlib import Path
from typing import List

from fastapi import APIRouter, Body, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from .core import send_email
from .schema import ATTACHMENT_MAX_TOTAL_SIZE, EmailPayload

router = APIRouter()


@router.post(
    "/email/",
    summary="寄Email"
)
async def post_email(
    email_payload: EmailPayload = Body(...),
    upload_file_list: List[UploadFile] = File(None, description="附加檔案"),
):
    if sum(upload_file.size for upload_file in upload_file_list) > ATTACHMENT_MAX_TOTAL_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="附加檔案總大小不可超過25MB"
        )

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
