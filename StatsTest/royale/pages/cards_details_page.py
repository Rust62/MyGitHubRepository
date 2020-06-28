from selenium.webdriver.remote.webelement import WebElement

from royale.pages.base.pagebase import PageBase


class CardDetailsPage ( PageBase ):
    def __init__(self , driver):
        super ().__init__ ( driver )
        self.map = CardDetailsPageMap


class CardDetailsPageMap:
    def __init__(self , driver):
        self._driver = driver

    @property
    def card_id(self) -> WebElement:
        return self._driver.find_element_by_css_selector ( "[class*='card_id']" )

    @property
    def card_cost(self) -> WebElement:
        return self._driver.find_element_by_css_selector ( "[class*='card_cost']" )

    @property
    def card_icon(self) -> WebElement:
        return self._driver.find_element_by_css_selector ( "[class*='card_icon']" )

    @property
    def card_name(self) -> WebElement:
        return self._driver.find_element_by_css_selector ( "[class*='card_name']" )

    @property
    def card_category(self) -> WebElement:
        return self._driver.find_element_by_css_selector ( "[class*='card_rarity']" )

    @property
    def card_rarity(self) -> WebElement:
        return self._driver.find_element_by_css_selector ( "[class*='rarityCaption']" )
