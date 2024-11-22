import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import yfinance as yf

# Configure database
DATABASE_URL = "sqlite:///./currency_prices.db"
Base = declarative_base()


class CurrencyPrice(Base):
    __tablename__ = "currency_prices"
    id = Column(Integer, primary_key=True, index=True)
    currency = Column(String, index=True)
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)


# Create database
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()


# Data pull form yfinance
def fetch_currency_data(currency_x, start_date, end_date):
    ticker = yf.Ticker(currency_x)
    data = ticker.history(start=start_date, end=end_date)
    return data


st.title('Historical Currency Prices')

# Input form
currency = st.text_input('Enter the currency ticker (e.g., EURUSD=X):', value='EURUSD=X')
start_date = st.date_input('Start date:', value=pd.to_datetime('2021-01-01'))
end_date = st.date_input('End date:', value=pd.to_datetime('today'))
fetch_data = st.button('Fetch and Save Data')

if fetch_data:
    data = fetch_currency_data(currency, start_date, end_date)
    if not data.empty:
        for index, row in data.iterrows():
            currency_price = CurrencyPrice(
                currency=currency,
                date=index,
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=row['Volume']
            )
            session.add(currency_price)
        session.commit()
        st.success(f"Data for {currency} from {start_date} to {end_date} has been saved to the database.")
    else:
        st.warning(f"No data found for {currency}.")

# Show database records
if st.button('Show Data'):
    currency_prices = session.query(CurrencyPrice).filter(CurrencyPrice.currency == currency).all()
    if currency_prices:
        df = pd.DataFrame([{
            'Date': price.date,
            'Open': price.open,
            'High': price.high,
            'Low': price.low,
            'Close': price.close,
            'Volume': price.volume
        } for price in currency_prices])
        st.dataframe(df)
    else:
        st.warning(f"No data in the database for {currency}.")

# Session close
session.close()