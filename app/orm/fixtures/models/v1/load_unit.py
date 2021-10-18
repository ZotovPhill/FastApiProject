from fpgen.example.models.goods import Unit
from fpgen.orm.sqlalchemy.sqla_fixtures_loader import SQLAlchemyFixturesLoader


class LoadUnit(SQLAlchemyFixturesLoader):
    __model__ = Unit

    @staticmethod
    def env_group() -> list:
        return ['dev', 'prod']
