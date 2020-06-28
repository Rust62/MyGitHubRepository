import self as self
from pylenium import WebElement

from royale.pages.base.pagebase import PageBase


class CardsPage ( PageBase ):
    def __init__(self , driver):
        super ().__init__ ( driver )
        self.headernav = None
        self.map = CardsPageMap ( driver )

    def goto(self):
        self.headernav.goto_cards_page ()
        return self

    def get_card_by_name(self , card_name: str) -> WebElement:
        if '' in card_name:
            card_name = card_name.replace ( '' , '+' )
        return self.map.card ( card_name )


class CardsPageMap:
    def __init__(self , driver):
        self._driver = driver

    def card(self , card_name)-> WebElement:
        return self._driver.find_element_by_css_selector ( f"[href*='{card_name}']" )
