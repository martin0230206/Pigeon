from typing import List

from pydantic import BaseModel, Field


class EmailPayload(BaseModel):
    recipient_list: List[str] = Field(..., description="收件人列表")
    """收件人列表"""
    subject: str = Field(..., description="主旨")
    """主旨"""
    html_content: str = Field(..., description="HTML內容")
    """HTML內容"""
    CC_list: List[str] = Field(None, description="抄送人列表")
    """抄送人列表"""
