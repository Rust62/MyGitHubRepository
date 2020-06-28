


class HeaderNav:
    def __init__(self, driver):
        self.map = HeaderNavMap(driver)

    def goto_cards_page(self):
        self.map.cards_link.click()


class HeaderNavMap:
    def __init__(self, driver):
        self._driver = driver

    @property
    def cards_link(self):
        return self._driver.find_element_by_css_selector("[href*='/cards']")
