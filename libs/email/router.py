from fastapi import APIRouter

from .core import send_email
from .schema import EmailPayload

router = APIRouter()


@router.get(
    "test",
    summary="測試"
)
async def test():
    email_payload = EmailPayload(
        recipient_list=[
            "XXXXXXXXXXXXXXX@gmail.com",
        ],
        subject='測試',
        html_content='<h1>Hello World</h1>',
        CC_list=[
            "XXXXXXXXXXXXXXX@gmail.com",
        ]
    )
    send_email(email_payload)
