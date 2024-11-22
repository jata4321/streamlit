import streamlit as st
import pandas as pd


# Function to fetch data from the given URL
def fetch_forecast_data(url):
    tables = pd.read_html(url, header=[0], index_col=0,
                          keep_default_na=False, displayed_only=True,
                          )
    return tables


# Streamlit app
def main():
    st.title("Economic Forecasts Data from ING")

    url = "https://think.ing.com/forecasts/"

    st.subheader("Fetching data from:")
    st.write(url)

    # Fetching data from the URL
    try:
        forecast_data = fetch_forecast_data(url)
        st.success("Data fetched successfully!")

        # Displaying the fetched tables
        for i, table in enumerate(forecast_data):
            st.subheader(f"Table {i + 1}")
            st.dataframe(table)

    except Exception as e:
        st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()