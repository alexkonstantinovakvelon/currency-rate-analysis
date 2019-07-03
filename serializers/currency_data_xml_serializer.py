from datetime import datetime
from models.currency import Currency
from models.rate import Rate
from xml.dom import minidom
import xml.etree.ElementTree as ET


class CurrencyDataXmlSerializer:
    @staticmethod
    def serialize(currency: Currency) -> str:
        currency_data = ET.Element('currency')
        currency_data.set('name', currency.name)
        rates_tags = ET.SubElement(currency_data, 'rates')
        for rate_data in currency.rates:
            rate_tag = ET.SubElement(rates_tags, 'rate')
            date_tag = ET.SubElement(rate_tag, 'date')
            date_tag.text = datetime.strftime(rate_data.date, '%d/%m/%Y')
            rate_value_tag = ET.SubElement(rate_tag, 'value')
            rate_value_tag.text = str(rate_data.rate)
        xml_data = ET.tostring(currency_data).decode()
        reparsed = minidom.parseString(xml_data)
        return reparsed.toprettyxml(indent='  ')

    @staticmethod
    def deserialize(currency_data_xml: str) -> Currency:
        rates = []
        tree = ET.fromstring(currency_data_xml)
        name = tree.get('name')
        rates_tags = tree.getiterator('rate')
        for rate_tag in rates_tags:
            rates.append(Rate(
                datetime.strptime(rate_tag.find(
                    'date').text, '%d/%m/%Y').date(),
                float(rate_tag.find('value').text)))

        return Currency(name, rates)
