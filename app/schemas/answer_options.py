from typing import Optional
from pydantic import BaseModel, ConfigDict

class AnswerOptionBase(BaseModel):
    content: str
    is_correct: bool = False

    model_config = ConfigDict(from_attributes=True)

class AnswerOptionCreate(AnswerOptionBase):
    question_id: Optional[int] = None

class AnswerOptionUpdate(BaseModel):
    # not forced to always update all the fields
    content: Optional[str] = None
    is_correct: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

class AnswerOptionReturn(AnswerOptionBase):
    id: int
    question_id: int
