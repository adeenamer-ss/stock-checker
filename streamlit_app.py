import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json
import os

st.title("Stock Checker", text_alignment = "center")

DISPLAY_ORDER = ["TOWNSHIP", "BRANDRETH ROAD", "MANGA MANDI", "P-I-A"]

@st.cache_resource
def get_client():
    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_json = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_json, scopes=scopes)
    return gspread.authorize(creds)

@st.cache_data(ttl=3600)
def load_stock_data():
    records = get_client().open("Stock In Hand - Syed Sons").sheet1.get_all_records()
    return pd.DataFrame(records).set_index("Product")

stock_data = load_stock_data()

product = st.selectbox("Enter product", stock_data.index, index=None, placeholder="Products", filter_mode = "fuzzy")

if product:
    row = stock_data.loc[product]
    for location in DISPLAY_ORDER:
        qty = row[location]
        if qty != 0:
            st.subheader(f"{location} : {int(qty)}")
