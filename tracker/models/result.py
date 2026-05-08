from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from tracker.storage.database import Base

class GameResult(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[int] = mapped_column(nullable=False)
    placement: Mapped[int] = mapped_column(nullable=False)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))

    session: Mapped["Session"] = relationship("Session", back_populates="results")
    player: Mapped["Player"] = relationship("Player")

    def __repr__(self):
        return f"GameResult(player={self.player}, score={self.score})"