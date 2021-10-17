from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import Column, ForeignKey, Index
from sqlalchemy import String, Text, Integer
from app.orm.models.base import BaseUUIDModel


class Category(BaseUUIDModel):
    __tablename__ = "gds_category"

    name = Column(String, unique=True)
    root_id = Column(Integer, ForeignKey("gds_category"))
    description = Column(Text)
    children = relationship(
        "Category",
        backref=backref("root", remote_side=[id])
    )

    __table_args__ = (
        Index("category", "root_id"),
        {}
    )
