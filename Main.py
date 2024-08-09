import json
import re
import unittest
from DataSaver import DataSaverUniversal
from Scrapper import TableScraper

class TestTableScraper(unittest.TestCase):
    def setUp(self):
        with open('examen.json', encoding='utf-8') as file:
            self.all_settings = json.load(file)

    def test_scrape_all(self):
        for key, settings_list in self.all_settings.items():
            for settings in settings_list:
                scraper = TableScraper(settings)
                scraper.setup_driver()
                try:
                    data = scraper.perform_actions()
                    file_name = re.sub(r'[^a-zA-Z\d]', '', scraper.driver.title)
                    DataSaverUniversal.save_to_csv(data, file_name + f'_{key}.csv')
                except Exception as e:
                    print(f"Error during scraping for {key}: {e}")
                finally:
                    scraper.close_driver()

if __name__ == "__main__":
    unittest.main()
