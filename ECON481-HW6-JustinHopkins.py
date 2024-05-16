import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import inspect
import pandas as pd
from sqlalchemy.orm import Session
import sqlite3

def github() -> str:

    return "https://github.com/jphopk/ECON481-Homework/blob/main/ECON481-HW6-JustinHopkins.py"

path = 'auctions.db'

class DataBase:
    def __init__(self, loc: str, db_type: str = "sqlite") -> None:
        """Initialize the class and connect to the database"""
        self.loc = loc
        self.db_type = db_type
        self.engine = create_engine(f'{self.db_type}:///{self.loc}')
    def query(self, q: str) -> pd.DataFrame:
        """Run a query against the database and return a DataFrame"""
        with Session(self.engine) as session:
            df = pd.read_sql(q, session.bind)
        return(df)

auctions = DataBase(path)

def std() -> str:
    query = """
    SELECT itemId, 
           SQRT(SUM((bidAmount - avg_bid)*(bidAmount - avg_bid)) / (COUNT(bidAmount) - 1)) AS std
    FROM (
        SELECT itemId, bidAmount, AVG(bidAmount) OVER(PARTITION BY itemId) AS avg_bid
        FROM bids
    )
    GROUP BY itemId
    HAVING (std is not null)
    """
    return query

def bidder_spend_frac() -> str:
    query = """
    WITH Sumbidder AS (
        SELECT HighbidderName AS bidderName, SUM(bidAmount) AS total_spend
        FROM (
            SELECT b1.HighbidderName, b1.bidAmount
            FROM bids b1
            JOIN (
                SELECT itemId, MAX(bidTime) AS latest_timestamp
                FROM bids
                GROUP BY itemId
            ) b2 ON b1.itemId = b2.itemId AND b1.bidTime = b2.latest_timestamp
        ) latest_bids
        GROUP BY bidderName
    ), 
    TotalBids AS (
        SELECT bidderName, MAX(bidAmount) AS total_bids
        FROM bids
        GROUP BY bidderName
    )
    SELECT s.bidderName, s.total_spend, t.total_bids, (s.total_spend / t.total_bids) AS spend_frac
    FROM Sumbidder s
    JOIN TotalBids t ON s.bidderName = t.bidderName;
    """
    return query

def min_increment_freq() -> str:
    query = """
    SELECT 
        SUM(CASE 
                WHEN b2.bidAmount = b1.bidAmount + i.bidIncrement THEN 1
                ELSE 0
            END) * 1.0 / COUNT(b2.bidAmount) AS freq
    FROM bids b1
    JOIN bids b2 ON b1.itemId = b2.itemId AND b1.bidAmount < b2.bidAmount
    JOIN items i ON i.itemId = b1.itemId
    WHERE i.isBuyNowUsed = 0
    GROUP BY b1.itemId;
    """
    return query

def win_perc_by_timestamp() -> str:
    query = """
    WITH AuctionTimes AS (
        SELECT
            itemId, MIN(bidTime) AS startTime, MAX(bidTime) AS endTime
        FROM bids
        GROUP BY itemId
    ),
    BidsWithNormalizedTime AS (
        SELECT
            b.itemId, b.bidTime, b.bidAmount, t.startTime, t.endTime,
            CASE
                WHEN (julianday(t.endTime) - julianday(b.bidTime)) / (julianday(t.endTime) - julianday(t.startTime)) < 0.1 THEN 1
                WHEN (julianday(t.endTime) - julianday(b.bidTime)) / (julianday(t.endTime) - julianday(t.startTime)) < 0.2 THEN 2
                WHEN (julianday(t.endTime) - julianday(b.bidTime)) / (julianday(t.endTime) - julianday(t.startTime)) < 0.3 THEN 3
                WHEN (julianday(t.endTime) - julianday(b.bidTime)) / (julianday(t.endTime) - julianday(t.startTime)) < 0.4 THEN 4
                WHEN (julianday(t.endTime) - julianday(b.bidTime)) / (julianday(t.endTime) - julianday(t.startTime)) < 0.5 THEN 5
                WHEN (julianday(t.endTime) - julianday(b.bidTime)) / (julianday(t.endTime) - julianday(t.startTime)) < 0.6 THEN 6
                WHEN (julianday(t.endTime) - julianday(b.bidTime)) / (julianday(t.endTime) - julianday(t.startTime)) < 0.7 THEN 7
                WHEN (julianday(t.endTime) - julianday(b.bidTime)) / (julianday(t.endTime) - julianday(t.startTime)) < 0.8 THEN 8
                WHEN (julianday(t.endTime) - julianday(b.bidTime)) / (julianday(t.endTime) - julianday(t.startTime)) < 0.9 THEN 9
                ELSE 10
            END AS timestamp_bin
        FROM bids b
        JOIN AuctionTimes t ON b.itemId = t.itemId
    ),
    WinningBids AS (
        SELECT itemId, MAX(bidAmount) AS highestBidAmount
        FROM bids
        GROUP BY itemId
    )
    SELECT
        n.timestamp_bin,
        100.0 * SUM(CASE WHEN n.bidAmount = w.highestBidAmount THEN 1 ELSE 0 END) / COUNT(*) AS win_perc
    FROM BidsWithNormalizedTime n
    JOIN WinningBids w ON n.itemId = w.itemId
    GROUP BY n.timestamp_bin
    """
    return query