import streamlit as st
import pandas as pd
import re

from pandas.core.interchange.dataframe_protocol import DataFrame


# Function to fetch data from the given URL
def fetch_forecast_data(url):
    tables = pd.read_html(url, header=[0], index_col=0)
    return tables


# Function to filter tables to find the one containing GDP growth
def filter_gdp_growth_table(tables) -> DataFrame | None:
    for table in tables:
        if any("YoY%" or "GDP" or "Growth" or "QoQ% Annualised" in str(col) for col in table.columns):
            return table.dropna()
    return None


# Function to clean and reformat the column names
def clean_table_columns(table):
    def clean_column_name(name):

        quarter_to_month = {
            1:'March',
            2:'June',
            3:'September',
            4:'December'
        }

        # Remove 'F' letter and any leading/trailing whitespace
        name = name.replace('F', '').strip()

        # Match the pattern for quarters or year (e.g., 'Q1 2021', '2022')
        match = re.match(r'(\dQ\d{2})', name)
        if match:
            return quarter_to_month[int(str(match.group(1))[:1])] +' 20' +str(match.group(1))[2:]
        return name

    table.columns = [clean_column_name(col) for col in table.columns]
    return table


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

        # Filtering to find the GDP growth table
        gdp_growth_table = filter_gdp_growth_table(forecast_data)

        if gdp_growth_table is not None:
            # Cleaning and reformatting the table columns
            cleaned_table = clean_table_columns(gdp_growth_table)

            st.subheader("GDP Growth Table")
            st.dataframe(cleaned_table, use_container_width=True)
        else:
            st.error("No table containing GDP growth data was found.")

    except Exception as e:
        st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()