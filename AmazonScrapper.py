from selenium.webdriver.common.by import By
from WebScrapper import WebScraper

class AmazonScraper(WebScraper):
    def scrape_data(self):
        titles = []
        authors = []
        prices = []

        if not self.driver:
            print("WebDriver not initialized properly.")
            return {'Title': titles, 'Author': authors, 'Price': prices}
        
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
        
        self.close()
        
        return {'Title': titles, 'Author': authors, 'Price': prices}