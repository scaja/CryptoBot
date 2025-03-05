import unittest  # Import the unittest module for testing
import preprocessing_script as preprocessing_script  # Import the preprocessing script

# Sample test data for BTC/USDT historical trades
test_btcusdt_historical_data = [
    {'id': 5891933, 'price': '95105.83000000', 'qty': '0.00390000', 'quoteQty': '370.91273700', 
     'time': 1735475154753, 'isBuyerMaker': True, 'isBestMatch': True},
    {'id': 5891934, 'price': '95105.83000000', 'qty': '0.00010000', 'quoteQty': '9.51058300', 
     'time': 1735475157292, 'isBuyerMaker': True, 'isBestMatch': True},
    {'id': 5891935, 'price': '95105.83000000', 'qty': '0.00395000', 'quoteQty': '375.66802850', 
     'time': 1735475157292, 'isBuyerMaker': True, 'isBestMatch': True}
]

# Sample test data for ETH/BTC historical trades
test_ethbtc_historical_data = [
    {'id': 1119631, 'price': '0.03579000', 'qty': '0.08970000', 'quoteQty': '0.00321036', 
     'time': 1735474923864, 'isBuyerMaker': False, 'isBestMatch': True},
    {'id': 1119632, 'price': '0.03577000', 'qty': '0.09420000', 'quoteQty': '0.00336953', 
     'time': 1735474934411, 'isBuyerMaker': False, 'isBestMatch': True},
    {'id': 1119633, 'price': '0.03577000', 'qty': '0.12670000', 'quoteQty': '0.00453205', 
     'time': 1735475026478, 'isBuyerMaker': False, 'isBestMatch': True}
]

# Define a test class that extends unittest.TestCase
class TestDataCleaner(unittest.TestCase):

    # Test if BTC/USDT historical data transformation correctly converts timestamps
    def test_btcusdt_historical_data_transformation(self):
        btcusdt_df = preprocessing_script.build_trad_data_frame(test_btcusdt_historical_data, "BTCUSDT")
        assert "2024-12-29 12:25:54.753000" == str(btcusdt_df.loc[0]['time']), \
            "BTC/USDT could not find expected time in the column"

    # Test if ETH/BTC historical data transformation correctly converts timestamps
    def test_etcbtc_historical_data_transformation(self):
        ethbtc_df = preprocessing_script.build_trad_data_frame(test_ethbtc_historical_data, "ETHBTC")
        assert "2024-12-29 12:22:03.864000" == str(ethbtc_df.loc[0]['time']), \
            "ETH/BTC could not find expected time in the column"

    # Test if BTC/USDT data format has the correct column names
    def test_btcusdt_historical_data_format(self):
        btcusdt_df = preprocessing_script.build_trad_data_frame(test_btcusdt_historical_data, "BTCUSDT")
        assert list(btcusdt_df.columns) == ['time', 'price', 'symbol'], \
            "BTC/USDT DataFrame columns do not match expected format"

    # Test if ETH/BTC data format has the correct column names
    def test_etcbtc_historical_data_format(self):
        ethbtc_df = preprocessing_script.build_trad_data_frame(test_ethbtc_historical_data, "ETHBTC")
        assert list(ethbtc_df.columns) == ['time', 'price', 'symbol'], \
            "ETH/BTC DataFrame columns do not match expected format"
    
# Run the tests if the script is executed directly
if __name__ == '__main__':
    unittest.main()
