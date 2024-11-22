import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Database setup
DATABASE_URL = "sqlite:///./countries.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database models
class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    code = Column(String, unique=True, index=True)


class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey('countries.id'))
    name = Column(String, unique=True, index=True)
    symbol = Column(String, unique=True, index=True)

    country = relationship("Country", back_populates="currencies")


class LongTermInterestRate(Base):
    __tablename__ = "long_term_interest_rates"

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey('countries.id'))
    year = Column(Integer, index=True)
    rate = Column(Float)

    country = relationship("Country", back_populates="interest_rates")


Country.currencies = relationship("Currency", order_by=Currency.id, back_populates="country")
Country.interest_rates = relationship("LongTermInterestRate", order_by=LongTermInterestRate.id,
                                      back_populates="country")

# Create database tables
Base.metadata.create_all(bind=engine)


# Streamlit app
def main():
    st.title("Country Database Application")

    menu = ["Create Country", "View Countries", "Update Country", "Delete Country",
            "Create Currency", "View Currencies", "Update Currency", "Delete Currency",
            "Create Interest Rate", "View Interest Rates", "Update Interest Rate", "Delete Interest Rate"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Create Country":
        st.subheader("Add New Country")
        name = st.text_input("Country Name")
        code = st.text_input("Country Code")

        if st.button("Add Country"):
            with SessionLocal() as session:
                new_country = Country(name=name, code=code)
                session.add(new_country)
                session.commit()
            st.success("Country added successfully")

    elif choice == "View Countries":
        st.subheader("View Countries")
        with SessionLocal() as session:
            countries = session.query(Country).all()
            for country in countries:
                st.write(f"ID: {country.id}, Name: {country.name}, Code: {country.code}")

    elif choice == "Update Country":
        st.subheader("Update Country")
        with SessionLocal() as session:
            countries = session.query(Country).all()
            country_dict = {country.name: country.id for country in countries}
            selected_country = st.selectbox("Select a Country to Update", list(country_dict.keys()))

            name = st.text_input("New Country Name")
            code = st.text_input("New Country Code")

            if st.button("Update Country"):
                country_id = country_dict[selected_country]
                country = session.query(Country).filter(Country.id == country_id).first()
                country.name = name
                country.code = code
                session.commit()
                st.success("Country updated successfully")

    elif choice == "Delete Country":
        st.subheader("Delete Country")
        with SessionLocal() as session:
            countries = session.query(Country).all()
            country_dict = {country.name: country.id for country in countries}
            selected_country = st.selectbox("Select a Country to Delete", list(country_dict.keys()))

            if st.button("Delete Country"):
                country_id = country_dict[selected_country]
                country = session.query(Country).filter(Country.id == country_id).first()
                session.delete(country)
                session.commit()
                st.success("Country deleted successfully")

    elif choice == "Create Currency":
        st.subheader("Add New Currency")
        with SessionLocal() as session:
            countries = session.query(Country).all()
            country_dict = {country.name: country.id for country in countries}
            selected_country = st.selectbox("Select Country", list(country_dict.keys()))

            name = st.text_input("Currency Name")
            symbol = st.text_input("Currency Symbol")

            if st.button("Add Currency"):
                country_id = country_dict[selected_country]
                new_currency = Currency(name=name, symbol=symbol, country_id=country_id)
                session.add(new_currency)
                session.commit()
                st.success("Currency added successfully")

    elif choice == "View Currencies":
        st.subheader("View Currencies")
        with SessionLocal() as session:
            currencies = session.query(Currency).all()
            for currency in currencies:
                st.write(
                    f"ID: {currency.id}, Name: {currency.name}, Symbol: {currency.symbol}, Country ID: {currency.country_id}")

    elif choice == "Update Currency":
        st.subheader("Update Currency")
        with SessionLocal() as session:
            currencies = session.query(Currency).all()
            currency_dict = {currency.name: currency.id for currency in currencies}
            selected_currency = st.selectbox("Select a Currency to Update", list(currency_dict.keys()))

            name = st.text_input("New Currency Name")
            symbol = st.text_input("New Currency Symbol")

            if st.button("Update Currency"):
                currency_id = currency_dict[selected_currency]
                currency = session.query(Currency).filter(Currency.id == currency_id).first()
                currency.name = name
                currency.symbol = symbol
                session.commit()
                st.success("Currency updated successfully")

    elif choice == "Delete Currency":
        st.subheader("Delete Currency")
        with SessionLocal() as session:
            currencies = session.query(Currency).all()
            currency_dict = {currency.name: currency.id for currency in currencies}
            selected_currency = st.selectbox("Select a Currency to Delete", list(currency_dict.keys()))

            if st.button("Delete Currency"):
                currency_id = currency_dict[selected_currency]
                currency = session.query(Currency).filter(Currency.id == currency_id).first()
                session.delete(currency)
                session.commit()
                st.success("Currency deleted successfully")

    elif choice == "Create Interest Rate":
        st.subheader("Add Long Term Interest Rate")
        with SessionLocal() as session:
            countries = session.query(Country).all()
            country_dict = {country.name: country.id for country in countries}
            selected_country = st.selectbox("Select Country", list(country_dict.keys()))

            year = st.number_input("Year", min_value=1900, max_value=2100, step=1)
            rate = st.number_input("Interest Rate")

            if st.button("Add Interest Rate"):
                country_id = country_dict[selected_country]
                new_rate = LongTermInterestRate(year=year, rate=rate, country_id=country_id)
                session.add(new_rate)
                session.commit()
                st.success("Interest Rate added successfully")

    elif choice == "View Interest Rates":
        st.subheader("View Long Term Interest Rates")
        with SessionLocal() as session:
            rates = session.query(LongTermInterestRate).all()
            for rate in rates:
                st.write(f"ID: {rate.id}, Year: {rate.year}, Rate: {rate.rate}, Country ID: {rate.country_id}")

    elif choice == "Update Interest Rate":
        st.subheader("Update Long Term Interest Rate")
        with SessionLocal() as session:
            rates = session.query(LongTermInterestRate).all()
            rate_dict = {f"{rate.year}, {rate.country_id}": rate.id for rate in rates}
            selected_rate = st.selectbox("Select an Interest Rate to Update", list(rate_dict.keys()))

            year = st.number_input("New Year", min_value=1900, max_value=2100, step=1)
            rate_value = st.number_input("New Rate")

            if st.button("Update Interest Rate"):
                rate_id = rate_dict[selected_rate]
                rate = session.query(LongTermInterestRate).filter(LongTermInterestRate.id == rate_id).first()
                rate.year = year
                rate.rate = rate_value
                session.commit()
                st.success("Interest Rate updated successfully")

    elif choice == "Delete Interest Rate":
        st.subheader("Delete Long Term Interest Rate")
        with SessionLocal() as session:
            rates = session.query(LongTermInterestRate).all()
            rate_dict = {f"{rate.year}, {rate.country_id}": rate.id for rate in rates}
            selected_rate = st.selectbox("Select an Interest Rate to Delete", list(rate_dict.keys()))

            if st.button("Delete Interest Rate"):
                rate_id = rate_dict[selected_rate]
                rate = session.query(LongTermInterestRate).filter(LongTermInterestRate.id == rate_id).first()
                session.delete(rate)
                session.commit()
                st.success("Interest Rate deleted successfully")


if __name__ == "__main__":
    main()