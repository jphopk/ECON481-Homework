def github() -> str:
    return "https://github.com/jphopk/ECON481-Homework/blob/main/ECON481-HW1-JustinHopkins.py"

def evens_and_odds(n: int) -> dict:
    evensSum = 0
    oddsSum = 0
    for i in range(0, n, 2):
        evensSum += i
    
    for i in range(1, n, 2):
        oddsSum += i
    
    return {'evens': evensSum, 'odds': oddsSum}


from datetime import datetime, date, time, timedelta
from typing import Union

def time_diff(date_1: str, date_2: str, out: str) -> Union[str,float]:
    dt1 = datetime.strptime(date_1, "%Y-%m-%d")
    dt2 = datetime.strptime(date_2, "%Y-%m-%d")
    delta = dt2-dt1
    daysBtwn = abs(delta.days)
    if (out == "string"):
        return "There are " + str(daysBtwn) + " days between the two dates"
    else:
        return daysBtwn

def reverse(in_list: list) -> list:
    newList = []
    for i in range(-1, -len(in_list) - 1, -1):
        newList.append(in_list[i])
    
    return newList

def prob_k_heads(n: int, k: int) -> float:
    nminuskfac = 1
    for i in range(1,n-k+1):
        nminuskfac *= i
    nchoosek = 1
    for i in range(k+1, n+1):
        nchoosek *= i
    nchoosek /= nminuskfac
    
    return nchoosek*(0.5**n)