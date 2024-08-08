from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException

class TableScraper:
    def __init__(self, conf):
        self.url = conf['url']
        self.xpath = conf['xpath']
        self.has_paginator = conf['hasPaginator']
        self.xpath_paginator = conf.get('xpathPaginator', None)
        self.x_column = conf.get('xColumn', None)
        self.driver = None

    def setup_driver(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    def scrape_table(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(6)

        row_count = len(self.driver.find_elements(By.XPATH, self.xpath + 'tbody/*'))
        table_not_str = False

        try:
            head = self.driver.find_element(By.XPATH, self.xpath + 'thead')
            headers = head.find_elements(By.XPATH, 'tr/*')
        except NoSuchElementException:
            table_not_str = True
            headers = self.driver.find_elements(By.XPATH, self.xpath + 'tbody/tr[1]/*')

        column_count = len(headers)
        grid = []
        type_map = {}

        while True:
            for x in range(row_count):
                if table_not_str and x == 0:
                    continue
                entry = {}
                for y in range(column_count):
                    value = self.driver.find_element(By.XPATH, self.get_xpath(x + 1, y + 1)).text.replace('\n', ' ')
                    typed_value = self.try_float(value)
                    type_map[headers[y].text] = type(typed_value)
                    entry[headers[y].text] = typed_value
                grid.append(entry)
            if self.has_paginator:
                next_btn = self.driver.find_element(By.XPATH, self.xpath_paginator)
                if next_btn.is_enabled():
                    next_btn.click()
                    self.driver.implicitly_wait(3)
                else:
                    break
            else:
                break

        return grid, type_map

    def get_xpath(self, row, column):
        return self.xpath + f'tbody/tr[{row}]/*[{column}]'

    @staticmethod
    def try_float(value):
        try:
            return float(value)
        except ValueError:
            return value

    def close_driver(self):
        if self.driver:
            self.driver.close()
            self.driver.quit()