import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

class DataSaverUniversal:
    @staticmethod
    def save_to_csv(data, filename):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        logging.info(f"Data saved to {filename}")
