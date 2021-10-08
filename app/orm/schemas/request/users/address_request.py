from typing import Optional

from app.orm.schemas.base_schema import BaseIdModel


class Address(BaseIdModel):
    street: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
