from datetime import datetime
from models.currency import Currency
from models.rate import Rate
from repositories.persistence_data_access import session
from sqlalchemy import Column, String, Date, Float, exc
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base


class PersistenceRepository:
    def get_last_stored_currency_rate_date(self,
                                           currency_name: str) -> datetime:
        result = session.query(func.max(CurrencyRate.date)).filter(
            CurrencyRate.currency == currency_name).first()[0]
        if result is None:
            return None
        return result

    def store_currency_data(self, _currency: Currency):
        data_objects = []
        for rate in _currency.rates:
            data_object = CurrencyRate(
                currency=_currency.name,
                date=rate.date,
                rate=rate.rate)
            data_objects.append(data_object)
        session.bulk_save_objects(data_objects)
        session.commit()

    def store_non_unique_currency_data(self, _currency: Currency):
        for rate in _currency.rates:
            try:
                data_object = CurrencyRate(
                    currency=_currency.name, date=rate.date, rate=rate.rate)
                session.add(data_object)
                session.commit()
            except exc.IntegrityError:
                session.rollback()
                print('Record exists. Skipping insert.')

    def get_currency(self, _currency_name) -> Currency:
        currency_rates_data = session.query(CurrencyRate).filter_by(
            currency=_currency_name)
        rates = map(lambda c: Rate(c.date, c.rate), currency_rates_data)
        return Currency(_currency_name, rates)


class CurrencyRate(declarative_base()):
    __tablename__ = 'currencyrates'

    currency = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)
    rate = Column(Float)
