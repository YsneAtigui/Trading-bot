from strategies.Strategies import Strategies
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


class RSI_Strategy(Strategies):
    """
    Implements an RSI-based trading strategy with additional MACD confirmation.

    Attributes:
        RSI_OVERSOLD (int): RSI value indicating oversold conditions (default: 40).
        RSI_OVERBOUGHT (int): RSI value indicating overbought conditions (default: 70).
        MACD_BUY_SIGNAL (bool): Condition for MACD buy signal.
        MACD_SELL_SIGNAL (bool): Condition for MACD sell signal.
        RISK_PERCENTAGE (float): Percentage of account balance to risk per trade.
        STOP_LOSS_PERCENTAGE (float): Stop loss percentage.
        TAKE_PROFIT_PERCENTAGE (float): Take profit percentage.
    """
    
    # Thresholds for RSI and MACD
    RSI_OVERSOLD = 40
    RSI_OVERBOUGHT = 70
    MACD_BUY_SIGNAL = True  # MACD > Signal Line
    MACD_SELL_SIGNAL = False  # MACD < Signal Line

    # Risk tolerance parameters
    RISK_PERCENTAGE = 0.02  # Risk 2% of the account balance per trade
    STOP_LOSS_PERCENTAGE = 0.02  # 2% stop loss
    TAKE_PROFIT_PERCENTAGE = 0.05  # 5% take profit

    def __init__(self, APIKEY=None, SECRETKEY=None):
        super().__init__(APIKEY, SECRETKEY)

    # Function to calculate Relative Strength Index (RSI)
    def rsi(self,data, period=14):
        """
        Calculates the Relative Strength Index (RSI).

        Args:
            data (pandas.Series): Series of closing prices.
            period (int): Lookback period for RSI calculation.

        Returns:
            pandas.Series: RSI values.
        """

        delta = data.diff().dropna()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

# Function to calculate MACD and Signal line
    def macd(self,data, short_period=12, long_period=26, signal_period=9):
        """
        Calculates the MACD line and Signal line.

        Args:
            data (pandas.DataFrame): DataFrame containing 'close' prices.
            short_period (int): Short EMA period.
            long_period (int): Long EMA period.
            signal_period (int): Signal line period.

        Returns:
            tuple: MACD line and Signal line.
        """

        short_ema = data['close'].ewm(span=short_period, adjust=False).mean()
        long_ema = data['close'].ewm(span=long_period, adjust=False).mean()
        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        return macd_line, signal_line

# Function to calculate position size based on account balance and risk tolerance
    def calculate_position_size(self,symbol, risk_percentage, stop_loss_percentage):
        """
        Calculates the position size based on risk tolerance.

        Args:
            symbol (str): Symbol of the stock/asset.
            risk_percentage (float): Percentage of account balance to risk.
            stop_loss_percentage (float): Stop loss percentage.

        Returns:
            int: Position size (number of shares).
        """
        account_balance = float(self.api.get_account().cash)  # Get available cash balance
        current_price = self.api.get_latest_trade(symbol).p
        risk_amount = account_balance * risk_percentage  # Amount to risk
        risk_per_share = current_price * stop_loss_percentage  # Risk per share
        position_size = risk_amount / risk_per_share  # Number of shares to buy
        return int(position_size)
    
    # Function to calculate the start date based on the required lookback period
    def get_date_range(self,lookback_days=365):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback_days)
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
    # Function to place a trade based on RSI strategy
    
    # Function to plot stock data (closing price and RSI)
    def plot_data(self,data, symbol, lookback_days=90):
        """
        Plots closing price, RSI, and MACD for visualization.

        Args:
            data (pandas.DataFrame): DataFrame with historical stock data.
            symbol (str): Symbol of the stock/asset.
            lookback_days (int): Number of days to visualize.
        """
        try:
            plt.figure(figsize=(14, 7))

            # Plot the closing price
            plt.subplot(3, 1, 1)
            plt.plot(data['close'], label='Close Price')
            plt.title(f'{symbol} - Close Price')
            plt.legend(loc='best')

            # Plot the RSI
            plt.subplot(3, 1, 2)
            plt.plot(data['RSI'], label='RSI', color='orange')
            plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')
            plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')
            plt.title(f'{symbol} - RSI')
            plt.legend(loc='best')

            # Highlight Buy and Sell signals for RSI
            buy_signals = data[data['RSI'] < 30]
            sell_signals = data[data['RSI'] > 70]
            if not buy_signals.empty:
                plt.scatter(buy_signals.index, buy_signals['RSI'], marker='^', color='green', label='Buy Signal')
            if not sell_signals.empty:
                plt.scatter(sell_signals.index, sell_signals['RSI'], marker='v', color='red', label='Sell Signal')

            # Plot the MACD and Signal line
            plt.subplot(3, 1, 3)
            plt.plot(data['MACD'], label='MACD Line', color='blue')
            plt.plot(data['Signal'], label='Signal Line', color='red')
            plt.title(f'{symbol} - MACD')
            plt.legend(loc='best')


            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error plotting data: {e}")

    def execute_trade_logic(self,symbol, current_rsi, current_macd, current_signal, position_qty, qty,
                        rsi_oversold, rsi_overbought, macd_buy_signal, macd_sell_signal):
        # Debugging: Print the current RSI and MACD values
        print(f"Current RSI for {symbol}: {current_rsi}")
        print(f"Current MACD for {symbol}: {current_macd}")
        print(f"Current Signal for {symbol}: {current_signal}")

    # Trading logic based on RSI and MACD
        if current_rsi < rsi_oversold and current_macd > current_signal and macd_buy_signal and position_qty == 0:
            print(f"Conditions met for buying {symbol}: RSI ({current_rsi}) < {rsi_oversold}, MACD ({current_macd}) > Signal ({current_signal})")
            try:
                print(f"Placing buy order for {symbol} (RSI: {current_rsi}, MACD: {current_macd})")
                self.api.submit_order(symbol=symbol, qty=qty, side='buy', type='market', time_in_force='gtc')
                print(f"Buy order placed for {symbol} (RSI: {current_rsi}, MACD: {current_macd})")
            except Exception as e:
                print(f"Error placing buy order: {e}")
        elif current_rsi > rsi_overbought and current_macd < current_signal and macd_sell_signal and position_qty > 0:
            print(f"Conditions met for selling {symbol}: RSI ({current_rsi}) > {rsi_overbought}, MACD ({current_macd}) < Signal ({current_signal})")
            try:
                print(f"Placing sell order for {symbol} (RSI: {current_rsi}, MACD: {current_macd})")
                self.api.submit_order(symbol=symbol, qty=position_qty, side='sell', type='market', time_in_force='gtc')
                print(f"Sell order placed for {symbol} (RSI: {current_rsi}, MACD: {current_macd})")
            except Exception as e:
                print(f"Error placing sell order: {e}")
        else:
            print(f"Holding {symbol}: No trading conditions met. (RSI: {current_rsi}, MACD: {current_macd})")



    def trade(self,symbol,qty):
        """
        Executes trades based on RSI and MACD strategy.

        Args:
            symbol (str): Stock/asset symbol.
            qty (int): Quantity to trade.
        """
        # Fetch historical data for the stock symbol
        start_date, end_date = self.get_date_range(lookback_days=730)  # Adjust the lookback period as needed
        data = self.get_stock_data(symbol,"Day",start_date, end_date)


    # Check if data is empty
        if data.empty:
            print(f"No data available for {symbol}")
            return

    # Calculate RSI and add it as a new column
        data['RSI'] = self.rsi(data['close'], 14)

    # Calculate MACD and Signal line
        data['MACD'], data['Signal'] = self.macd(data)

        if len(data) > 0:
            current_rsi = data['RSI'].iloc[-1]
            current_macd = data['MACD'].iloc[-1]
            current_signal = data['Signal'].iloc[-1]
            print(f"Current RSI for {symbol}: {current_rsi}")
            print(f"Current MACD for {symbol}: {current_macd}")
            print(f"Current Signal for {symbol}: {current_signal}")

            # Get current position in the symbol
            position_qty = self.get_position(symbol)
            print(f"Current position in {symbol}: {position_qty} shares")

            # Calculate the position size based on risk tolerance
            position_size = self.calculate_position_size(symbol, self.RISK_PERCENTAGE,self.STOP_LOSS_PERCENTAGE)
            print(f"Calculated position size: {position_size} shares")

        

            # Plot closing price, RSI, and MACD
            self.plot_data(data, symbol)

            # Execute trading logic based on RSI and MACD values
            self.execute_trade_logic(symbol, current_rsi, current_macd, current_signal, position_qty, qty,
                            self.RSI_OVERSOLD, self.RSI_OVERBOUGHT, self.MACD_BUY_SIGNAL, self.MACD_SELL_SIGNAL)
        else:
            print(f"No data available for {symbol}")