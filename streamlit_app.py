import streamlit as st
import pandas as pd
from pathlib import Path

st.title("Stock Checker", text_alignment="center")

current_dir = Path(__file__).parent
file_path = current_dir / "All Stock.xlsx"

stock_data = pd.read_excel(file_path)



product = st.selectbox("Enter product", stock_data['Product'], index = None, placeholder="Products", filter_mode="fuzzy")

if product:
    stock = stock_data.loc[stock_data["Product"] == product]
    
    if(stock.iloc[0,4] != 0):  st.subheader(f"Township : {int(stock.iloc[0,4])}")
    if(stock.iloc[0,1] != 0):  st.subheader(f"Brandreth Road : {stock.iloc[0,1]}")
    if(stock.iloc[0,2] != 0):  st.subheader(f"Manga Mandi : {stock.iloc[0,2]}")
    if(stock.iloc[0,3] != 0):  st.subheader(f"PIA : {stock.iloc[0,3]}")
