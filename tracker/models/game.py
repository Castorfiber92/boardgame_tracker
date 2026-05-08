from sqlalchemy.orm import Mapped, mapped_column
from tracker.storage.database import Base

class BoardGame(Base):
    __tablename__ = "boardgames"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"BoardGame(name={self.name})"