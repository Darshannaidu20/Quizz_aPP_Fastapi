from datetime import datetime
from typing import TYPE_CHECKING, Type, Union

from sqlalchemy import DateTime, ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship
from sqlalchemy.sql import func

from app.models.database import Base
from app.schemas import QuestionCreate

if TYPE_CHECKING:
    from app.models.answer_options import AnswerOption
    from app.models.quiz import Quiz

QuestionType = Type["Question"]  # Type alias for the class

class Question(Base):
    __tablename__ = "questions"

    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id"))
    content: Mapped[str] = mapped_column(String(256), nullable=False)
    type: Mapped[str] = mapped_column(String(64), nullable=False)
    points: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # types as strings (i.e. "Quiz") to avoid circular dependencies
    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="questions")

    answer_options: Mapped[list["AnswerOption"]] = relationship(
        "AnswerOption", back_populates="question", cascade="delete, delete-orphan"
    )

    @classmethod
    async def create(cls: QuestionType, db: AsyncSession, question: QuestionCreate) -> QuestionType:
        new_question = cls(
            quiz_id=question.quiz_id,
            content=question.content,
            type=question.type,
            points=question.points,
        )
        new_question.updated_at = func.now()
        db.add(new_question)
        await db.commit()
        await db.refresh(new_question)

        return new_question

    @classmethod
    async def get_by_quiz_id(cls: QuestionType, db: AsyncSession, quiz_id: int) -> list[QuestionType]:
        result = await db.execute(select(cls).where(cls.quiz_id == quiz_id))
        return list(result.scalars().all())

    @classmethod
    async def get_with_answers(cls: QuestionType, db: AsyncSession, id: int) -> Union[QuestionType, None]:
        result = await db.execute(
            select(cls).where(cls.id == id).options(joinedload(cls.answer_options))
        )

        return result.scalar()
