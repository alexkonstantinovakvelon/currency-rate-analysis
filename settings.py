class Settings:
    BUCKET_NAME = 'currencyrates'
    CBR_SERVICE_URL = 'https://www.cbr.ru/eng/currency_base/dynamics/'
    CURRENCIES = ['USD', 'EUR', 'GBP', 'CHF']
    DEFAULT_DAYS_TO_FETCH = 183
    QUERY_DATE_FORMAT = '%d.%m.%Y'
    CONNECTION_STRING = 'redshift+psycopg2://{user}:{pass}@{host}:5439/dev'
    AWS_REGION = 'eu-north-1'
