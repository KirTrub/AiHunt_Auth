from db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[int] = mapped_column(ForeignKey("roles.id"), index=True)
    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.id"))
    create_perm: Mapped[bool] = mapped_column()
    read_perm: Mapped[bool] = mapped_column()
    read_all_perm: Mapped[bool] = mapped_column()
    update_perm: Mapped[bool] = mapped_column()
    update_all_perm: Mapped[bool] = mapped_column()
    delete_perm: Mapped[bool] = mapped_column()
    delete_all_perm: Mapped[bool] = mapped_column()