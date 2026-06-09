import streamlit as st
import pandas as pd
from streamlit_app import stock_data


st.title("Stock File", text_alignment="center")
search_product = st.text_input("Enter product")

search_df = stock_data[stock_data['Product'].str.contains(search_product, case=False, na=False)]
st.write(search_df)
