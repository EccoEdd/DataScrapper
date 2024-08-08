import pandas as pd

class DataSaver:
    @staticmethod
    def save_to_excel(titles = "", authors = "", prices = "", filename='amazon_books.xlsx'):
        data = {
            'Title': titles,
            'Author': authors,
            'Price': prices
        }
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print("All Ready")

class DataSaverUnversal:
    @staticmethod
    def save_to_excel(data, filename='scraped_data.xlsx'):
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print("All Ready")