import os
from colorama import init, Fore, Style
from strategies.SMA_Strategy import SMA_Strategy
from strategies.RSI_Strategy import RSI_Strategy

from dotenv import load_dotenv

from utils import write_to_env
load_dotenv(dotenv_path=".env")

# Initialize colorama
init()

# Define the ASCII art using raw strings (prefix with 'r')
ascii_art = (
    Fore.WHITE + r"     __    ___    ____  _______       __________  ___    ____  _____   ________   ____  ____  ______    __    " + "\n" +
    Fore.WHITE + r"   _/ /   /   |  / __ \/  _/   |     /_  __/ __ \/   |  / __ \/  _/ | / / ____/  / __ )/ __ \/_  __/  _/ /    " + "\n" +
    Fore.GREEN + r"  / __/  / /| | / / / // // /| |      / / / /_/ / /| | / / / // //  |/ / / __   / __  / / / / / /    / __/    " + "\n" +
    Fore.GREEN + r" (_  )  / ___ |/ /_/ // // ___ |     / / / _, _/ ___ |/ /_/ // // /|  / /_/ /  / /_/ / /_/ / / /    (_  )     " + "\n" +
    Fore.WHITE + r"/  _/  /_/  |_/_____/___/_/  |_|    /_/ /_/ |_/_/  |_/_____/___/_/ |_/\____/  /_____/\____/ /_/    /  _/      " + "\n" +
    Fore.WHITE + r"/_/                                                                                                /_/        " + "\n" +
    Style.RESET_ALL  # Reset the color
)

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Displays the main menu and prompts the user for an option."""
    clear_screen()
    print(ascii_art)
    print(Fore.CYAN + "╔══════════════════════════════════════════════════╗")
    print(Fore.CYAN + "║" + Fore.YELLOW + "               Trading Strategies Menu            " + Fore.CYAN + "║")
    print(Fore.CYAN + "╠══════════════════════════════════════════════════╣")
    print(Fore.CYAN + "║" + Fore.GREEN + " 1. Execute SMA Strategy" + " " * 26 + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.GREEN + " 2. Execute RSI Strategy" + " " * 26 + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.RED + " 3. Exit" + " " * 42 + Fore.CYAN + "║")
    print(Fore.CYAN + "╚══════════════════════════════════════════════════╝" + Style.RESET_ALL)
    return input(Fore.YELLOW + "Choose an option: " + Style.RESET_ALL)

def get_user_input(prompt, input_type=str):
    """Helper function to get and validate user input."""
    while True:
        try:
            value = input_type(input(prompt))
            return value
        except ValueError:
            print(Fore.RED + f"Invalid input. Please enter a valid {input_type.__name__}." + Style.RESET_ALL)

def execute_sma_strategy():
    """Executes the SMA strategy."""
    print(Fore.CYAN + "\n--- SMA Strategy Selected ---" + Style.RESET_ALL)

    api_key = os.getenv("API_KEY")
    if not api_key or api_key.strip() == "":
        api_key = input("Enter API Key: ")
        write_to_env(".env", "API_KEY", api_key)

    secret_key = os.getenv("SECRET_KEY")
    if not secret_key or secret_key.strip() == "":
        secret_key = input("Enter Secret Key: ")
        write_to_env(".env", "SECRET_KEY", secret_key)
    
    sma_fast = get_user_input("Enter SMA Fast Period (integer): ", int)
    sma_slow = get_user_input("Enter SMA Slow Period (integer): ", int)
    
    symbol = input("Enter Symbol (e.g., BTC/USD): ")
    
    qty_per_trade = get_user_input("Enter Quantity per Trade (float): ", float)

    if sma_fast >= sma_slow:
        print(Fore.RED + "Error: SMA Fast period must be less than SMA Slow period." + Style.RESET_ALL)
        return

    sma_strategy = SMA_Strategy(api_key, secret_key, sma_fast, sma_slow)
    print(Fore.GREEN + "Starting SMA strategy..." + Style.RESET_ALL)
    try:
        sma_strategy.start_crypto_SMA(SYMBOL=symbol, QTY_PER_TRADE=qty_per_trade)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nSMA strategy stopped by user." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An error occurred while executing SMA strategy: {e}" + Style.RESET_ALL)

def execute_rsi_strategy():
    """Executes the RSI strategy."""
    print(Fore.CYAN + "\n--- RSI Strategy Selected ---" + Style.RESET_ALL)
    
    api_key = os.getenv("API_KEY")
    if not api_key or api_key.strip() == "":
        api_key = input("Enter API Key: ")
        write_to_env(".env", "API_KEY", api_key)

    secret_key = os.getenv("SECRET_KEY")
    if not secret_key or secret_key.strip() == "":
        secret_key = input("Enter Secret Key: ")
        write_to_env(".env", "SECRET_KEY", secret_key)

    symbol = input("Enter Symbol (e.g., AAPL): ")
    qty = get_user_input("Enter Quantity per Trade (float): ", float)

    rsi_strategy = RSI_Strategy(api_key, secret_key)
    print(Fore.GREEN + "Fetching stock data and executing RSI strategy..." + Style.RESET_ALL)
    try:
        rsi_strategy.trade(symbol, qty)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nRSI strategy stopped by user." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An error occurred while executing RSI strategy: {e}" + Style.RESET_ALL)

def main():
    """Main program loop."""
    while True:
        choice = display_menu()
        if choice == "1":
            execute_sma_strategy()
        elif choice == "2":
            execute_rsi_strategy()
        elif choice == "3":
            print(Fore.YELLOW + "Exiting the program. Goodbye!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
        input(Fore.CYAN + "\nPress Enter to continue..." + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nProgram terminated by user." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}" + Style.RESET_ALL)