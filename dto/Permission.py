from pydantic import BaseModel
from typing import Optional

class PermissionCreate(BaseModel):
    role: int
    resource_id: int
    create_perm: bool
    read_perm: bool
    read_all_perm: bool
    update_perm: bool
    update_all_perm: bool
    delete_perm: bool
    delete_all_perm: bool

class PermissionUpdate(BaseModel):
    role: Optional[int] = None
    resource_id: Optional[int] = None
    create_perm: Optional[bool] = None
    read_perm: Optional[bool] = None
    read_all_perm: Optional[bool] = None
    update_perm: Optional[bool] = None
    update_all_perm: Optional[bool] = None
    delete_perm: Optional[bool] = None
    delete_all_perm: Optional[bool] = None
