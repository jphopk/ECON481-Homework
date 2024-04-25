import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
from sklearn.linear_model import LogisticRegression

def github() -> str:

    return "https://github.com/jphopk/ECON481-Homework/blob/main/ECON481-HW4-JustinHopkins.py"


def load_data() -> pd.DataFrame:
    teslaData = pd.read_csv("https://lukashager.netlify.app/econ-481/data/TSLA.csv")

    return teslaData


def plot_close(df: pd.DataFrame, start: str = '2010-06-29', end: str = '2024-04-15') -> None:
    df['Date'] = pd.to_datetime(df['Date'])   
    df.set_index('Date', inplace=True)
    
    myDates = df.loc[start:end]
    
    
    plt.figure(figsize=(12, 6))
    plt.plot(myDates.index, myDates['Close'], color='blue', marker='o', markersize = 2, linestyle='-')
    plt.title(f'Tesla Stock Closing Price ({start} to {end})')
    plt.xlabel('Year')
    plt.ylabel('Closing Price ($)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def autoregress(df: pd.DataFrame) -> float:
    
    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index)
    
    df['CurrentMinusBefore'] = df['Close'].diff()
    df.dropna(inplace=True)
    df['Close_lag'] = df['CurrentMinusBefore'].shift(periods=1)
    df.dropna(inplace=True)
    
    #print(df)
    
    Y = df['CurrentMinusBefore']
    X = df['Close_lag']
    
    model = sm.OLS(Y, X)
    results = model.fit(cov_type='HC1')
    
    return results.tvalues['Close_lag']


def autoregress_logit(df: pd.DataFrame) -> float:
    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index)
    
    df['CurrentMinusBefore'] = df['Close'].diff()
    df.dropna(inplace=True)
    df['Close_lag'] = df['CurrentMinusBefore'].shift(periods=1)
    df.dropna(inplace=True)
    
    #print(df)
    
    Y = df['CurrentMinusBefore']
    X = df['Close_lag']

    newY = Y.map(lambda x: 1 if x > 0 else 0)
    
    model = sm.Logit(newY, X)
    results = model.fit()
    
    return results.tvalues['Close_lag']


def plot_delta(df: pd.DataFrame) -> None:
    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index)
    
    df['Close_lag'] = df['Close'].shift(periods=1, freq = 'D')
    df['CurrentMinusLag'] = df['Close'] - df['Close_lag']
    df.fillna(0, inplace=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['CurrentMinusLag'] , color='blue', marker='o', markersize = 2, linestyle='-', linewidth = 1)
    plt.title('Tesla Stock Change in Close Price')
    plt.xlabel('Year')
    plt.ylabel('Change in Price ($)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()