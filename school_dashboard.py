import pandas as pd
import streamlit as st
import os

st.set_page_config(page_title="PNET Dashboard", layout="wide")
st.title("🏫 BAHRIA COLLEGE EAB-1 PNET - Parent Student Dashboard")

# List files for debugging
st.write("📁 Files in directory:", os.listdir("."))

# ====================== DATA LOAD ======================
@st.cache_data
def load_data():
    possible_files = ["data.xlsx", "Final Secy PNET Meeting List.xlsx", "data.xls", "Final Secy PNET Meeting List.xls"]
    
    for file in possible_files:
        if os.path.exists(file):
            try:
                df = pd.read_excel(file, sheet_name="Sheet1")
                st.success(f"✅ File loaded: {file}")
                return df
            except Exception as e:
                st.warning(f"Error with {file}: {e}")
    
    st.error("❌ Excel file not found! Please check file name.")
    return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# Cleaning
df["Father's Name"] = df["Father's Name"].astype(str).str.strip()

# Grouping with Unique Key
df['Unique_Parent'] = df["Father's Name"] + " | " + df.get("Mobile No", "").astype(str)

parent_groups = df.groupby(['Unique_Parent', "Father's Name", "Mobile No"]).agg(
    Total_Children=('Name', 'count'),
    Students=('Name', lambda x: ' | '.join(x)),
    Classes=('New Class', lambda x: ' | '.join(x.astype(str))),
    Family_No=('Family No', 'first'),
    Wing=('Wing', 'first')
).reset_index().drop(columns=['Unique_Parent'])

parent_groups = parent_groups.sort_values(by='Total_Children', ascending=False)

# UI
col1, col2 = st.columns(2)
col1.metric("Total Unique Parents", len(parent_groups))
col2.metric("Total Students", len(df))

search = st.text_input("🔍 Search by Parent Name", "")

if search:
    filtered = parent_groups[parent_groups["Father's Name"].str.contains(search, case=False, na=False)]
else:
    filtered = parent_groups

st.dataframe(filtered, use_container_width=True, hide_index=True)

# Details
st.subheader("👨 Click to view details")
for _, row in filtered.head(30).iterrows():   # limit for speed
    with st.expander(f"👨 {row['Father\'s Name']} — **{row['Total_Children']}** bachay"):
        parent_df = df[(df["Father's Name"] == row["Father's Name"]) & 
                       (df["Mobile No"].astype(str) == str(row["Mobile No"]))]
        st.dataframe(parent_df[["Name", "New Class", "New Sec", "Mobile No", "Wing"]], use_container_width=True, hide_index=True)
