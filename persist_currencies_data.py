from repositories.persistence_repository import PersistenceRepository
from repositories.s3_intermediate_repository import S3IntermediateRepository
from settings import Settings


def persist_currencies_data():
    intermediate_repository = S3IntermediateRepository()
    persistence_repository = PersistenceRepository()
    for currency_name in Settings.CURRENCIES:
        currency = intermediate_repository.get_currency_data(currency_name)
        if currency is not None:
            persistence_repository.store_currency_data(currency)
            intermediate_repository.delete_currency_data(currency_name)


persist_currencies_data()
