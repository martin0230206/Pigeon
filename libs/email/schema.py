import json
from typing import List

from pydantic import BaseModel, Field, model_validator


class EmailPayload(BaseModel):
    recipient_list: List[str] = Field(..., description="收件人列表")
    """收件人列表"""
    subject: str = Field(..., description="主旨")
    """主旨"""
    html_content: str = Field(..., description="HTML內容")
    """HTML內容"""
    CC_list: List[str] = Field(None, description="抄送人列表")
    """抄送人列表"""

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
