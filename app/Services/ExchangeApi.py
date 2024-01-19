import requests

class CurrencyExchangeApi:

    def __init__(self) -> None:
        self.url = "https://currency-exchange.p.rapidapi.com/exchange"
        self.headers = {
                    "X-RapidAPI-Key": "427a90fc41msh4ce02db795252e4p149596jsnbd9b123ef525",
                    "X-RapidAPI-Host": "currency-exchange.p.rapidapi.com"
        }

    def get_exhange_rate(self, from_currency, to_currency):
        querystring = {"from":from_currency,"to":to_currency,"q":1}
        response = requests.get(self.url, headers=self.headers, params=querystring)

        return response.json()
