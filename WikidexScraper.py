from selenium.webdriver.common.by import By
from WebScrapper import WebScraper

class WikidexScraper(WebScraper):
    def scrape_data(self):
        names = []
        numbers = []

        if not self.driver:
            print("WebDriver not initialized properly.")
            return {'Name': names, 'Number': numbers}
        
        try:
            coliseo_header = self.driver.find_element(By.XPATH, "//span[text()='Coliseo']")
            table = coliseo_header.find_element(By.XPATH, "./following::table[1]")
            rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')
            
            for row in rows:
                try:
                    name = row.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text
                    names.append(name)
                except:
                    names.append(None)
                
                try:
                    number = row.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text
                    numbers.append(number)
                except:
                    numbers.append(None)
        
        except Exception as e:
            print(f"Error during scraping: {e}")
        
        self.close()
        
        return {'ID': names, 'Info': numbers}