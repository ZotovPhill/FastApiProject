from datetime import datetime

from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from app.orm.models.base import BaseUUIDModel
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    DateTime, Integer, CheckConstraint, Boolean, Index, func,
)
from sqlalchemy.orm import backref, relationship
from sqlalchemy_utils import CountryType


class Product(BaseUUIDModel):
    __tablename__ = "gds_product"

    name = Column(String)
    country_of_origin = Column(CountryType)
    expiration_time = Column(DateTime, nullable=True)
    unit_price = Column(Integer, default=0)
    units_per_package = Column(Integer, default=0)
    _units_in_stock = Column("units_in_stock", Integer, default=0)
    _is_visible = Column("is_visible", Boolean, default=True)
    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("gds_category.id", ondelete="SET NULL")
    )
    category = relationship(
        "Category",
        cascade="all, delete",
        passive_deletes=True,
        backref=backref('products', lazy='dynamic'),
        remote_side='Category.id'
    )
    unit_id = Column(
        UUID(as_uuid=True),
        ForeignKey("gds_unit.id", ondelete="SET NULL")
    )
    unit = relationship(
        "Unit",
        cascade="all, delete",
        passive_deletes=True,
        backref=backref('products', lazy='dynamic'),
        remote_side='Unit.id'
    )

    @hybrid_property
    def units_in_stock(self):
        return self._units_in_stock

    @units_in_stock.update_expression
    def units_in_stock(self, value):
        return [
            (self._units_in_stock, self._units_in_stock + value)
        ]

    @hybrid_property
    def price_per_package(self):
        return self.unit_price * self.units_per_package

    @hybrid_property
    def is_visible(self):
        return self._is_visible

    @is_visible.setter
    def is_visible(self, value: bool = True):
        if self.expiration_time:
            self._is_visible = self.expiration_time > datetime.now()

        self._is_visible = value

    @hybrid_method
    def show_available(self) -> bool:
        # Product.query.filter(Product.is_visible()).all()
        if self.expiration_time:
            return self.expiration_time > datetime.now() and self._is_visible

        return self._is_visible

    __table_args__ = (
        CheckConstraint(unit_price >= 0, name='unit_price_non_negative_constraint'),
        CheckConstraint(units_per_package >= 0, name='quantity_per_unit_non_negative_constraint'),
        CheckConstraint(_units_in_stock >= 0, name='quantity_per_unit_non_negative_constraint'),
        Index("category", "category_id"),
        Index("visible", "id", func.IF(is_visible == 1)),
        {}
    )
