Pylenium
========

This is a wrapper around the Selenium Webdriver Python API, which provides a more Pythonic interface. The main differences are in the element selectors and the condition API. Pylenium allows you to do ``driver.find_element(css='body')`` instead of ``driver.find_element(By.CSS_SELECTOR, 'body')``. 

Other differences: 

- There is a ``link_text`` selector. The conditions and WebElements have also been wrapped to support the new selectors. 
- There are a number of new conditions available such as ``any`` and ``not_or_gone`` that can be composed with other conditions. 
- It is possible to use normal python callables as conditions.



