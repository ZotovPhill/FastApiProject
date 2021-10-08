from sqlalchemy.orm import relationship

from app.orm.models.base import BaseIDModel
from sqlalchemy import Column, String


class Address(BaseIDModel):

    __tablename__ = 'usr_address'

    employees = relationship("Employee", back_populates="address")

    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
