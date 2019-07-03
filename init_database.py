from repositories.persistence_data_access import engine
from repositories.persistence_repository import CurrencyRate


def create_database():
    CurrencyRate.metadata.create_all(engine)


def delete_database():
    CurrencyRate.__table__.drop(engine)


delete_database()
create_database()
