from enum import Enum


class ResultStatus(str, Enum):
    MATCH = "MATCH"
    VARIANT = "VARIANT"
    REJECT = "REJECT"


LANG_DICTIONARY = {
    "EN": {
        "accept": "Accept all",
        "results": "Visual matches"
    },
    "PL": {
        "accept": "Akceptuj wszystko",
        "results": "Dopasowania wisualne"
    }
}
