from DataSaver import DataSaver
from Scrapper import AmazonScraper

if __name__ == '__main__':
    url = 'https://www.amazon.com.mx/s?k=mushoku+tensei+light+novel&crid=1QEQLGF7KKPGR&sprefix=mushoku+tensei+lig%2Caps%2C138&ref=nb_sb_ss_pltr-xclick_1_18'
    
    scraper = AmazonScraper(url)
    scraper.open_page()
    titles, authors, prices = scraper.scrape_data()
    
    DataSaver.save_to_excel(titles, authors, prices)