import streamlit as st
import pandas as pd

st.set_page_config(page_title="Parent Dashboard", layout="wide")

st.title("Parent Student Dashboard")

# Data Load
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")        # ya pd.read_excel("data.xlsx")
    # Basic cleaning
    df = df.fillna("")
    return df

df = load_data()

st.success(f"✅ Data Loaded Successfully! **Total Records: {len(df)}**")

# ================== BETTER DATA TABLE ==================
st.subheader("Student Data")

# Bara aur searchable table
st.dataframe(
    df,
    use_container_width=True,
    height=700,           # height barha do
    hide_index=False,
)

# Extra Features (Recommended)
col1, col2, col3 = st.columns(3)
with col1:
    st.write(f"**Total Students:** {len(df)}")
with col2:
    search = st.text_input("🔍 Search Father's Name / Student Name")
with col3:
    if st.button("Download Full Data"):
        st.download_button(
            label="📥 Download as CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="parent_student_data.csv",
            mime="text/csv"
        )
