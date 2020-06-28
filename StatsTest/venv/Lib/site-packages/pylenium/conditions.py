from __future__ import unicode_literals, division, absolute_import, print_function

import six
from six.moves import builtins
import inspect
import selenium.webdriver.support.expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException, \
    StaleElementReferenceException, NoAlertPresentException

from .locator import Locator, locator_from_args


def _element_present(element):
    try:
        element.is_enabled()
        return True
    except StaleElementReferenceException:
        return False

def _parse_args(args, kwargs, arg_name=None):
    """Supported orders: <locator>, <locator, value>, <element>, <element, value>. 
    Locator can be either a locator instance or a keyword arg e.g. css='body'. 
    All three can be specified in the original call as either named or positional parameters."""
    locator = kwargs.get('locator')
    element = kwargs.get('element')
    if locator == element == None and args:
        if isinstance(args[0], Locator):
            locator = args[0]
            args = args[1:]
        elif isinstance(args[0], WebElement):
            element = args[0]
            args = args[1:]
    if locator == element == None:
        locator = locator_from_args(None, kwargs, stackdepth=2)
        if locator == None:
            raise TypeError("No locator or element found for {}".format(inspect.stack()[1][3]))
    if arg_name == None or args:
        return (locator, element) + args
    return (locator, element, kwargs[arg_name])


class Condition (object):
    def test(self, driver):
        try:
            return self(driver)
        except (StaleElementReferenceException, NoSuchElementException):
            return False

class _element_mixin (Condition):
    def __init__(self, *args, **kwargs):
        self.locator, self.element = _parse_args(args, kwargs)

    def get_element(self, driver):
        if self.element is not None:
            return self.element
        return driver.find_element(self.locator)

class _element_value_mixin (_element_mixin):
    def __init__(self, *args, **kwargs):
        self.locator, self.element, argument = _parse_args(args, kwargs, arg_name=self.argument_name)
        setattr(self, self.argument_name, argument)
    

class title_is (Condition, ec.title_is):
    pass

class in_title (Condition, ec.title_contains):
    pass

class element_present (_element_mixin, ec.presence_of_element_located):
    """Test if an element is present
    element_present(<locator or element>)"""

    def __call__(self, driver):
        if self.element:
            return element if _element_present(self.element) else False
        try:
            return driver.find_element(self.locator)
        except NoSuchElementException:
            return False

class element_visible (_element_mixin, ec.visibility_of_element_located, ec.visibility_of):
    """Tests if an element is visible. If the element does not exist, raise an exception"""

    def __call__(self, driver):
        element = self.get_element(driver)
        return element if element.is_displayed() else False
        
class text_in_element (_element_value_mixin, ec.text_to_be_present_in_element):
    argument_name = 'text'

    def __call__(self, driver):
        return self.text in self.get_element(driver).text
        
class text_in_element_value (_element_value_mixin, ec.text_to_be_present_in_element_value):
    argument_name = 'text'

    def __call__(self, driver):
        value = self.get_element(driver).get_attribute('value')
        return self.text in value if value else False
        
class switch_to_frame (Condition, ec.frame_to_be_available_and_switch_to_it):
    def __init__(self, frame):
        self.frame_ref = frame

    def __call__(self, driver):
        try:
            return driver.switch_to.frame(self.frame_ref)
        except NoSuchFrameException:
            return False

class element_invisible (_element_mixin, ec.invisibility_of_element_located):
    def __call__(self, driver):
        element = self.get_element(driver)
        return element if not element.is_displayed() else False

class element_clickable (_element_mixin, ec.element_to_be_clickable):
    def __call__(self, driver):
        element = self.get_element(driver)
        return element if element.is_displayed() and element.is_enabled() else False

class element_gone_stale (Condition, ec.staleness_of):
    def __init__(self, element):
        self.element = element

    def __call__(self, driver):
        return not _element_present(self.element)

class element_selected (_element_mixin, ec.element_to_be_selected, ec.element_located_to_be_selected):
    def __call__(self, driver):
        return self.get_element(driver).is_selected()

class element_selection_state (_element_value_mixin, ec.element_selection_state_to_be, ec.element_located_selection_state_to_be):
    argument_name = 'selected'

    def __call__(self, driver):
        return self.get_element(driver).is_selected() == self.selected

class alert_present (Condition, ec.alert_is_present):
    pass

class all (Condition):
    """Returns True if all conditions are true"""
    def __init__(self, *conditions):
        self.conditions = conditions

    def __call__(self, driver):
        try:
            return builtins.all(c(driver) for c in self.conditions)
        except (NoSuchElementException, StaleElementReferenceException):
            return False

class any (Condition):
    """Returns the result of the first true condition, or False"""
    def __init__(self, *conditions):
        self.conditions = conditions

    def __call__(self, driver):
        for c in self.conditions:
            try:
                result = c(driver)
                if result:
                    return result
            except (NoSuchElementException, StaleElementReferenceException):
                continue
        return False

class not_ (Condition):
    """Negates the condition. Any exceptions are passed through."""
    def __init__(self, condition):
        self.condition = condition

    def __call__(self, driver):
        return not self.condition(driver)

class not_or_gone (Condition):
    """Returns True if the condition is False or if it throws a NoSuchElementException or 
    StaleElementReferenceException"""
    def __init__(self, condition):
        self.condition = condition

    def __call__(self, driver):
        try:
            return not self.condition(driver)
        except (NoSuchElementException, StaleElementReferenceException):
            return True

class true_or_gone (Condition):
    """Returns the result of the condition if it is true. Also return True on a NoSuchElementException or 
    StaleElementReferenceException"""
    def __init__(self, condition):
        self.condition = condition

    def __call__(self, driver):
        try:
            return self.condition(driver)
        except (NoSuchElementException, StaleElementReferenceException):
            return True
