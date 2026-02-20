from typing import List

from sqlalchemy import ForeignKey
from db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship



class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    resource_type_id: Mapped[int] = mapped_column(ForeignKey("resources.id"), default=2)
    name: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column()
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner = relationship("User", back_populates="articles") 