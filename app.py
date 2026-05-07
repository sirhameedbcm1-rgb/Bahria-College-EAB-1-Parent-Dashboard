import pandas as pd
import streamlit as st
import os

st.set_page_config(page_title="PNET Dashboard", layout="wide")
st.title("🏫 BAHRIA COLLEGE EAB-1 PNET - Parent Student Dashboard")

# Debug: Files list
st.write("📁 Files in directory:")
st.write(os.listdir("."))

# Load Data with multiple attempts
@st.cache_data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv")
        st.success("✅ data.csv loaded successfully!")
        return df
    except Exception as e:
        st.error(f"CSV Load Error: {e}")
        return pd.DataFrame()
# Rest of your code (grouping etc.)
df["Father's Name"] = df["Father's Name"].astype(str).str.strip()

df['Unique_Parent'] = df["Father's Name"] + " | " + df["Mobile No"].astype(str)

parent_groups = df.groupby(['Unique_Parent', "Father's Name", "Mobile No"]).agg(
    Total_Children=('Name', 'count'),
    Students=('Name', lambda x: ' | '.join(x)),
    Classes=('New Class', lambda x: ' | '.join(x.astype(str)))
).reset_index().drop(columns=['Unique_Parent'])

parent_groups = parent_groups.sort_values(by='Total_Children', ascending=False)

# Display
col1, col2 = st.columns(2)
col1.metric("Total Unique Parents", len(parent_groups))
col2.metric("Total Students", len(df))

search = st.text_input("🔍 Search by Parent Name", "")
if search:
    filtered = parent_groups[parent_groups["Father's Name"].str.contains(search, case=False)]
else:
    filtered = parent_groups

st.dataframe(filtered, use_container_width=True, hide_index=True)
