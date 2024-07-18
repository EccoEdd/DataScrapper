from selenium.webdriver.common.by import By
from WebScrapper import WebScraper

class WikipediaScraper(WebScraper):
    def scrape_data(self):
        titles = []

        if not self.driver:
            print("WebDriver not initialized properly.")
            return {'Title': titles}
        
        try:
            table_elements = self.driver.find_elements(By.CSS_SELECTOR, 'table.wikitable tbody tr')
            
            for row in table_elements:
                try:
                    title = row.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text
                    titles.append(title)
                except:
                    titles.append(None)
        
        except Exception as e:
            print(f"Error during scraping: {e}")
        
        self.close()
        
        return {'Title': titles}