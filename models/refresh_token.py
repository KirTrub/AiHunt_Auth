from datetime import datetime
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.session import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token: Mapped[str] = mapped_column(unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    is_revoked: Mapped[bool] = mapped_column(default=False)

class BlackListedToken(Base):
    __tablename__ = "blacklisted_tokens"

    jti: Mapped[str] = mapped_column(primary_key=True, index=True)
    expires_at: Mapped[datetime] = mapped_column()