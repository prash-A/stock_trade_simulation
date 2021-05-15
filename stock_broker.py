# json parser
import json

from datetime import datetime

# Nse tools
from nsetools import Nse
nse = Nse()

#logging 
import logging
from time import sleep
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.INFO)
'''
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
'''

# Raw Package
import numpy as np
import pandas as pd

#Data Source
import yfinance as yf


# read data files
with open('./wallet.json') as w:
  wallet = json.load(w)

with open('./investment.json') as inv:
  investment = json.load(inv)

# Investment declaration 
def invest_now():
    tickers = investment['TICKERS']
    logging.info("Investement started ...")
    for ticker in tickers:
        if invest_in(ticker) :
            logging.info("Invested in " + ticker + " successfully.")
        else:
            logging.error("Investment failed for " + ticker)
    
    logging.info("Investment done ...!")
    return


def get_current_price( ticker ):
    return nse.get_quote(ticker)['lastPrice']


def invest_in( ticker ):
    # Check if Ticker is Acitve(already invested)
    if investment[ticker]['isActive'] == True:
         logging.info( ticker + " is Active, cannot invest again")
         return True
    else:
        logging.info("Verifying " + ticker + "to invest \n")
        logging.info(" Stock details")
               
        balance = wallet['walletBalance']
        current_price = get_current_price(ticker)
        quantity = investment[ticker]['quantity']
        total_invested = current_price * quantity
        
        if total_invested > balance :
            logging.error(" Insufficient funds in wallet.")
            return False 
        
        # invested, update the variables
        investment[ticker]['isActive'] = True
        investment[ticker]['investedAmount'] = total_invested
        wallet['walletBalance'] = balance - total_invested
        wallet['totalInvested'] += total_invested
        logging.info("Invested and updated wallet and portfolio")
        return True

def keep_running():
    tickers = investment['TICKERS']
    logging.info("Market is running ...")
    
    for ticker in tickers:
        logging.info(investment[ticker])
        get_total_invested = investment[ticker]['investedAmount'] 
        current_price = get_current_price(ticker)
        current_total = current_price * investment[ticker]['quantity']
        investment[ticker]['currentValue'] = current_total

        if get_total_invested < current_total :
            investment[ticker]['profit'] = current_total - get_total_invested
            investment[ticker]['loss'] = 0
            logging.info( ticker + " is running on profit")
        elif get_total_invested == current_total:
            logging.info(ticker + " is stable")
        else:
            investment[ticker]['profit'] = 0
            investment[ticker]['loss'] = get_total_invested -current_total
            logging.info( ticker + "is running on loss")
    
    current_assets = 0
    for ticker in tickers:
        current_assets += investment[ticker]['currentValue']
    if wallet['totalInvested'] > current_assets :
        logging.info("Assets under loss")
        wallet['totalLoss'] = wallet['totalInvested'] - current_assets
    elif wallet['totalInvested'] == current_assets:
        logging.info("Assets are stable")
    else:
        logging.info("Assets running in profit")
        wallet['totalProfit'] = current_assets - wallet['totalInvested']


def display_wallet():
    print("------ Wallet Details------\n")
    print("Name             : " , wallet['Name'] , "\n")
    print("Balance          : ", wallet['walletBalance'] , "\n")
    print("Total Invested   :" , wallet['totalInvested'] , "\n")
    print("Profit           :" , wallet['totalProfit'] , "\n")
    print("Loss             :" , wallet['totalLoss'] , "\n")

    print("------ Stocks details------\n")
    for ticker in investment['TICKERS']:
        json_formatted_str = json.dumps(investment[ticker], indent=2)
        print("......." + ticker + "........\n")
        print(json_formatted_str + "\n")



if __name__ == "__main__":

    print("Starting stock broker...\n")

    display_wallet()
    
    invest_now()

    with open('wallet.json', 'w') as f1:
        json.dump(wallet, f1)
    with open('investment.json', 'w') as f2:
        json.dump(investment,f2) 

    print("Running repetitively...\n")

    now = datetime.now()
    market_open_time = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close_time = now.replace(hour=16, minute=0, second=0, microsecond=0)

    while ( now > market_open_time and now < market_close_time):
        logging.info("-------------------->>")
        keep_running()
        with open('wallet.json', 'w') as f1:
            json.dump(wallet, f1)
        with open('investment.json', 'w') as f2:
            json.dump(investment,f2)
        sleep(5)

    logging.info("Market Closed.")



