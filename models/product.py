from sqlalchemy import ForeignKey
from db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    resource_type_id: Mapped[int] = mapped_column(ForeignKey("resources.id"), default=1)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner = relationship("User", back_populates="products")