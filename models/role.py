from db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    
    permissions = relationship("Permission", back_populates="role_rel")