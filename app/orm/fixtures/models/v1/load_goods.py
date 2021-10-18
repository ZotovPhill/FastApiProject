from fpgen.example.models.goods import Product, Unit, Category
from fpgen.orm.sqlalchemy.sqla_fixtures_loader import SQLAlchemyFixturesLoader


class LoadGoods(SQLAlchemyFixturesLoader):
    def load(self) -> None:
        with self.db.session_scope() as session:
            units = session.query(Unit).all()
            categories = session.query(Category).all()
            objects = [
                Product(
                    name=self.fake.sentence(nb_words=4, variable_nb_words=True),
                    country_of_origin=self.fake.country_code(),
                    expiration_time=self.fake.date_between(start_date='-2y', end_date='+10y'),
                    unit_price=self.fake.random_int(min=1),
                    units_per_package=self.fake.random_int(min=1, max=10),
                    units_in_stock=self.fake.random_int(min=10),
                    unit_id=self.fake.random_element(units),
                    category_id=self.fake.random_element(categories)
                )
                for _ in range(self.quantity)
            ]
            session.bulk_save_objects(objects)

    @staticmethod
    def env_group() -> list:
        return ['dev', 'prod']
