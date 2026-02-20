from typing import List, Optional
from db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    last_name: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    patronymic: Mapped[Optional[str]] = mapped_column()
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), default=3)
    is_active: Mapped[bool] = mapped_column(default=True)
    password_hashed: Mapped[str] = mapped_column()

    role = relationship("Role")
    products = relationship("Product", back_populates="owner")
    articles = relationship("Article", back_populates="owner")