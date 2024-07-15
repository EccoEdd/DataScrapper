import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

class AmazonScraper:
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
        if not self.driver:
            print("WebDriver not initialized properly.")
            return [], [], []
        
        titles = []
        authors = []
        prices = []
        
        try:
            product_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.s-main-slot div.s-result-item')
            
            for product in product_elements:
                try:
                    title = product.find_element(By.CSS_SELECTOR, 'h2 a span').text
                    titles.append(title)
                except:
                    titles.append(None)
                
                try:
                    author = product.find_element(By.CSS_SELECTOR, 'h2 + div span.a-size-base').text
                    authors.append(author)
                except:
                    authors.append(None)
                
                try:
                    price = product.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text
                    prices.append(price)
                except:
                    prices.append(None)
        
        except Exception as e:
            print(f"Error during scraping: {e}")
        
        self.driver.quit()
        
        return titles, authors, prices