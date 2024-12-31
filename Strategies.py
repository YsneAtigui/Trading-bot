from alpaca_trade_api.rest import REST, TimeFrame
from datetime import datetime
import pandas as pd
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, QueryOrderStatus
from alpaca.trading.requests import GetOrdersRequest

class Strategies :

    def __init__(self,APIKEY=None,SECRETKEY=None):
        self.__APIKEY=APIKEY
        self.__SECRETKEY=SECRETKEY
        self.api = REST(key_id=APIKEY,secret_key=SECRETKEY,base_url="https://paper-api.alpaca.markets")

    def set_client(self,APIKEY,SECRETKEY):
        self.api = REST(key_id=APIKEY,secret_key=SECRETKEY,base_url="https://paper-api.alpaca.markets")
        self.__APIKEY=APIKEY
        self.__SECRETKEY=SECRETKEY
        

    def get_position(self,symbol):
        positions = self.api.list_positions()
        for p in positions:
            if p.symbol == symbol:
                return float(p.qty)
        return 0
    
    def get_stock_data(self,symbol,timeframe,start_date=None,end_date=None):
        
        timeframe_mapping = {
                        "Minute": TimeFrame.Minute,
                        "Hour": TimeFrame.Hour,
                        "Day": TimeFrame.Day,
                        "Week": TimeFrame.Week,
                        "Month": TimeFrame.Month,
                            }
        timeframe = timeframe_mapping.get(timeframe)

        bars = self.api.get_bars(symbol = symbol,
                                 timeframe= timeframe,
                                 start= start_date,
                                 end= end_date)

        return bars.df
    
    def get_crypto_data(self,symbol,timeframe,start_date=None,end_date=None):
        
        timeframe_mapping = {
                        "Minute": TimeFrame.Minute,
                        "Hour": TimeFrame.Hour,
                        "Day": TimeFrame.Day,
                        "Week": TimeFrame.Week,
                        "Month": TimeFrame.Month,
                            }
        timeframe = timeframe_mapping.get(timeframe)

        bars = self.api.get_crypto_bars(symbol = symbol,
                                 timeframe= timeframe,
                                 start= start_date,
                                 end= end_date)

        return bars.df

    def make_Market_order(self,symbol,qty,order):
        order_mapping = {
                        "BUY":OrderSide.BUY,
                        "SELL":OrderSide.SELL
        }
        
        order = order_mapping.get(order.upper())
        self.api.submit_order(
                symbol= symbol,
                qty=qty,
                side=order,
                type='market',
                time_in_force='day',
        )

    def make_order(self,symbol,qty,order):
        order_mapping = {
                        "BUY":OrderSide.BUY,
                        "SELL":OrderSide.SELL
        }
        
        order = order_mapping.get(order.upper())
        self.api.submit_order(
                symbol= symbol,
                qty=qty,
                side=order,
                time_in_force="ioc"
        )
    
    
    def get_orders(self,order):
        trading_client = TradingClient(self.__APIKEY, self.__SECRETKEY, paper=True)

        order_mapping = {
                        "BUY":OrderSide.BUY,
                        "SELL":OrderSide.SELL
        }
        order = order_mapping.get(order.upper())

        # params to filter orders by
        request_params = GetOrdersRequest(
                    status=QueryOrderStatus.ALL,
                    side=order
                 )

        # orders that satisfy params
        orders = trading_client.get_orders(filter=request_params)
        return orders