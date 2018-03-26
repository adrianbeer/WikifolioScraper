from selenium.webdriver.common.by import By

def _create_finder_support(driver, container):
    container = dict(
        By.CLASS_NAME = driver.find_elements_by_class_name,
        By.CSS_SELECTOR = driver.find_elements_by_css_selector,
        By.ID = driver.find_elements_by_id,
        By.LINK_TEXT = driver.find_elements_by_link_text,
        By.NAME = driver.find_elements_by_name,
        By.PARTIAL_LINK_TEXT = driver.find_elements_by_partial_link_text,
        By.TAG_NAME = driver.find_elements_by_tag_name,
        By.XPATH = driver.find_elements_by_xpath,
    )

