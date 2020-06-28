from typing import List

import requests
from requests.models import Response

from royale.models.card import Card


def get_all_cards() -> List[Card]:
    response = requests.get('https://statsroyale.com/api/cards')
    if response.ok:
        return[Card(**card) for card in response.json()]


    else:
       raise Exception('Response was not ok. Status Code: ' + 'response.status_code')


def get_card_by_name(card_name: Card) -> Card:
    cards = get_all_cards ()
    return next(card for card in cards if card_name == card.name)
