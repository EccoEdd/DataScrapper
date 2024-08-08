from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException

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

    def perform_actions(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(6)
        for action in self.actions:
            if action['type'] == 'search':
                self.perform_search(action)
            elif action['type'] == 'extract':
                data = self.extract_data(action['data'])
                return data

    def perform_search(self, action):
        search_box = self.driver.find_element(By.XPATH, action['searchBoxXPath'])
        search_box.send_keys(action['query'])
        submit_button = self.driver.find_element(By.XPATH, action['submitXPath'])
        submit_button.click()

    def extract_data(self, data_fields):
        data = []
        while True:
            page_data = []
            extracted_data = {field['name']: self.driver.find_elements(By.XPATH, field['xpath']) for field in data_fields}
            primary_field = data_fields[0]['name']
            max_len = len(extracted_data[primary_field])
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
            data.extend(page_data)
            
            if self.pagination.get('hasPaginator'):
                try:
                    next_button = self.driver.find_element(By.XPATH, self.pagination['nextPageXPath'])
                    if next_button.is_enabled():
                        next_button.click()
                        self.driver.implicitly_wait(3)
                    else:
                        break
                except NoSuchElementException:
                    break
            else:
                break
        return data

    def close_driver(self):
        if self.driver:
            self.driver.close()
            self.driver.quit()