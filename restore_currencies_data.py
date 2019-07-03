from data_providers.currency_rate_data_provider import CurrencyRateDataProvider
from datetime import datetime
from models.currency import Currency
from repositories.persistence_repository import PersistenceRepository
from repositories.s3_intermediate_repository import S3IntermediateRepository


def restore_currencies_data(from_date: datetime, currency_name: str):
    currency_rate_data_provider = CurrencyRateDataProvider()
    intermediate_repository = S3IntermediateRepository()
    persistence_repository = PersistenceRepository()

    to_date = datetime.today()

    rates = currency_rate_data_provider.get_currency_rates(
        from_date, to_date, currency_name)
    intermediate_repository.store_currency_data(Currency(currency_name, rates))
    currency = intermediate_repository.get_currency_data(currency_name)
    if currency is not None:
        persistence_repository.store_non_unique_currency_data(currency)
        intermediate_repository.delete_currency_data(currency_name)
