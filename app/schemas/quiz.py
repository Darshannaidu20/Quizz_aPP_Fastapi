from datetime import datetime
from typing  import Optional
from pydantic import BaseModel, ConfigDict

from app.schemas import QuestionReturn


class QuizBase(BaseModel):
    title: str
    description: Optional[str]=None
    created_by: Optional[int]=None

    model_config = ConfigDict(from_attributes=True)


class QuizCreate(QuizBase):
    pass


class QuizUpdate(BaseModel):
    # not forced to always update all the fields
    title: Optional[str]=None
    description: Optional[str]=None

    model_config = ConfigDict(from_attributes=True)


class QuizReturn(QuizBase):
    id: int
    created_at: datetime
    updated_at: datetime


class QuizWithQuestions(QuizReturn):
    questions: list[QuestionReturn]
