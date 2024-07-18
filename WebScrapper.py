import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

class WebScraper:
    def __init__(self, url):
        self.url = url
        try:
            self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        except Exception as e:
            print(f"Error setting up WebDriver: {e}")
            self.driver = None

    def open_page(self):
        if self.driver:
            self.driver.get(self.url)
            time.sleep(10)
    
    def scrape_data(self):
        raise NotImplementedError("This method needs to be implemented by subclasses")
    
    def close(self):
        if self.driver:
            self.driver.quit()