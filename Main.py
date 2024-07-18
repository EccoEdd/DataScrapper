from DataSaver import DataSaverUnversal
from AmazonScrapper import AmazonScraper
from WikidexScraper import WikidexScraper
from WikipediaScraper import WikipediaScraper

def get_scraper(url):
    if 'amazon.com' in url:
        return AmazonScraper(url)
    elif 'wikipedia.org' in url:
        return WikipediaScraper(url)
    elif 'wikidex.net' in url:
        return WikidexScraper(url)
    else:
        raise ValueError("Unsupported URL")

if __name__ == '__main__':
    urls = [
        'https://www.amazon.com.mx/s?k=mushoku+tensei+light+novel&crid=1QEQLGF7KKPGR&sprefix=mushoku+tensei+lig%2Caps%2C138&ref=nb_sb_ss_pltr-xclick_1_18',
        'https://es.wikipedia.org/wiki/.hack',
        'https://www.wikidex.net/wiki/Lista_de_cartas_de_Pokémon_Trading_Card_Game'
    ]
    
    for url in urls:
        scraper = get_scraper(url)
        scraper.open_page()
        data = scraper.scrape_data()
        DataSaverUnversal.save_to_excel(data, filename=f'scraped_data_{url.split("//")[1].split("/")[0]}.xlsx')