from db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    
    last_name: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    patronymic: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    role: Mapped[str] = mapped_column(ForeignKey("roles.name"), default="user")
    
    is_active: Mapped[bool] = mapped_column(default=True)

    password_hashed: Mapped[str] = mapped_column()