from datetime import datetime
from typing import TYPE_CHECKING, Type, Union

from sqlalchemy import DateTime, ForeignKey, String, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship
from sqlalchemy.sql import func

from app.models.database import Base
from app.schemas import QuizCreate

if TYPE_CHECKING:
    from app.models.question import Question
    from app.models.user import User

class Quiz(Base):
    __tablename__ = "quizzes"

    title: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # have to use "Question" to avoid circular dependencies
    questions: Mapped[list["Question"]] = relationship(
        "Question", back_populates="quiz", cascade="delete, delete-orphan"
    )
    user: Mapped["User"] = relationship("User", back_populates="quizzes")

    @classmethod
    async def create(cls: Type["Quiz"], db: AsyncSession, quiz: QuizCreate) -> "Quiz":
        new_quiz = cls(
            title=quiz.title, description=quiz.description, created_by=quiz.created_by
        )
        new_quiz.updated_at = func.now()
        db.add(new_quiz)
        await db.commit()
        await db.refresh(new_quiz)

        return new_quiz

    @classmethod
    async def get_multiple(
        cls: Type["Quiz"], db: AsyncSession, offset: int = 0, limit: int = 25
    ) -> list["Quiz"]:
        result = await db.execute(
            select(cls).order_by(desc(cls.created_at)).offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    @classmethod
    async def get_with_questions(cls: Type["Quiz"], db: AsyncSession, id: int) -> Union["Quiz", None]:
        result = await db.execute(
            select(cls).where(cls.id == id).options(joinedload(cls.questions))
        )
        return result.scalar()

    @classmethod
    async def get_quiz_created_by(cls: Type["Quiz"], db: AsyncSession, id: int) -> Union[int, None]:
        result = await db.execute(select(cls.created_by).where(cls.id == id))
        return result.scalar()
