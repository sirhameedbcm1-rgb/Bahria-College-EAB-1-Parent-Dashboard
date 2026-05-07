import streamlit as st
import pandas as pd

st.title("Parent Student Dashboard")

# ================== DATA LOADING ==================
@st.cache_data
def load_data():
    try:
        # Agar CSV use kar rahe ho
        df = pd.read_csv("data.csv")
        
        # Agar Excel use kar rahe ho
        # df = pd.read_excel("data.xlsx")
        
        # Cleaning
        df["Father's Name"] = df["Father's Name"].astype(str).str.strip()
        # baqi cleaning yahan karo...
        
        return df
    except Exception as e:
        st.error(f"Data load nahi ho saka: {e}")
        return None

df = load_data()

if df is None:
    st.stop()   # app yahan ruk jayegi

# ================== Baqi App Code ==================
st.write("Data loaded successfully!")
st.dataframe(df.head())
# aapka dashboard code yahan...
