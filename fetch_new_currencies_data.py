from data_providers.currency_rate_data_provider import CurrencyRateDataProvider
from datetime import datetime, timedelta
from models.currency import Currency
from repositories.persistence_repository import PersistenceRepository
from repositories.s3_intermediate_repository import S3IntermediateRepository
from settings import Settings


def fetch_new_currencies_data():
    currency_rate_data_provider = CurrencyRateDataProvider()
    intermediate_repository = S3IntermediateRepository()
    persistence_repository = PersistenceRepository()

    days_to_fetch = Settings.DEFAULT_DAYS_TO_FETCH
    default_from_date = datetime.today() - timedelta(days=days_to_fetch)
    to_date = datetime.today()

    for currency_name in Settings.CURRENCIES:
        from_date = persistence_repository.get_last_stored_currency_rate_date(
            currency_name)
        if from_date is None:
            from_date = default_from_date
        else:
            from_date = from_date + timedelta(days=1)
        rates = currency_rate_data_provider.get_currency_rates(
            from_date, to_date, currency_name)
        currency = Currency(currency_name, rates)
        intermediate_repository.store_currency_data(currency)


fetch_new_currencies_data()
