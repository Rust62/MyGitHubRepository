from __future__ import unicode_literals, division, absolute_import, print_function

import inspect
from collections import namedtuple
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# Only for pylenium.WebElement, but importing that directly results in a circular import
import pylenium

__all__ = ['Locator', 'css', 'class_name', 'id', 'link_text', 'name', 
           'partial_link_text', 'tag', 'xpath', 'locator_from_args']


locator_keys = dict(
    css = By.CSS_SELECTOR,
    class_name = By.CLASS_NAME,
    id = By.ID,
    link_text = By.LINK_TEXT,
    name = By.NAME,
    partial_link_text = By.PARTIAL_LINK_TEXT,
    tag = By.TAG_NAME,
    xpath = By.XPATH,
)

# Inherit from a namedtuple so that a Locator can easily be converted to the 
# format that selenium webdriver expects. This should be considered an 
# implementation detail and not relied on. 
class Locator (namedtuple('Locator', ('key', 'value'))):
    contains_text = None
    text = None

    # inheriting from namedtuple means we need to override __new__ to have the desired arguments
    def __new__(cls, key, value=None, contains_text=None, text=None):
        if value == None:
            value = key
            key = cls.__name__
        key = locator_keys[key]
        obj = super(Locator, cls).__new__(cls, key, value)
        if contains_text:
            obj.contains_text = contains_text
        if text:
            obj.text = text
        return obj

    def __repr__(self):
        return '{0}({1}{2}{3})'.format(type(self).__name__, repr(self.value), 
                                       ", contains_text="+repr(self.contains_text) if self.contains_text else '',
                                       ", text="+repr(self.text) if self.text else '')

    def _test_element(self, element):
        text = element.text
        if self.contains_text and self.contains_text not in text:
            return False
        if self.text and self.text != text:
            return False
        return True

    # A separate implementation for the find_element(s) methods for efficiency reasons. We could always call
    # driver.find_elements, but that potentially returns a large list of data from the browser 
    # that we don't need.
    def _find_element(self, driver):
        "Find the first element matching this locator. The element is a selenium WebElement."
        WE = pylenium.WebElement
        if not self.contains_text and not self.text:
            return WE(driver.find_element(self.key, self.value))
        elems = [e for e in driver.find_elements(self.key, self.value) if self._test_element(e)]
        if not elems:
            raise NoSuchElementException("Unable to locate element: "+repr(self))
        return WE(elems[0])

    def _find_elements(self, driver):
        WE = pylenium.WebElement
        if not self.contains_text and not self.text:
            return [WE(e) for e in driver.find_elements(self.key, self.value)]
        return [WE(e) for e in driver.find_elements(self.key, self.value) if self._test_element(e)]

    def _has_element(self, driver):
        try:
            self._find_element(driver)
            return True
        except InvalidSelectorException:
            # don't hide invalid xpath selectors
            raise
        except NoSuchElementException:
            return False


class css (Locator): pass
class class_name (Locator): pass
class id (Locator): pass
class link_text (Locator): pass
class name (Locator): pass
class partial_link_text (Locator): pass
class tag (Locator): pass
class xpath (Locator): pass

locators = dict()
for cls in Locator.__subclasses__():
    locators[cls.__name__] = cls

def locator_from_args(locator, kwargs, stackdepth=1):
    if locator == None:
        locator = kwargs.get('locator')
        locator_keys_ = locator_keys
        for key in kwargs.keys():
            if key in locator_keys_:
                if locator:
                    raise TypeError("Multiple locators specified in call to {}. Use only one argument named {} or locator.".format(
                        inspect.stack()[stackdepth][3], ', '.join(locator_keys.keys())))
                locator = locators[key](kwargs[key])
            elif key not in ('contains_text', 'text'):
                raise TypeError('Unsupported keyword {} in call to {}'.format(key, inspect.stack()[stackdepth][3]))
    if 'contains_text' in kwargs:
        locator.contains_text = kwargs['contains_text']
    if 'text' in kwargs:
        locator.text = kwargs['text']
    return locator
