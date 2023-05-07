import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        quote = quote.lower()
        base = base.lower()

        if quote == base:
            raise APIException(f'Нельзя конвертировать одинаковые валюты: {base}.')
        try:
            quote_ticker = keys[quote]

        except KeyError:
            raise APIException(f'Неправильная или несуществующая валюта: {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Неправильная или несуществующая валюта: {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать число: {amount}')

        if amount < 0:
            raise APIException('Количество переводимой валюты должно быть положительным целым числом.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_quote = json.loads(r.content)[keys[quote]]
        total_base = total_quote * amount
        return total_base
