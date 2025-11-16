from enum import Enum

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR" 
    GBP = "GBP"
    JPY = "JPY"
    CAD = "CAD"
    AUD = "AUD"
    CHF = "CHF"
    CNY = "CNY"
    SEK = "SEK"
    NZD = "NZD"
    BDT = "BDT"

CURRENCY_MAP = {
    "USD": Currency.USD, "$": Currency.USD, "DOLLAR": Currency.USD, "US DOLLAR": Currency.USD,
    "EUR": Currency.EUR, "€": Currency.EUR, "EURO": Currency.EUR,
    "GBP": Currency.GBP, "£": Currency.GBP, "POUND": Currency.GBP,
    "CAD": Currency.CAD, "CAD$": Currency.CAD,
    "BDT": Currency.BDT, "TAKA": Currency.BDT,
}

VALID_CURRENCIES = list(Currency)