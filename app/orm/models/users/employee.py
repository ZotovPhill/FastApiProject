from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.orm.models.base import BaseIDModel


class Employee(BaseIDModel):
    __tablename__ = 'usr_employee'

    address_id = Column(Integer, ForeignKey('usr_address.id', ondelete="SET NULL"))
    address = relationship("Address", back_populates='employees')

    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
