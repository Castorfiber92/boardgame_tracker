from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from tracker.storage.database import Base

class TerraformingMarsSession(Base):
    __tablename__ = "terraforming_mars_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    generations: Mapped[int] = mapped_column(nullable=True)
    with_turmoil: Mapped[bool] = mapped_column(nullable=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))

    session: Mapped["Session"] = relationship("Session")

    def __repr__(self):
        return f"TerraformingMarsSession(generations={self.generations}, with turmoil={self.with_turmoil})"