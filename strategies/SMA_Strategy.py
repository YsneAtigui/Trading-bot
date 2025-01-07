from strategies.Strategies import Strategies
from datetime import datetime, timedelta
import math
import time


class SMA_Strategy(Strategies):
    """
    A trading strategy based on Simple Moving Averages (SMA).

    This strategy uses two SMAs (fast and slow) to determine buy/sell signals.
    """

    def __init__(self, APIKEY, SECRETKEY, SMA_FAST, SMA_SLOW):
        """
        Initialize the SMA Strategy.

        Args:
            APIKEY (str): Alpaca API key.
            SECRETKEY (str): Alpaca secret key.
            SMA_FAST (int): Window size for the fast SMA.
            SMA_SLOW (int): Window size for the slow SMA.
        """
        super().__init__(APIKEY, SECRETKEY)
        if not isinstance(SMA_FAST, int) or SMA_FAST <= 0:
            raise ValueError("SMA_FAST must be a positive integer.")
        if not isinstance(SMA_SLOW, int) or SMA_SLOW <= 0:
            raise ValueError("SMA_SLOW must be a positive integer.")
        self.SMA_FAST = SMA_FAST
        self.SMA_SLOW = SMA_SLOW

    def get_pause(self):
        """
        Calculate the time to wait until the start of the next minute.

        Returns:
            int: Number of seconds to pause.
        """
        now = datetime.now()
        next_min = now.replace(second=0, microsecond=0) + timedelta(minutes=1)
        pause = math.ceil((next_min - now).seconds)
        print(f"Sleeping for {pause} seconds...")
        return pause

    def get_sma(self, prices, window):
        """
        Calculate the SMA for a given window.

        Args:
            prices (pd.Series): Series of price data.
            window (int): The SMA window size.

        Returns:
            pd.Series: Series containing the SMA.
        """
        if not isinstance(window, int) or window <= 0:
            raise ValueError(f"Window must be a positive integer. Received: {window}")
        return prices.rolling(window=window).mean()

    def get_signal(self, fast, slow):
        """
        Determine whether to buy or sell based on SMA values.

        Args:
            fast (pd.Series): Fast SMA values.
            slow (pd.Series): Slow SMA values.

        Returns:
            bool: True if fast SMA > slow SMA (buy signal), False otherwise.
        """
        print(f"Fast SMA: {fast.iloc[-1]} / Slow SMA: {slow.iloc[-1]}")
        return fast.iloc[-1] > slow.iloc[-1]

    def get_crypto_SMA_bars(self, symbol):
        """
        Fetch cryptocurrency data and calculate SMAs.

        Args:
            symbol (str): The cryptocurrency symbol (e.g., 'BTC/USD').

        Returns:
            pd.DataFrame: DataFrame containing cryptocurrency data and SMAs.
        """
        try:
            bars = super().get_crypto_data(symbol, "Minute")
            bars['sma_fast'] = self.get_sma(bars.close, self.SMA_FAST)
            bars['sma_slow'] = self.get_sma(bars.close, self.SMA_SLOW)
            return bars
        except Exception as e:
            raise RuntimeError(f"Failed to fetch or calculate SMAs for {symbol}: {e}")

    def get_SMA_bars(self, symbol):
        """
        Fetch stock data and calculate SMAs.

        Args:
            symbol (str): The stock symbol (e.g., 'AAPL').

        Returns:
            pd.DataFrame: DataFrame containing stock data and SMAs.
        """
        try:
            bars = super().get_stock_data(symbol, "Minute")
            bars['sma_fast'] = self.get_sma(bars.close, self.SMA_FAST)
            bars['sma_slow'] = self.get_sma(bars.close, self.SMA_SLOW)
            return bars
        except Exception as e:
            raise RuntimeError(f"Failed to fetch or calculate SMAs for {symbol}: {e}")

    def start_crypto_SMA(self, SYMBOL, QTY_PER_TRADE):
        """
        Run the SMA strategy for cryptocurrency trading.

        Args:
            SYMBOL (str): The cryptocurrency symbol (e.g., 'BTC/USD').
            QTY_PER_TRADE (float): The quantity to trade.
        """
        try:
            while True:
                # Fetch data and calculate SMAs
                bars = self.get_crypto_SMA_bars(symbol=SYMBOL)

                # Check positions
                position = super().get_position(symbol=SYMBOL)
                should_buy = self.get_signal(bars.sma_fast, bars.sma_slow)
                print(f"Position: {position} / Should Buy: {should_buy}")

                # Make trade decisions
                if position == 0 and should_buy:
                    super().make_order(SYMBOL, QTY_PER_TRADE, "BUY")
                    print(f"BUY: {QTY_PER_TRADE} {SYMBOL}")
                elif position > 0 and not should_buy:
                    super().make_order(SYMBOL, QTY_PER_TRADE, "SELL")
                    print(f"SELL: {QTY_PER_TRADE} {SYMBOL}")

                # Pause until the next minute
                time.sleep(self.get_pause())
                print("*" * 20)
        except Exception as e:
            print(f"An error occurred during strategy execution: {e}")
