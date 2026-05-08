from sqlalchemy.orm import Mapped, mapped_column
from tracker.storage.database import Base

class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"Player(name={self.name})"