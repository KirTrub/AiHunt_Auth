from datetime import datetime, timezone
from db.session import Base

from sqlalchemy.orm import Mapped, mapped_column

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    jti: Mapped[str] = mapped_column(primary_key=True, index=True)
    expires_at: Mapped[datetime] = mapped_column()