import json
import pandas as pd
import matplotlib.pyplot as plt
import re
import unittest
from DataSaverUniversal import DataSaverUniversal
from TableScrapperUniversal import TableScraper

class TestTableScraper(unittest.TestCase):
    def setUp(self):
        with open('info.json') as file:
            self.settings = json.load(file)['settings']

    def test_scrape(self):
        for conf in self.settings:
            scraper = TableScraper(conf)
            scraper.setup_driver()
            data, type_map = scraper.scrape_table()
            file_name = re.sub(r'[^a-zA-Z\d]', '', scraper.driver.title)
            DataSaverUniversal.save_to_csv(data, file_name + '.csv')
            scraper.close_driver()

if __name__ == "__main__":
    unittest.main()
