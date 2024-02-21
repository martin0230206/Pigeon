from typing import List

from fastapi import APIRouter, Body, File, HTTPException, UploadFile, status
from hurry import filesize
from redis import Redis
from rq import Queue

from libs.config import CONFIG

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
            detail=f"附加檔案總大小不可超過{filesize.size(ATTACHMENT_MAX_TOTAL_SIZE)}"
        )

    attachment_filename_list = [
        upload_file.filename
        for upload_file in upload_file_list
    ]
    attachment_list = [
        upload_file.file.read()
        for upload_file in upload_file_list
    ]

    queue = Queue(
        name=CONFIG.queue.queue_name,
        connection=Redis(CONFIG.redis.host, CONFIG.redis.port),
    )
    queue.enqueue(
        send_email,
        email_payload,
        dict(zip(attachment_filename_list, attachment_list))
    )
