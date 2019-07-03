from repositories.persistence_repository import PersistenceRepository
from settings import Settings

persistence_repository = PersistenceRepository()

for currency_name in Settings.CURRENCIES:
    currency_data = persistence_repository.get_currency(currency_name)
    print(currency_data.name)
    for rates_data in currency_data.rates:
        print('{0}         {1}'.format(
            rates_data.date, rates_data.rate))
