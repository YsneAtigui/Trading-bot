from strategies.Strategies import Strategies
from datetime import datetime, timedelta
import math
import time


class SMA_Strategy(Strategies):
    
    def __init__(self, APIKEY, SECRETKEY, SMA_FAST , SMA_SLOW ):
        super().__init__(APIKEY, SECRETKEY)
        self.SMA_FAST = SMA_FAST
        self.SMA_SLOW=SMA_SLOW

    # Description is given in the article
    def get_pause(self):
        now = datetime.now()
        next_min = now.replace(second=0, microsecond=0) + timedelta(minutes=1)
        pause = math.ceil((next_min - now).seconds)
        print(f"Sleep for {pause}")
        return pause
    
    # Returns a series with the moving average
    def get_sma(self, prices, window):

        if not isinstance(window, int) or window <= 0:
            raise ValueError(f"window must be a positive integer {window}")
        return prices.rolling(window=window).mean()      

    # Checks wether we should buy (fast ma > slow ma)
    def get_signal(self, fast, slow):
        print(f"Fast {fast.iloc[-1]}  /  Slow: {slow.iloc[-1]}")
        return fast.iloc[-1] > slow.iloc[-1]
    
    # Get up-to-date 1 minute data from Alpaca and add the moving averages
    def get_crypto_SMA_bars(self,symbol):
        bars = super().get_crypto_data(symbol,"Minute")
        bars['sma_fast'] = self.get_sma(bars.close, self.SMA_FAST)
        bars['sma_slow'] = self.get_sma(bars.close, self.SMA_SLOW)
        return bars
    
    def get_SMA_bars(self,symbol):
        bars = super().get_stock_data(symbol,"Minute")
        bars[f'sma_fast'] = self.get_sma(bars.close, self.SMA_FAST)
        bars[f'sma_slow'] = self.get_sma(bars.close, self.SMA_SLOW)
        return bars

    def start_crypto_SMA(self,SYMBOL,QTY_PER_TRADE):
        
        while True:
            # GET DATA
            bars = self.get_crypto_SMA_bars(symbol=SYMBOL)
            # CHECK POSITIONS
            position = super().get_position(symbol=SYMBOL)
            should_buy = self.get_signal(bars.sma_fast,bars.sma_slow)
            print(f"Position: {position} / Should Buy: {should_buy}")
            if position == 0 and should_buy == True:
            # WE BUY
                super().make_order(SYMBOL,QTY_PER_TRADE,"BUY")
                print(f'Symbol: {SYMBOL} / Side: BUY / Quantity: {QTY_PER_TRADE}')
            elif position > 0 and should_buy == False:
            # WE SELL
                super().make_order(SYMBOL,QTY_PER_TRADE,"SELL")
                print(f'Symbol: {SYMBOL} / Side: SELL / Quantity: {QTY_PER_TRADE}')

            time.sleep(self.get_pause())
            print("*"*20)