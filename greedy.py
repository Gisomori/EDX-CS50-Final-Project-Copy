import cs50
import math


QUARTER = 0.25
DIME = 0.10
NICKEL = 0.05
PENNY = 0.01
TOTAL_COINS = 0
COINS_USED = 0
PAY_IN = 0

def get_positive_float():
    while True:
        n = cs50.get_float()
        if n > 0:
            break
    return n

def left_over_calc(coinType):

    global PAY_IN
    global TOTAL_COINS
    global COINS_USED

    COINS_USED =  math.floor( PAY_IN / coinType)
    TOTAL_COINS = COINS_USED +  TOTAL_COINS
    PAY_IN = round(PAY_IN - (COINS_USED *  coinType),2)

def main():
    print('O hai! How much change is owed?')
    global PAY_IN
    PAY_IN = get_positive_float()

    if(PAY_IN >= QUARTER):
        left_over_calc(QUARTER)
    if(PAY_IN >= DIME):
        left_over_calc(DIME)
    if(PAY_IN >= NICKEL):
        left_over_calc(NICKEL)
    if(PAY_IN >= PENNY):
        left_over_calc(PENNY)
    print(TOTAL_COINS)

if __name__ == "__main__":
    main()
