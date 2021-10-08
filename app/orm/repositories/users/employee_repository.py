from app.orm.repositories.base import BaseRepository
from app.orm.models import Employee


class EmployeeRepository(BaseRepository):
    __model__ = Employee

    def find_by_email(self, email):
        with self.session_factory() as session:
            return session.query(self.model).filter_by(email=email).first()
