from db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), index=True)
    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.id"))
    
    create_perm: Mapped[bool] = mapped_column(default=False)
    read_perm: Mapped[bool] = mapped_column(default=False)
    read_all_perm: Mapped[bool] = mapped_column(default=False)
    update_perm: Mapped[bool] = mapped_column(default=False)
    update_all_perm: Mapped[bool] = mapped_column(default=False)
    delete_perm: Mapped[bool] = mapped_column(default=False)
    delete_all_perm: Mapped[bool] = mapped_column(default=False)

    role_rel = relationship("Role", back_populates="permissions")
    resource_rel = relationship("Resource", back_populates="permissions")