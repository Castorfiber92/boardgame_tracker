from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from tracker.storage.database import Base

class TerraformingMarsResult(Base):
    __tablename__ = "terraforming_mars_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_result_id: Mapped[int] = mapped_column(ForeignKey("game_results.id"))
    tr_rating: Mapped[int] = mapped_column(nullable=False)
    points_milestones_and_awards: Mapped[int] = mapped_column(nullable=False)
    points_board: Mapped[int] = mapped_column(nullable=False)
    points_on_cards: Mapped[int] = mapped_column(nullable=False)
    points_from_cards: Mapped[int] = mapped_column(nullable=False)
    corporation: Mapped[str] = mapped_column(nullable=False)
    prelude_1: Mapped[str] = mapped_column(nullable=True)
    prelude_2: Mapped[str] = mapped_column(nullable=True)

    game_result: Mapped["GameResult"] = relationship("GameResult")

    @property
    def points_total(self):
        return (
            self.tr_rating +                      
            self.points_milestones_and_awards +   
            self.points_board +                   
            self.points_on_cards +
            self.points_from_cards
        )

    def __repr__(self):
        return f"TerraformingMarsResult(corporation={self.corporation}, total={self.points_total})"