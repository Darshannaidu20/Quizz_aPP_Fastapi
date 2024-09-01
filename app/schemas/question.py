from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.schemas import AnswerOptionReturn


class QuestionType(str, Enum):
    open = "open"
    multiple_choice = "multiple_choice"
    true_false = "true_false"


class QuestionBase(BaseModel):
    content: str
    type: QuestionType = QuestionType.open
    points: int = 1

    model_config = ConfigDict(from_attributes=True)


class QuestionCreate(QuestionBase):
    quiz_id: Optional[int]=None


class QuestionUpdate(BaseModel):
    # not forced to always update all the fields
    content: Optional[str]=None
    type: Optional[QuestionType]=None
    points: Optional[int]=None

    model_config = ConfigDict(from_attributes=True)


class QuestionReturn(QuestionBase):
    id: int
    quiz_id: int
    created_at: datetime
    updated_at: datetime


class QuestionWithOptions(QuestionReturn):
    answer_options: list[AnswerOptionReturn]
