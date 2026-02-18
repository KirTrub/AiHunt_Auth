from db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column()
    
