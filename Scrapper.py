import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

logging.basicConfig(level=logging.INFO)

class TableScraper:
    def __init__(self, conf):
        self.url = conf['url']
        self.actions = conf['actions']
        self.pagination = conf.get('pagination', {})
        self.driver = None

    def setup_driver(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
        self.driver.get(self.url)

    def perform_actions(self):
        all_data = []
        for action in self.actions:
            if action['type'] == 'select':
                self._perform_select(action)
            elif action['type'] == 'search':
                self._perform_search(action)
            elif action['type'] == 'extract':
                page_data = self._extract_data(action['data'])
                all_data.extend(page_data)

                while self._handle_pagination():
                    page_data = self._extract_data(action['data'])
                    all_data.extend(page_data)

        return all_data
    
    def _perform_select(self, action):
        try:
            select_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, action['selectXPath']))
            )
            select = Select(select_element)
            select.select_by_visible_text(action['optionValue'])
            logging.info(f"Selected option '{action['optionValue']}' from the dropdown.")
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Error selecting option: {e}")
            raise

    def _perform_search(self, action):
        try:
            search_box = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, action['searchBoxXPath']))
            )
            search_box.send_keys(action['query'])
            submit_button = self.driver.find_element(By.XPATH, action['submitXPath'])
            submit_button.click()
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']"))
            )
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Error performing search: {e}")
            raise

    def _extract_data(self, data_fields):
        extracted_data = {}
        for field in data_fields:
            try:
                elements = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, field['xpath']))
                )
                extracted_data[field['name']] = elements
            except (NoSuchElementException, TimeoutException):
                logging.warning(f"No elements found for {field['name']} using XPath {field['xpath']}")
                extracted_data[field['name']] = []

        primary_field = data_fields[0]['name']
        max_len = len(extracted_data.get(primary_field, []))

        page_data = []
        for i in range(max_len):
            item = {}
            for field in data_fields:
                elements = extracted_data[field['name']]
                if i < len(elements):
                    value = elements[i].text if 'attribute' not in field else elements[i].get_attribute(field['attribute'])
                    item[field['name']] = value
                else:
                    item[field['name']] = None
            page_data.append(item)
        return page_data

    def _handle_pagination(self):
        if self.pagination.get('hasPaginator'):
            try:
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.pagination['nextPageXPath']))
                )
                if next_button:
                    next_button.click()
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']"))
                    )
                    return True
            except (NoSuchElementException, TimeoutException) as e:
                logging.info("No more pages to navigate or unable to click next button.")
                return False
        return False

    def close_driver(self):
        if self.driver:
            self.driver.quit()
