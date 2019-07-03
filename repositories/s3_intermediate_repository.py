from botocore.exceptions import ClientError
from models.currency import Currency
from serializers.currency_data_xml_serializer import CurrencyDataXmlSerializer
from settings import Settings
import boto3


class S3IntermediateRepository:
    def __init__(self):
        self.s3_client = boto3.client('s3', region_name=Settings.AWS_REGION)
        self.s3_resource = boto3.resource(
            's3', region_name=Settings.AWS_REGION)
        self.ensure_bucket_exists()

    def store_currency_data(self, currency: Currency):
        currency_data_xml = CurrencyDataXmlSerializer.serialize(currency)
        self.s3_client.put_object(
            Body=currency_data_xml,
            Bucket=Settings.BUCKET_NAME,
            Key=S3IntermediateRepository.__get_file_name__(currency.name))

    def get_currency_data(self, currency_name: str) -> Currency:
        obj = self.s3_client.get_object(
            Bucket=Settings.BUCKET_NAME,
            Key=S3IntermediateRepository.__get_file_name__(currency_name))
        currency_data_xml = obj['Body'].read()
        currency = CurrencyDataXmlSerializer.deserialize(currency_data_xml)
        return currency

    def delete_currency_data(self, currency_name: str):
        file_name = S3IntermediateRepository.__get_file_name__(currency_name)
        try:
            self.s3_client.delete_object(
                Bucket=Settings.BUCKET_NAME, Key=file_name)
        except ClientError:
            return

    def ensure_bucket_exists(self):
        bucket = self.s3_resource.Bucket(Settings.BUCKET_NAME)
        if bucket.creation_date is None:
            location = {'LocationConstraint': Settings.AWS_REGION}
            self.s3_client.create_bucket(Bucket=Settings.BUCKET_NAME,
                                         CreateBucketConfiguration=location)

    @staticmethod
    def __get_file_name__(currency_name: str):
        return '{0}.xml'.format(currency_name)
