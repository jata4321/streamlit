import streamlit as st
import yfinance as yf
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from streamlit_login_auth_ui.widgets import __login__

# Predefined Users
predefined_users = {
    "user1": "password1",
    "user2": "password2",
}

# Email settings
gmail_user = 'your-email@gmail.com'
gmail_password = 'your-password'


def send_email(username):
    recipient = 'recepient@gmail.com'
    subject = f"{username} Logged In"
    body = f"User {username} has logged in to the Streamlit application."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = recipient

    with SMTP("smtp.gmail.com") as smtp:
        smtp.login(gmail_user, gmail_password)
        smtp.sendmail(gmail_user, recipient, msg.as_string())


def main():
    login_component = __login__(predefined_users.keys())
    authenticated, username, password = login_component.build_login_ui()

    if authenticated:
        if predefined_users[username] == password:
            st.title("Stock Price History Viewer")

            send_email(username)

            ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, GOOGL)", "AAPL")
            if ticker:
                stock_data = yf.Ticker(ticker)
                history = stock_data.history(period="1y")

                st.line_chart(history.Close)
        else:
            st.error("Incorrect username or password.")
    else:
        st.info("Please log in.")


if __name__ == "__main__":
    main()