from alpaca_trade_api.rest import REST, TimeFrame
from datetime import datetime
import pandas as pd
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, QueryOrderStatus
from alpaca.trading.requests import GetOrdersRequest

class Strategies:
    """
    A base class for trading strategies using Alpaca API.

    Attributes:
        APIKEY (str): The API key for Alpaca.
        SECRETKEY (str): The secret key for Alpaca.
        api (REST): The Alpaca REST API client.
    """

    def __init__(self, APIKEY=None, SECRETKEY=None):
        """
        Initialize the Strategies class.

        Args:
            APIKEY (str, optional): Alpaca API key. Defaults to None.
            SECRETKEY (str, optional): Alpaca secret key. Defaults to None.
        """
        try:
            self.__APIKEY = APIKEY
            self.__SECRETKEY = SECRETKEY
            self.api = REST(key_id=APIKEY, secret_key=SECRETKEY, base_url="https://paper-api.alpaca.markets")
        except Exception as e:
            raise ValueError(f"Failed to initialize Alpaca API client: {e}")

    def set_client(self, APIKEY, SECRETKEY):
        """
        Update the API client with new credentials.

        Args:
            APIKEY (str): Alpaca API key.
            SECRETKEY (str): Alpaca secret key.
        """
        try:
            self.api = REST(key_id=APIKEY, secret_key=SECRETKEY, base_url="https://paper-api.alpaca.markets")
            self.__APIKEY = APIKEY
            self.__SECRETKEY = SECRETKEY
        except Exception as e:
            raise ValueError(f"Failed to set API client: {e}")

    def get_position(self, symbol):
        """
        Get the current position for a given symbol.

        Args:
            symbol (str): The trading symbol (e.g., 'AAPL').

        Returns:
            float: The quantity of the position. Returns 0 if no position exists.
        """
        try:
            positions = self.api.list_positions()
            for p in positions:
                if p.symbol == symbol:
                    return float(p.qty)
            return 0
        except Exception as e:
            raise RuntimeError(f"Failed to fetch positions for {symbol}: {e}")

    def get_stock_data(self, symbol, timeframe, start_date=None, end_date=None):
        """
        Fetch historical stock data.

        Args:
            symbol (str): The stock symbol (e.g., 'AAPL').
            timeframe (str): The timeframe for the data (e.g., 'Minute', 'Day').
            start_date (str, optional): The start date in ISO format. Defaults to None.
            end_date (str, optional): The end date in ISO format. Defaults to None.

        Returns:
            pd.DataFrame: A DataFrame containing the stock data.
        """
        try:
            timeframe_mapping = {
                "Minute": TimeFrame.Minute,
                "Hour": TimeFrame.Hour,
                "Day": TimeFrame.Day,
                "Week": TimeFrame.Week,
                "Month": TimeFrame.Month,
            }
            timeframe = timeframe_mapping.get(timeframe)
            bars = self.api.get_bars(symbol=symbol, timeframe=timeframe, start=start_date, end=end_date, feed="iex")
            return bars.df
        except Exception as e:
            raise RuntimeError(f"Failed to fetch stock data for {symbol}: {e}")

    def get_crypto_data(self, symbol, timeframe, start_date=None, end_date=None):
        """
        Fetch historical cryptocurrency data.

        Args:
            symbol (str): The cryptocurrency symbol (e.g., 'BTC/USD').
            timeframe (str): The timeframe for the data (e.g., 'Minute', 'Day').
            start_date (str, optional): The start date in ISO format. Defaults to None.
            end_date (str, optional): The end date in ISO format. Defaults to None.

        Returns:
            pd.DataFrame: A DataFrame containing the cryptocurrency data.
        """
        try:
            timeframe_mapping = {
                "Minute": TimeFrame.Minute,
                "Hour": TimeFrame.Hour,
                "Day": TimeFrame.Day,
                "Week": TimeFrame.Week,
                "Month": TimeFrame.Month,
            }
            timeframe = timeframe_mapping.get(timeframe)
            bars = self.api.get_crypto_bars(symbol=symbol, timeframe=timeframe, start=start_date, end=end_date)
            return bars.df
        except Exception as e:
            raise RuntimeError(f"Failed to fetch crypto data for {symbol}: {e}")

    def make_Market_order(self, symbol, qty, order):
        """
        Place a market order.

        Args:
            symbol (str): The trading symbol (e.g., 'AAPL').
            qty (float): The quantity to trade.
            order (str): 'BUY' or 'SELL'.

        Raises:
            ValueError: If the order type is invalid.
        """
        try:
            order_mapping = {"BUY": OrderSide.BUY, "SELL": OrderSide.SELL}
            order = order_mapping.get(order.upper())
            if not order:
                raise ValueError("Invalid order type. Must be 'BUY' or 'SELL'.")
            self.api.submit_order(symbol=symbol, qty=qty, side=order, type='market', time_in_force='day')
        except Exception as e:
            raise RuntimeError(f"Failed to place market order for {symbol}: {e}")

    def make_order(self, symbol, qty, order):
        """
        Place an immediate or cancel (IOC) order.

        Args:
            symbol (str): The trading symbol (e.g., 'AAPL').
            qty (float): The quantity to trade.
            order (str): 'BUY' or 'SELL'.

        Raises:
            ValueError: If the order type is invalid.
        """
        try:
            order_mapping = {"BUY": OrderSide.BUY, "SELL": OrderSide.SELL}
            order = order_mapping.get(order.upper())
            if not order:
                raise ValueError("Invalid order type. Must be 'BUY' or 'SELL'.")
            self.api.submit_order(symbol=symbol, qty=qty, side=order, time_in_force="ioc")
        except Exception as e:
            raise RuntimeError(f"Failed to place IOC order for {symbol}: {e}")

    def get_orders(self, order):
        """
        Fetch orders by type.

        Args:
            order (str): 'BUY' or 'SELL'.

        Returns:
            list: A list of orders matching the criteria.

        Raises:
            ValueError: If the order type is invalid.
        """
        try:
            trading_client = TradingClient(self.__APIKEY, self.__SECRETKEY, paper=True)
            order_mapping = {"BUY": OrderSide.BUY, "SELL": OrderSide.SELL}
            order = order_mapping.get(order.upper())
            if not order:
                raise ValueError("Invalid order type. Must be 'BUY' or 'SELL'.")
            request_params = GetOrdersRequest(status=QueryOrderStatus.ALL, side=order)
            return trading_client.get_orders(filter=request_params)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch orders: {e}")
