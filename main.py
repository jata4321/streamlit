import streamlit as st
import yfinance as yf
import altair as alt
import pandas as pd

from datetime import date


class Stock:
    def __init__(self, ticker='CAT'):
        self.ticker = yf.Ticker(ticker)
        self.industry = self.ticker.info.get('sectorKey')

    def __repr__(self):
        return f"{self.ticker.ticker}"

    def get_info(self):
        stock_info = self.ticker.info["longBusinessSummary"]
        return stock_info

    def get_news(self):
        stock_news_list = list()
        stock_news = self.ticker.news
        for i, value in enumerate(stock_news):
            stock_news_list.append({'title': value['title'], 'link': value['link']})
        stock_news = pd.DataFrame(stock_news_list)
        return stock_news

    def get_quotes(self, start_date='2022-01-01', end_date=None):
        stock_history = self.ticker.history(start=start_date, end=end_date)
        return stock_history

    def get_volatility(self, start_date='2022-01-01', end_date=None):
        stock_history = self.ticker.history(start=start_date, end=end_date)
        stock_volatility = stock_history.copy()
        stock_volatility['Volatility'] = stock_volatility['Close'] / stock_volatility['Close'].shift() - 1
        return stock_volatility

    def get_balance(self):
        stock_balance = self.ticker.balance_sheet
        return stock_balance

    def get_cashflow(self):
        stock_cashflow = self.ticker.cash_flow
        return stock_cashflow

    def get_income_statement(self):
        stock_income_statement = self.ticker.income_stmt
        return stock_income_statement

    def get_calendar(self):
        stock_calendar = self.ticker.calendar
        return stock_calendar

    def get_earning_estimates(self):
        stock_earning_estimates = self.ticker.earnings_estimate
        return stock_earning_estimates

    def get_revenue_estimates(self):
        stock_revenue_estimates = self.ticker.revenue_estimate
        return stock_revenue_estimates

    def get_eps_trends(self):
        stock_eps_estimates_trends = self.ticker.eps_trend
        return stock_eps_estimates_trends

    def get_recommendations(self):
        stock_recommendations = self.ticker.recommendations_summary
        stock_price_targets = self.ticker.analyst_price_targets
        recommendations = {'stock_recommendations': stock_recommendations,
                           'stock_price_targets': stock_price_targets}
        return recommendations


st.title('Analytic world!')
st.subheader(f'This is sub-header for stock analysis')

tickers = st.selectbox('Stock name:', ['AAPL', 'CAT', 'PLTR',
                                       'BA', 'MSFT',
                                       'C', 'GE', 'FDX', 'DIS',
                                       'PZU.WA', 'OPL.WA',
                                       'ETFBTBSP.WA', 'ETFBM40TR.WA',
                                       'IHYA.L'], key='ticker')
stock = Stock(st.session_state['ticker'])

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['General information',
                                              'Price history',
                                              'Balance Sheet',
                                              'Cash Flow',
                                              'Income Statement',
                                              'Estimates'])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f'Data for the {stock.ticker.ticker}')
    with col2:
        st.slider('Slider:', 0, 10, 0)
    try:
        st.markdown(stock.get_info())
    except KeyError as e:
        pass
    st.divider()
    st.subheader('News roll:')
    st.dataframe(stock.get_news())

with tab2:
    st.date_input('Pick start date:', value=date(2024, 1, 2), key='start_date')
    st.number_input('Insert moving average length:', min_value=1, max_value=250, step=1, value=1, key='moving_average')
    df = stock.get_quotes(start_date=st.session_state["start_date"])
    df['Ma'] = df['Close'].rolling(st.session_state['moving_average']).mean()
    st.write(f'Stock price of {stock}')

    ax_type = st.checkbox('Y axis log type:', value=False)
    if ax_type:
        type_of_axis = "symlog"
    else:
        type_of_axis = "linear"

    st.altair_chart(alt.Chart(df.reset_index()).transform_fold(['Close', 'Ma'])
                    .mark_line()
                    .encode(x=alt.X('Date:T', axis=alt.Axis(format='%B %Y')),
                            y=alt.Y('value:Q').scale(domainMin=df['Close'].min() * 0.98, type=type_of_axis),
                            color='key:O'), use_container_width=True)
    df_vol = stock.get_volatility(start_date=st.session_state['start_date'])
    st.line_chart(df_vol['Volatility'])
    st.expander('Price history').dataframe(df)

with tab3:
    st.dataframe(stock.get_balance())

with tab4:
    st.expander('Expand frame to see data: ').dataframe(stock.get_calendar())
    st.dataframe(stock.get_cashflow())

with tab5:
    try:
        df_inc_stat = pd.DataFrame(stock.get_income_statement())
        inc_stat_items = df_inc_stat.index
        st.selectbox('Choose your option:', options=inc_stat_items, key='income_statement_item')
        st.dataframe(df_inc_stat)
        dff = df_inc_stat.loc[st.session_state['income_statement_item']].reset_index()
        st.bar_chart(dff[st.session_state['income_statement_item']]
                     .sort_index(ascending=False)
                     .reset_index(drop=True))
    except KeyError as e:
        pass

with tab6:
    st.expander('Estimates for the revenues').table(stock.get_revenue_estimates())
    st.expander('Estimates for the eps').table(stock.get_earning_estimates())
    st.expander('Change of estimates for the eps').table(stock.get_eps_trends())
    st.radio('Select:',
             options=['stock_recommendations', 'stock_price_targets'],
             horizontal=True,
             key='radio_choice')
    st.expander('Change of recommendations').table(stock.get_recommendations()[st.session_state['radio_choice']])
