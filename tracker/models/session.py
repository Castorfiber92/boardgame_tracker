from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from tracker.storage.database import Base

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(nullable=False)
    notes: Mapped[str] = mapped_column(nullable=True)
    boardgame_id: Mapped[int] = mapped_column(ForeignKey("boardgames.id"))

    boardgame: Mapped["BoardGame"] = relationship("BoardGame")
    results: Mapped[list["GameResult"]] = relationship("GameResult", back_populates="session")

    def __repr__(self):
        return f"Session(date={self.date}, boardgame={self.boardgame})"