from fpgen.example.models.goods import Category
from fpgen.orm.sqlalchemy.sqla_fixtures_loader import SQLAlchemyFixturesLoader


class LoadCategory(SQLAlchemyFixturesLoader):
    __model__ = Category

    @staticmethod
    def env_group() -> list:
        return ['dev', 'prod']
